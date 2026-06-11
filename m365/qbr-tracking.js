/*
 * Shared GA4 tracking helper for IntelliThing m365 product pages.
 *
 * - Loads gtag.js only if a global tag is not already on the page.
 * - Exposes window.trackEvent(name, params) with default params
 *   (product, page_path, page_title) merged in.
 * - Declarative click tracking: any element with data-track="event_name"
 *   (optionally data-cta-location="...") fires that event on click.
 * - Optional page-load and scroll-depth events via <body> attributes:
 *     <body data-track-page-view="qbr_page_view" data-track-scroll>
 */
(function () {
  var GA_ID = 'G-LR50K84QEZ';
  var PRODUCT = 'merchant_qbr_autopilot';

  window.dataLayer = window.dataLayer || [];
  if (typeof window.gtag !== 'function') {
    window.gtag = function () { window.dataLayer.push(arguments); };
  }

  // Do not double-load GA if a global tag already exists on the page.
  if (!document.querySelector('script[src*="googletagmanager.com/gtag/js"]')) {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    window.gtag('js', new Date());
    window.gtag('config', GA_ID);
  }

  function baseParams() {
    return {
      product: PRODUCT,
      page_path: window.location.pathname + window.location.search,
      page_title: document.title
    };
  }

  window.trackEvent = function (name, params) {
    var merged = baseParams();
    if (params) {
      for (var k in params) {
        if (Object.prototype.hasOwnProperty.call(params, k)) merged[k] = params[k];
      }
    }
    window.gtag('event', name, merged);
  };

  document.addEventListener('click', function (e) {
    var el = e.target && e.target.closest ? e.target.closest('[data-track]') : null;
    if (!el) return;
    var params = {};
    if (el.getAttribute('data-cta-location')) params.cta_location = el.getAttribute('data-cta-location');
    var href = el.getAttribute('href');
    if (href) params.link_url = href;
    window.trackEvent(el.getAttribute('data-track'), params);
  });

  function init() {
    var body = document.body;

    var pageViewEvent = body.getAttribute('data-track-page-view');
    if (pageViewEvent) window.trackEvent(pageViewEvent);

    if (body.hasAttribute('data-track-scroll')) {
      var fired50 = false;
      var fired90 = false;
      var onScroll = function () {
        var doc = document.documentElement;
        var max = doc.scrollHeight - window.innerHeight;
        var pct = max > 0 ? (window.scrollY / max) * 100 : 100;
        if (!fired50 && pct >= 50) {
          fired50 = true;
          window.trackEvent('qbr_scroll_50', { percent_scrolled: 50 });
        }
        if (!fired90 && pct >= 90) {
          fired90 = true;
          window.trackEvent('qbr_scroll_90', { percent_scrolled: 90 });
        }
        if (fired50 && fired90) window.removeEventListener('scroll', onScroll);
      };
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
