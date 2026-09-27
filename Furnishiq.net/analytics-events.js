// Shared GTM dataLayer event tracking for key conversion actions.
// Runs on every page (loaded alongside support.js / nav-mobile.js / floating-buttons.js).
(function () {
  window.dataLayer = window.dataLayer || [];

  // Custom page-view event — fires once per page load. Every FurnishIQ page is a
  // real full page load (no client-side routing), so this covers every navigation.
  function getPageCategory(pathname) {
    const p = pathname.toLowerCase();
    // Standalone Google Ads landing pages (EN + AR).
    if (p.includes('concept-to-turnkey') || p.includes('landing-turnkey')) return 'landing';
    if (p.includes('contact')) return 'contact';
    if (p.includes('about-us')) return 'about';
    if (p.includes('single-post')) return 'blog_post';
    if (p.includes('blog')) return 'blog';
    if (p.includes('project-detail')) return 'portfolio_detail';
    if (p.includes('portfolio')) return 'portfolio';
    if (p.includes('services-')) return 'services';
    if (p === '/' || p === '/en' || p === '/ar' || p.includes('home')) return 'home';
    return 'other';
  }
  window.dataLayer.push({
    event: 'page_view_data',
    page_category: getPageCategory(window.location.pathname),
    page_language: document.documentElement.lang || 'en',
    page_path: window.location.pathname,
  });

  // "Book Free Consultation" — nav CTA on every page (.fiq-nav-cta / .fiq-nav-cta-btn)
  // plus the standalone CTA button on the portfolio page (#id-cta-btn).
  document.addEventListener('click', function (e) {
    // Landing pages add their own consultation CTAs: hero, package, video, mobile menu, and the
    // project / service pop-ups (built by script, so matched by their data attributes).
    const el = e.target.closest('.fiq-nav-cta, .fiq-nav-cta-btn, #id-cta-btn, .fiq-nav-overlay-cta, .fiq-hero-cta-primary, .fiq-svc-cta, .fiq-vid-btn-primary, [data-pm-cta], [data-sm-cta]');
    if (!el) return;
    const section = el.closest('section');
    window.dataLayer.push({
      event: 'book_consultation_click',
      cta_text: el.textContent.trim(),
      cta_location: el.closest('.fiq-smodal') ? 'service_popup'
        : el.closest('.fiq-pmodal') ? 'project_popup'
        : el.closest('.fiq-nav-overlay') ? 'mobile_menu'
        : el.closest('nav') ? 'nav'
        : section ? section.id || 'section' : 'other',
      page_path: window.location.pathname,
    });
  }, true);

  // WhatsApp — the floating button (every page) and any in-page wa.me link/button.
  document.addEventListener('click', function (e) {
    const el = e.target.closest('a[href^="https://wa.me/"]');
    if (!el) return;
    window.dataLayer.push({
      event: 'whatsapp_click',
      link_id: el.id || null,
      page_path: window.location.pathname,
    });
  }, true);

  // Call — any tel: link (in-page call buttons and the footer phone number).
  document.addEventListener('click', function (e) {
    const el = e.target.closest('a[href^="tel:"]');
    if (!el) return;
    window.dataLayer.push({
      event: 'call_click',
      link_id: el.id || null,
      page_path: window.location.pathname,
    });
  }, true);
})();
