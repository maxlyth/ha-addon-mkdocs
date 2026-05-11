#!/usr/bin/env python3
"""Vault watcher + rebuilder for mkdocs.

Runs as a long-lived sidecar. Uses watchdog's PollingObserver because
inotify does not propagate through the addon container's bind-mount
boundaries; this is the standard library-managed fallback used by mkdocs,
hugo, esbuild, vite and friends when native filesystem events are
unavailable.

Behaviour:
  * On start: mirror /homeassistant/documentation -> /config/docs and run
    `mkdocs build` so nginx has fresh static output to serve.
  * Continuously poll the vault every 60s. On any detected change,
    re-mirror and re-build. Deletions in the vault propagate (mirror
    is destructive on the user-vault subset; preserves any addon-seeded
    files that are not in the vault).
  * Self-correcting: every poll cycle re-checks state, so any silent
    drift gets fixed on the next cycle.
"""
import logging
import shutil
import subprocess
import sys
import time
from pathlib import Path

try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers.polling import PollingObserver
except ImportError:
    print("vault-watcher: watchdog not installed — exiting", file=sys.stderr)
    sys.exit(1)


VAULT = Path("/homeassistant/documentation")
DOCS = Path("/config/docs")
SITE = Path("/tmp/mkdocs_built")
MKDOCS_YML = "/config/mkdocs.yml"
POLL_INTERVAL_SEC = 60

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [vault-watcher] %(message)s",
    datefmt="%H:%M:%S",
)


# Track files this watcher has previously synced from VAULT into DOCS, so
# deletions in VAULT can be mirrored without touching XB-seeded sample files
# (addons/, assets/, images/, index.md, 404.md) which the watcher never owns.
_synced_from_vault: set[Path] = set()


def sync_vault():
    """Mirror VAULT into DOCS. Tracks previously-synced relative paths;
    files we synced earlier that are no longer in VAULT are deleted from
    DOCS. XB-seeded sample files (anything we never synced) are untouched.
    """
    global _synced_from_vault
    if not VAULT.is_dir():
        logging.warning(f"{VAULT} not present; skipping sync")
        return

    current: set[Path] = set()
    for src in VAULT.rglob("*"):
        if src.is_file():
            rel = src.relative_to(VAULT)
            current.add(rel)
            dst = DOCS / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    # mkdocs needs an index.md as the landing page; vault uses README.md by
    # convention, so mirror it to index.md for the home page.
    readme = VAULT / "README.md"
    if readme.is_file():
        idx = DOCS / "index.md"
        shutil.copy2(readme, idx)
        current.add(Path("index.md"))

    # Mirror deletions: anything we synced before but isn't in VAULT now -> remove
    for rel in _synced_from_vault - current:
        dst = DOCS / rel
        if dst.is_file():
            try:
                dst.unlink()
                logging.info(f"removed (no longer in vault): {rel}")
                # Clean up empty parent dirs (best-effort)
                parent = dst.parent
                while parent != DOCS and not any(parent.iterdir()):
                    parent.rmdir()
                    parent = parent.parent
            except OSError as e:
                logging.warning(f"failed to remove {dst}: {e}")

    _synced_from_vault = current


def rebuild_site():
    SITE.parent.mkdir(parents=True, exist_ok=True)
    if SITE.exists():
        shutil.rmtree(SITE)
    result = subprocess.run(
        ["mkdocs", "build", "--quiet",
         "--config-file", MKDOCS_YML,
         "--site-dir", str(SITE)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        logging.error(f"mkdocs build failed (rc={result.returncode}): {result.stderr[:300]}")
        return False
    logging.info("rebuilt OK")
    return True


class Handler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self._dirty = False

    def on_any_event(self, event):
        if event.is_directory:
            return
        # Mark dirty; the main loop debounces and rebuilds at most once per poll cycle.
        self._dirty = True
        logging.info(f"change: {event.event_type} {event.src_path}")


def main():
    if not VAULT.is_dir():
        logging.warning(f"{VAULT} not mounted; watcher will idle. Vault changes will not propagate.")

    logging.info("initial build")
    rebuild_site()

    handler = Handler()
    observer = PollingObserver(timeout=POLL_INTERVAL_SEC)
    if VAULT.is_dir():
        observer.schedule(handler, str(VAULT), recursive=True)
        observer.start()
        logging.info(f"polling {VAULT} every {POLL_INTERVAL_SEC}s")

    try:
        while True:
            time.sleep(POLL_INTERVAL_SEC)
            if handler._dirty:
                handler._dirty = False
                logging.info("rebuilding after detected change")
                rebuild_site()
    except KeyboardInterrupt:
        if observer.is_alive():
            observer.stop()
            observer.join()


if __name__ == "__main__":
    main()
