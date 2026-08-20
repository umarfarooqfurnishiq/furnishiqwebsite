// Shared mobile off-canvas menu (hamburger toggle + overlay).
// Each page calls window.FIQMobileNav(nav) once its own componentDidMount has
// resolved its <nav> element, so this never races the page's own render.
(function () {
  if (window.FIQMobileNav) return;

  var styleInjected = false;
  function injectStyle() {
    if (styleInjected) return;
    styleInjected = true;
    var css = [
      '.fiq-nav-toggle{display:none;position:relative;flex-shrink:0;width:48px;height:48px;padding:0;border:0;background:transparent;cursor:pointer;align-items:center;justify-content:center;z-index:210;}',
      '@media(max-width:960px){.fiq-nav-toggle{display:flex!important;}}',
      '.fiq-nav-toggle span{position:absolute;left:12px;right:12px;height:1.5px;background:#FFFFFF;transition:transform 0.35s cubic-bezier(0.25,0.46,0.45,0.94),opacity 0.25s cubic-bezier(0.25,0.46,0.45,0.94),background 0.3s cubic-bezier(0.25,0.46,0.45,0.94);}',
      '.fiq-nav-toggle span:nth-child(1){top:16px;}',
      '.fiq-nav-toggle span:nth-child(2){top:23px;}',
      '.fiq-nav-toggle span:nth-child(3){top:30px;}',
      '.fiq-nav-toggle--scrolled span{background:#1F1F1F;}',
      '.fiq-nav-toggle--open span:nth-child(1){top:23px;transform:rotate(45deg);}',
      '.fiq-nav-toggle--open span:nth-child(2){opacity:0;}',
      '.fiq-nav-toggle--open span:nth-child(3){top:23px;transform:rotate(-45deg);}',
      '.fiq-nav-overlay{position:fixed;inset:0;z-index:199;background:#1F1F1F;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:32px;opacity:0;pointer-events:none;transform:translateY(-14px);transition:opacity 0.4s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.4s cubic-bezier(0.25,0.46,0.45,0.94);}',
      '.fiq-nav-overlay--open{opacity:1;pointer-events:auto;transform:translateY(0);}',
      '.fiq-nav-overlay-links{display:flex!important;flex-direction:column;align-items:center;gap:28px;}',
      '.fiq-nav-overlay-links a{color:#F5F2ED!important;opacity:1!important;font-size:16px!important;letter-spacing:0.16em!important;}',
      '.fiq-nav-overlay-cta{font-family:"Lama Sans",sans-serif;font-size:12px;letter-spacing:0.18em;text-transform:uppercase;color:#1F1F1F;text-decoration:none;background:#D6C2A8;padding:14px 32px;margin-top:8px;transition:opacity 0.3s cubic-bezier(0.25,0.46,0.45,0.94);}',
      '.fiq-nav-overlay-cta:hover{opacity:0.85;}',
      'body.fiq-nav-open{overflow:hidden;}',
      '@media(prefers-reduced-motion:reduce){.fiq-nav-overlay,.fiq-nav-toggle span{transition:none!important;}}',
      // Services dropdown — desktop: hover/focus reveals a dark panel below the trigger.
      '.fiq-dropdown{position:relative;}',
      '.fiq-dropdown-trigger{font-family:inherit;background:transparent;border:none;padding:0;cursor:default;}',
      '.fiq-dropdown-panel{position:absolute;top:100%;left:50%;transform:translateX(-50%) translateY(8px);margin-top:14px;background:#3A2D25;min-width:220px;padding:12px 0;opacity:0;pointer-events:none;transition:opacity 0.3s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.3s cubic-bezier(0.25,0.46,0.45,0.94);box-shadow:0 24px 80px rgba(58,45,37,0.2);}',
      '.fiq-dropdown:hover .fiq-dropdown-panel,.fiq-dropdown:focus-within .fiq-dropdown-panel{opacity:1;pointer-events:auto;transform:translateX(-50%) translateY(0);}',
      '.fiq-dropdown-panel a{display:block;padding:10px 24px;font-family:"Lama Sans",sans-serif;font-size:11px;letter-spacing:0.14em;text-transform:uppercase;color:#D6C2A8;text-decoration:none;white-space:nowrap;transition:background 0.2s,color 0.2s;}',
      '.fiq-dropdown-panel a:hover{background:rgba(214,194,168,0.08);color:#FFFFFF;}',
      '@media(prefers-reduced-motion:reduce){.fiq-dropdown-panel{transition:none!important;}}',
      // Services dropdown — mobile: no hover, so render the panel inline/expanded in the overlay.
      '@media(max-width:960px){',
      '.fiq-nav-overlay-links .fiq-dropdown{display:flex;flex-direction:column;align-items:center;}',
      '.fiq-nav-overlay-links .fiq-dropdown-trigger{color:#F5F2ED;opacity:0.6;font-size:13px!important;letter-spacing:0.16em;text-transform:uppercase;}',
      '.fiq-nav-overlay-links .fiq-dropdown-panel{position:static;opacity:1!important;pointer-events:auto!important;transform:none!important;background:transparent;box-shadow:none;padding:14px 0 0;margin-top:0;min-width:0;}',
      '.fiq-nav-overlay-links .fiq-dropdown-panel a{font-size:16px!important;padding:8px 0;text-align:center;}',
      '}'
    ].join('');
    var styleEl = document.createElement('style');
    styleEl.setAttribute('data-fiq-nav-mobile', '');
    styleEl.textContent = css;
    document.head.appendChild(styleEl);
  }

  window.FIQMobileNav = function (nav) {
    if (!nav || nav.dataset.fiqMobileNavInit) return;
    nav.dataset.fiqMobileNavInit = '1';
    injectStyle();

    var linksBox = nav.querySelector('.fiq-nav-links');
    var cta = nav.querySelector('a[class*="nav-cta"]');
    if (!linksBox) return;

    var toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'fiq-nav-toggle';
    toggle.setAttribute('aria-label', document.documentElement.lang === 'ar' ? 'فتح القائمة' : 'Open menu');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.innerHTML = '<span></span><span></span><span></span>';
    linksBox.parentElement.appendChild(toggle);

    var overlay = document.createElement('div');
    overlay.className = 'fiq-nav-overlay';
    overlay.setAttribute('aria-hidden', 'true');

    var linksClone = linksBox.cloneNode(true);
    linksClone.className = 'fiq-nav-overlay-links';
    linksClone.removeAttribute('style');
    overlay.appendChild(linksClone);

    if (cta) {
      var ctaClone = cta.cloneNode(true);
      ctaClone.className = 'fiq-nav-overlay-cta';
      ctaClone.removeAttribute('style');
      overlay.appendChild(ctaClone);
    }
    document.body.appendChild(overlay);

    function setScrolledState() {
      toggle.classList.toggle('fiq-nav-toggle--scrolled', window.scrollY > 60);
    }
    setScrolledState();
    window.addEventListener('scroll', setScrolledState, { passive: true });

    function close() {
      overlay.classList.remove('fiq-nav-overlay--open');
      toggle.classList.remove('fiq-nav-toggle--open');
      toggle.setAttribute('aria-expanded', 'false');
      overlay.setAttribute('aria-hidden', 'true');
      document.body.classList.remove('fiq-nav-open');
    }
    function open() {
      overlay.classList.add('fiq-nav-overlay--open');
      toggle.classList.add('fiq-nav-toggle--open');
      toggle.setAttribute('aria-expanded', 'true');
      overlay.setAttribute('aria-hidden', 'false');
      document.body.classList.add('fiq-nav-open');
    }
    toggle.addEventListener('click', function () {
      if (overlay.classList.contains('fiq-nav-overlay--open')) close();
      else open();
    });
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) close();
    });
    Array.prototype.forEach.call(overlay.querySelectorAll('a'), function (a) {
      a.addEventListener('click', close);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 960) close();
    });
  };
})();
