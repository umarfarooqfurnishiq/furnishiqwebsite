// Shared footer newsletter ("Join the IQ"). The footer form is plain markup on every page,
// so one delegated handler serves all of them, including pages whose template has no
// newsletter state. Records the same `newsletter_subscribe` dataLayer event as before.
(function () {
  if (window.__fiqNewsletterInit) return;
  window.__fiqNewsletterInit = true;

  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form || !form.matches || !form.matches('[data-fiq-newsletter]')) return;
    e.preventDefault();
    var input = form.querySelector('input[type="email"]');
    var email = input ? input.value.trim() : '';
    if (!email || email.indexOf('@') < 1) {
      if (input) input.focus();
      return;
    }
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: 'newsletter_subscribe', page_path: window.location.pathname });
    input.value = '';
    var thanks = form.parentElement && form.parentElement.querySelector('[data-fiq-newsletter-thanks]');
    if (thanks) thanks.style.display = 'block';
  });
})();
