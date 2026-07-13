/**
 * Placeholder Resonate wordmark — one isolated component so the final
 * logo can replace it later without touching layout. Kept deliberately
 * bare (just the word, no marks) until the finished logo drops in.
 *
 * The word "Resonate" is the brand name in both languages; it is never
 * translated. Fill is deep water blue with a subtle gold sheen at the
 * very top edge of the letters (light on water).
 */
export function createWordmark(size: 'hero' | 'small' = 'hero'): HTMLElement {
  const el = document.createElement('div');
  el.className = `wordmark wordmark--${size}`;
  el.innerHTML = `<span class="wordmark__word">Resonate</span>`;
  return el;
}
