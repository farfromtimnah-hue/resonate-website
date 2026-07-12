/**
 * Placeholder Resonate wordmark — one isolated component so the final
 * logo can replace it later without touching layout.
 *
 * The word "Resonate" is the brand name in both languages; it is never
 * translated. Fill is deep water blue with a subtle gold sheen at the
 * very top edge of the letters (light on water). Beneath, a ripple
 * mark: three concentric arcs widening downward, fading outward.
 */
export function createWordmark(size: 'hero' | 'small' = 'hero'): HTMLElement {
  const el = document.createElement('div');
  el.className = `wordmark wordmark--${size}`;
  el.innerHTML = `
    <span class="wordmark__word">Resonate</span>
    <svg class="wordmark__ripple" viewBox="0 0 120 34" fill="none"
         aria-hidden="true" focusable="false">
      <path d="M40 6 A 20 14 0 0 0 80 6" stroke="var(--c-mid)"
            stroke-width="2.5" stroke-linecap="round" opacity="0.9"/>
      <path d="M26 8 A 34 22 0 0 0 94 8" stroke="var(--c-mid)"
            stroke-width="2" stroke-linecap="round" opacity="0.5"/>
      <path d="M12 10 A 48 30 0 0 0 108 10" stroke="var(--c-ripple)"
            stroke-width="1.5" stroke-linecap="round" opacity="0.25"/>
    </svg>
  `;
  return el;
}
