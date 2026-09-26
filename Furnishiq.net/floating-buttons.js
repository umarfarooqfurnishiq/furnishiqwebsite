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
  // Opt-in per page: <script src="./floating-buttons.js" data-wa-style="official" defer>
  // shows WhatsApp's own round green button instead of the brand sand square.
  var WA_OFFICIAL = !!(document.currentScript && document.currentScript.getAttribute('data-wa-style') === 'official');
  var WA_LOGO = '<svg width="30" height="30" viewBox="0 0 24 24" fill="#FFFFFF" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>';

  function injectStyle() {
    var css = [
      '.fiq-float-btn{position:fixed;bottom:24px;width:52px;height:52px;display:flex;align-items:center;justify-content:center;background:#D6C2A8;box-shadow:0 4px 20px rgba(58,45,37,0.18);text-decoration:none;z-index:220;transition:opacity 0.4s cubic-bezier(0.25,0.46,0.45,0.94),transform 0.4s cubic-bezier(0.25,0.46,0.45,0.94),background 0.25s;}',
      '.fiq-float-wa{left:24px;color:#3A2D25;}',
      '.fiq-float-wa:hover{background:#c9b192;}',
      '.fiq-float-top{right:24px;background:#1F1F1F;color:#D6C2A8;border:0;cursor:pointer;opacity:0;pointer-events:none;transform:translateY(12px);}',
      '.fiq-float-top:hover{background:#3A2D25;}',
      '.fiq-float-top--visible{opacity:1;pointer-events:auto;transform:translateY(0);}',
      '.fiq-float-wa--official{width:56px;height:56px;border-radius:50%;background:#25D366;box-shadow:0 6px 20px rgba(0,0,0,0.25);}',
      '.fiq-float-wa--official:hover{background:#1EBE5A;transform:scale(1.05);}',
      // Back-to-top matches the round WhatsApp button on opted-in pages, and lifts on hover.
      '.fiq-float-top--round{width:56px;height:56px;border-radius:50%;box-shadow:0 6px 20px rgba(0,0,0,0.25);}',
      '.fiq-float-top--round.fiq-float-top--visible:hover{transform:translateY(-4px);box-shadow:0 10px 24px rgba(0,0,0,0.3);}',
      '@media(max-width:600px){.fiq-float-btn{width:46px;height:46px;bottom:16px;}.fiq-float-wa{left:16px;}.fiq-float-top{right:16px;}.fiq-float-wa--official,.fiq-float-top--round{width:52px;height:52px;}}',
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
    wa.className = 'fiq-float-btn fiq-float-wa' + (WA_OFFICIAL ? ' fiq-float-wa--official' : '');
    wa.href = 'https://wa.me/' + WA_NUMBER + '?text=' + WA_TEXT;
    wa.target = '_blank';
    wa.rel = 'noopener noreferrer';
    wa.setAttribute('aria-label', WA_ARIA);
    wa.innerHTML = WA_OFFICIAL ? WA_LOGO : '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19l1.4-4.2A7.5 7.5 0 1 1 8.7 18Z"/></svg>';
    document.body.appendChild(wa);

    var top = document.createElement('button');
    top.type = 'button';
    top.className = 'fiq-float-btn fiq-float-top' + (WA_OFFICIAL ? ' fiq-float-top--round' : '');
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
