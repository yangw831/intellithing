// Copy-link behavior for article share buttons. The share URL comes from the
// page's canonical link so the same script works on every article.
document.addEventListener("DOMContentLoaded", function () {
  var canonical = document.querySelector('link[rel="canonical"]');
  var url = canonical ? canonical.href : window.location.href;
  var checkIcon =
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>';

  function legacyCopy(text) {
    var area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.top = "-1000px";
    document.body.appendChild(area);
    area.select();
    try {
      document.execCommand("copy");
    } catch (e) {
      /* nothing left to try */
    }
    document.body.removeChild(area);
  }

  document.querySelectorAll(".share-copy").forEach(function (button) {
    var linkIcon = button.innerHTML;
    var resetTimer = null;
    button.addEventListener("click", function () {
      var written = navigator.clipboard
        ? navigator.clipboard.writeText(url)
        : Promise.reject();
      written
        .catch(function () {
          legacyCopy(url);
        })
        .then(function () {
          button.innerHTML = checkIcon;
          button.setAttribute("title", "Copied");
          clearTimeout(resetTimer);
          resetTimer = setTimeout(function () {
            button.innerHTML = linkIcon;
            button.setAttribute("title", "Copy link");
          }, 2000);
        });
    });
  });
});
