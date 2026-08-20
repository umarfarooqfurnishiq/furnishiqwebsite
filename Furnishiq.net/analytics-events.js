// Shared GTM dataLayer event tracking for key conversion actions.
// Runs on every page (loaded alongside support.js / nav-mobile.js / floating-buttons.js).
(function () {
  window.dataLayer = window.dataLayer || [];

  // "Book Free Consultation" — nav CTA on every page (.fiq-nav-cta / .fiq-nav-cta-btn)
  // plus the standalone CTA button on the portfolio page (#id-cta-btn).
  document.addEventListener('click', function (e) {
    const el = e.target.closest('.fiq-nav-cta, .fiq-nav-cta-btn, #id-cta-btn');
    if (!el) return;
    window.dataLayer.push({
      event: 'book_consultation_click',
      cta_text: el.textContent.trim(),
      page_path: window.location.pathname,
    });
  }, true);
})();
