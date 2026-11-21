// Poll the current page in the background instead of a 0.5 s meta refresh,
// so the "Processing" page does not flicker. Reload once the server stops
// rendering the waiting state (done or failed). Based on #85; elapsed time
// and the slow-PDF hint are from #113.
(function () {
  const marker = document.querySelector('[data-processing]');
  if (!marker) {
    return;
  }
  const started = Date.now();
  const elapsed = marker.querySelector('[data-elapsed]');
  const slowHint = marker.querySelector('[data-slow-hint]');
  const tick = function () {
    const seconds = Math.floor((Date.now() - started) / 1000);
    if (elapsed) {
      const m = Math.floor(seconds / 60);
      elapsed.textContent = m ? m + 'm ' + (seconds % 60) + 's' : seconds + 's';
    }
    if (slowHint && seconds >= 30) {
      slowHint.classList.remove('d-none');
    }
  };
  setInterval(tick, 1000);

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
