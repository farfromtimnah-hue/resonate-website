/**
 * PT/EN language swap. Portuguese is the default on load.
 *
 * Mechanism: every piece of copy lives in an element carrying both a
 * data-pt and a data-en attribute; the active language is stamped on
 * <html data-lang="..."> and this module swaps the visible text.
 * Elements with [data-lang-only="pt|en"] are shown/hidden by CSS.
 * The choice persists in localStorage. No routing, no URL changes.
 */
export type Lang = 'pt' | 'en';

const STORAGE_KEY = 'resonate-lang';

export function getLang(): Lang {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored === 'en' || stored === 'pt') return stored;
  } catch {
    /* storage unavailable — fall through to default */
  }
  return 'pt';
}

export function setLang(lang: Lang): void {
  document.documentElement.setAttribute('data-lang', lang);
  document.documentElement.setAttribute('lang', lang === 'pt' ? 'pt-BR' : 'en');
  try {
    localStorage.setItem(STORAGE_KEY, lang);
  } catch {
    /* non-fatal */
  }
  applyLang(lang);
  updateToggle(lang);
}

function applyLang(lang: Lang): void {
  document.querySelectorAll<HTMLElement>('[data-pt]').forEach((el) => {
    const text = lang === 'pt' ? el.dataset.pt : el.dataset.en;
    if (text !== undefined) el.textContent = text;
  });
}

function updateToggle(lang: Lang): void {
  document.querySelectorAll<HTMLButtonElement>('.lang-toggle button').forEach((btn) => {
    btn.setAttribute('aria-pressed', String(btn.dataset.setLang === lang));
  });
}

export function initLang(): void {
  const toggle = document.createElement('div');
  toggle.className = 'lang-toggle';
  toggle.setAttribute('role', 'group');
  toggle.setAttribute('aria-label', 'Idioma / Language');
  toggle.innerHTML = `
    <button type="button" data-set-lang="pt" aria-pressed="false" aria-label="Português">PT</button>
    <span class="lang-divider" aria-hidden="true">|</span>
    <button type="button" data-set-lang="en" aria-pressed="false" aria-label="English">EN</button>
  `;
  toggle.addEventListener('click', (e) => {
    const btn = (e.target as HTMLElement).closest<HTMLButtonElement>('button[data-set-lang]');
    if (btn) setLang(btn.dataset.setLang as Lang);
  });
  document.body.appendChild(toggle);
  setLang(getLang());
}
