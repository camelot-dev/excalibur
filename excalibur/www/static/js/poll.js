// Poll the current page in the background instead of a 0.5 s meta refresh,
// so the "Processing" page does not flicker. Reload once the server stops
// rendering the waiting state. Based on #85.
(function () {
  const marker = document.querySelector('[data-processing]');
  if (!marker) {
    return;
  }
  const poll = function () {
    fetch(window.location.href, { cache: 'no-store' })
      .then(function (response) { return response.text(); })
      .then(function (html) {
        if (html.indexOf('data-processing') === -1) {
          window.location.reload();
        } else {
          setTimeout(poll, 1000);
        }
      })
      .catch(function () { setTimeout(poll, 3000); });
  };
  setTimeout(poll, 1000);
})();
