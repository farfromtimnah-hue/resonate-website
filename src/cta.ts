/**
 * Scene 8 CTA → WhatsApp, via the resonate-cta Worker so the phone
 * number never appears in this repo or the shipped bundle.
 *
 * The lang param is read from <html data-lang> — the exact state the
 * PT|EN toggle maintains (see lang.ts) — and it is re-read on every
 * click, so a toggle flipped after page load is always respected.
 */
const CTA_ENDPOINT = 'https://resonate-cta.farfromtimnah.workers.dev/whatsapp';

function ctaHref(): string {
  const lang = document.documentElement.getAttribute('data-lang') === 'en' ? 'en' : 'pt';
  return `${CTA_ENDPOINT}?lang=${lang}`;
}

export function initCta(): void {
  const button = document.querySelector<HTMLAnchorElement>('.cta-button');
  if (!button) return;
  button.href = ctaHref();
  // Refresh synchronously on click (and middle-click/ctrl-click via
  // auxclick) so navigation always carries the current toggle state.
  const refresh = (): void => {
    button.href = ctaHref();
  };
  button.addEventListener('click', refresh);
  button.addEventListener('auxclick', refresh);
  button.addEventListener('contextmenu', refresh);
}
