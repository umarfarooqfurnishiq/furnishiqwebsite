// Shared floating action buttons: WhatsApp (always visible, bottom-left)
// and Back to Top (appears after scroll, bottom-right). Self-contained —
// builds its own DOM, no per-page wiring needed beyond the <script> tag.
(function () {
  if (window.__fiqFloatingButtonsInit) return;
  window.__fiqFloatingButtonsInit = true;

  var WA_NUMBER = '966580330627';
  var WA_TEXT_EN = 'Hello FurnishIQ, I would like to know more about your design and fit-out services.';
  var WA_TEXT_AR = 'مرحباً FurnishIQ، أود معرفة المزيد عن خدمات التصميم والتشطيبات لديكم.';
  var WA_TEXT = encodeURIComponent(document.documentElement.lang === 'ar' ? WA_TEXT_AR : WA_TEXT_EN);
  var WA_ARIA = document.documentElement.lang === 'ar' ? 'الدردشة عبر واتساب' : 'Chat on WhatsApp';
  var TOP_ARIA = document.documentElement.lang === 'ar' ? 'العودة إلى الأعلى' : 'Back to top';

  function injectStyle() {
    var css = [
      '.fiq-float-btn{position:fixed;bottom:24px;width:52px;height:52px;display:flex;align-items:center;justify-content:center;background:#D6C2A8;box-shadow:0 4px 20px rgba(58,45,37,0.18);text-decoration:none;z-index:220;transition:opacity 0.4s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.4s cubic-bezier(0.25,0.46,0.45,0.94),background 0.25s;}',
      '.fiq-float-wa{left:24px;color:#3A2D25;}',
      '.fiq-float-wa:hover{background:#c9b192;}',
      '.fiq-float-top{right:24px;background:#1F1F1F;color:#D6C2A8;border:0;cursor:pointer;opacity:0;pointer-events:none;transform:translateY(12px);}',
      '.fiq-float-top:hover{background:#3A2D25;}',
      '.fiq-float-top--visible{opacity:1;pointer-events:auto;transform:translateY(0);}',
      '@media(max-width:600px){.fiq-float-btn{width:46px;height:46px;bottom:16px;}.fiq-float-wa{left:16px;}.fiq-float-top{right:16px;}}',
      '@media(prefers-reduced-motion:reduce){.fiq-float-btn{transition:none!important;}}'
    ].join('');
    var styleEl = document.createElement('style');
    styleEl.setAttribute('data-fiq-floating-buttons', '');
    styleEl.textContent = css;
    document.head.appendChild(styleEl);
  }

  function init() {
    injectStyle();

    var wa = document.createElement('a');
    wa.className = 'fiq-float-btn fiq-float-wa';
    wa.href = 'https://wa.me/' + WA_NUMBER + '?text=' + WA_TEXT;
    wa.target = '_blank';
    wa.rel = 'noopener noreferrer';
    wa.setAttribute('aria-label', WA_ARIA);
    wa.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19l1.4-4.2A7.5 7.5 0 1 1 8.7 18Z"/></svg>';
    document.body.appendChild(wa);

    var top = document.createElement('button');
    top.type = 'button';
    top.className = 'fiq-float-btn fiq-float-top';
    top.setAttribute('aria-label', TOP_ARIA);
    top.innerHTML = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>';
    document.body.appendChild(top);

    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function syncTop() {
      top.classList.toggle('fiq-float-top--visible', window.scrollY > 400);
    }
    requestAnimationFrame(syncTop);
    window.addEventListener('scroll', syncTop, { passive: true });

    top.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
