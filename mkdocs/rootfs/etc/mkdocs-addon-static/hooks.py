"""mkdocs build hooks for the ha-addon-mkdocs fork.

  * Injects our addon-internal stylesheet + JS as virtual `assets/` files
    so they appear in the build output without polluting the user's vault.
  * Aliases the vault's README.md as index.md so it serves as the home page
    (the vault has no index.md by convention; mkdocs needs one).
"""
from pathlib import Path
from mkdocs.structure.files import File

ADDON_STATIC = Path("/etc/mkdocs-addon-static")
INJECTED = [
    ("stylesheet.css",  "assets/stylesheet.css"),
    ("search-shortcut.js", "assets/search-shortcut.js"),
    ("page-memory.js",  "assets/page-memory.js"),
    ("mkdocs_icon.png", "assets/mkdocs_icon.png"),
    ("logo.png",        "images/logo.png"),
]


def on_files(files, config):
    use_dir_urls = config.get("use_directory_urls", False)
    docs_dir = config["docs_dir"]
    site_dir = config.get("site_dir", "")

    # Inject addon-internal CSS/JS as virtual files at <docs_dir>/assets/
    for name, virtual_path in INJECTED:
        src = ADDON_STATIC / name
        if not src.is_file():
            continue
        f = File(
            path=virtual_path,
            src_dir=str(ADDON_STATIC),
            dest_dir=site_dir,
            use_directory_urls=use_dir_urls,
        )
        f.abs_src_path = str(src)
        files.append(f)

    # Alias README.md as index.md so it serves as the homepage.
    readme = next((f for f in files if f.src_path == "README.md"), None)
    if readme and not any(f.src_path == "index.md" for f in files):
        idx = File(
            path="index.md",
            src_dir=readme.src_dir,
            dest_dir=readme.dest_dir,
            use_directory_urls=use_dir_urls,
        )
        idx.abs_src_path = readme.abs_src_path
        files.append(idx)
        # Drop README.md to avoid duplicate /readme.html alongside the home page.
        files.remove(readme)

    return files
