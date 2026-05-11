// Last-page memory for HA panel re-entry.
// HA UI keeps the iframe alive when switching dashboards but reloads it on
// some panel changes. Save current path on hide / unload, restore when the
// iframe lands at root after re-entry.
(function () {
  const KEY = "ha-docs-mkdocs-lastpath";

  function save() {
    try {
      localStorage.setItem(KEY, location.pathname + location.search + location.hash);
    } catch (_) {}
  }

  function restore() {
    let saved;
    try {
      saved = localStorage.getItem(KEY);
    } catch (_) {
      return;
    }
    if (!saved) return;
    const atRoot =
      (location.pathname === "/" || /\/(index\.html?)?$/.test(location.pathname)) &&
      !location.search &&
      !location.hash;
    if (atRoot && saved !== location.pathname) {
      location.replace(saved);
    }
  }

  // Restore once on initial load (the iframe just mounted).
  restore();

  // Save on every nav-away event: visibility change (HA dashboard switch keeps
  // iframe alive), beforeunload (iframe full reload), popstate (in-page nav).
  document.addEventListener("visibilitychange", save);
  window.addEventListener("beforeunload", save);
  window.addEventListener("popstate", save);
})();
