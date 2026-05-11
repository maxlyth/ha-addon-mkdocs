// Intercept Cmd+F / Ctrl+F and open Material's search instead of browser Find.
// Tested in HA ingress iframe context: iframe keydown handlers fire when the
// iframe has focus, so this overrides the default for in-panel users.
(function () {
  function openSearch() {
    const toggle = document.getElementById("__search");
    if (toggle) toggle.checked = true;
    // Focus after Material's transition completes (~150ms in default theme).
    setTimeout(function () {
      const input = document.querySelector(".md-search__input");
      if (input) {
        input.focus();
        input.select();
      }
    }, 80);
  }

  document.addEventListener(
    "keydown",
    function (e) {
      // Cmd+F (macOS) or Ctrl+F (Windows/Linux); ignore Shift+/ etc.
      const isFindCombo =
        (e.metaKey || e.ctrlKey) &&
        !e.shiftKey &&
        !e.altKey &&
        (e.key === "f" || e.key === "F" || e.code === "KeyF");
      if (!isFindCombo) return;
      e.preventDefault();
      e.stopPropagation();
      openSearch();
    },
    true // capture phase — fire before any other handler
  );
})();
