# Changelog

All notable changes to this project will be documented in this file.

## 1.1.8 - 05-11-2026

- ➕ Add `vault_path` option (default `/homeassistant/documentation`) so a single addon image can serve any directory under the host's HA config. The s6 run script reads `bashio::config 'vault_path'` on every start, patches `docs_dir` in `/config/mkdocs.yml`, and exports `VAULT_PATH` for the watcher. Enables N installs of the same image with different sidebar entries, each scoped to a different sub-vault.

## 1.1.7 - 05-11-2026

- ➕ Mount Home Assistant config read-only via `homeassistant_config:ro`; defaults `docs_dir` to `/homeassistant/documentation` so an external Markdown vault can be served with no copy step.
- ➕ Vault watcher sidecar (`vault-watcher.py`): library-managed `PollingObserver` (60s) rebuilds the static site on any change in the mounted vault. inotify does not propagate through addon bind-mounts, so polling is the standard fallback (same pattern mkdocs/hugo/vite use when native FS events are unavailable).
- ➕ Light + dark palette with toggle (Material `prefers-color-scheme` pair); slate foreground variables nudged up to match Home Assistant's text contrast.
- ➕ Cmd/Ctrl+F shortcut handler opens Material's search overlay instead of the browser find-in-page (`search-shortcut.js`).
- ➕ Last-page memory: persists the last viewed path to `localStorage` on hide/unload/nav events and restores it when the iframe re-mounts at root (`page-memory.js`).
- ➕ Per-file "last updated" dates via **mkdocs-git-revision-date-localized-plugin** `1.4.7`.
- ➕ Static-asset bundle injected via mkdocs `hooks.py` (CSS, JS, icon, logo) so no `extra_files:` copy step is needed.
- 🔁 Image namespace moved to `ghcr.io/maxlyth/{arch}-addon-mkdocs`.
- 🗑️ Dropped the seeded `addons/mkdocs/help.md` sample tree; the addon no longer ships demo content.

## 1.1.6 - 03-15-2025

- ⬆️ Bump **actions/checkout** `4.1.7` ➜ `4.2.1`
- ⬆️ Bump **frenck/action-addon-linter** `2.16` ➜ `2.17`
- ⬆️ Bump **mkdocs-macros-plugin** `1.2.0` ➜ `1.3.6`
- ⬆️ Bump **mkdocs-material** `9.5.38` ➜ `9.5.42`
- ⬆️ Bump **pymdown-extensions** `10.10.2` ➜ `10.11.2`

## 1.1.5 - 01-30-2025

- ⬆️ Bump **mkdocs-material** `9.5.49` ➜ `9.5.50`
- ⬆️ Bump **pymdown-extensions** `10.12` ➜ `10.14.1`

## 1.1.4 - 12-24-2024

- ⬆️ Bump **mkdocs-material** `9.5.45` ➜ `9.5.49`
- ⬆️ Bump **jinja2** `3.1.4` ➜ `3.1.5`
- ⬆️ Bump **mkdocs-awesome-pages-plugin** `2.9.3` ➜ `2.10.1`
- ⬆️ Bump **click** `8.1.7` ➜ `8.1.8`

## 1.1.3 - 11-25-2024

- ⬆️ Bump **actions/checkout** `4.1.7` ➜ `4.2.1`
- ⬆️ Bump **frenck/action-addon-linter** `2.16` ➜ `2.17`
- ⬆️ Bump **mkdocs-macros-plugin** `1.2.0` ➜ `1.3.6`
- ⬆️ Bump **mkdocs-material** `9.5.38` ➜ `9.5.42`
- ⬆️ Bump **pymdown-extensions** `10.10.2` ➜ `10.11.2`

## 1.1.2 - 10-24-2024

- ⬆️ Bump **mkdocs-macros-plugin** `1.2.0` ➜ `1.3.6`
- ⬆️ Bump **mkdocs-material** `9.5.38` ➜ `9.5.42`
- ⬆️ Bump **pymdown-extensions** `10.10.2` ➜ `10.11.2`

## 1.1.1 - 09-27-2024

- ⬆️ Bump **mkdocs-macros-plugin** `1.0.5` ➜ `1.2.0`
- ➕ Add **mkdocs-awesome-pages-plugin** `2.9.3`
- ➕ Add **mkdocs-glightbox** `0.4.0`
- ⬆️ Bump **mkdocs-material** `9.5.34` ➜ `9.5.38`
- ⬆️ Bump **plantuml-markdown** `3.10.3` ➜ `3.10.4`
- ⬆️ Bump **pymdown-extensions** `10.9` ➜ `10.10.2`

## 1.1.0 - 09-01-2024

- ⬆️ Bump **Markdown** `3.6` ➜ `3.7`
- ⬆️ Bump **mkdocs-material** `9.5.29` ➜ `9.5.34`
- ⬆️ Bump **mkdocs** `1.6.0` ➜ `1.6.1`
- ⬆️ Bump **plantuml-markdown** `3.9.8` ➜ `3.10.3`
- ⬆️ Bump **pymdown-extensions** `10.8.1` ➜ `10.9`

## 1.0.0 - 08-01-2024

**Initial release:**

- ➕ Add **click** `8.1.7`
- ➕ Add **Jinja2** `3.1.4`
- ➕ Add **Markdown** `3.6`
- ➕ Add **mkdocs-macros-plugin** `1.0.5`
- ➕ Add **mkdocs-material-extensions** `1.3.1`
- ➕ Add **mkdocs-material** `9.5.29`
- ➕ Add **mkdocs** `1.6.0`
- ➕ Add **plantuml-markdown** `3.9.8`
- ➕ Add **pymdown-extensions** `10.8.1`
