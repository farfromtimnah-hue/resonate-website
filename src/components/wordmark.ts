/**
 * Placeholder Resonate wordmark — one isolated component so the final
 * logo can replace it later without touching layout.
 *
 * The word "Resonate" is the brand name in both languages; it is never
 * translated. Fill is deep water blue with a subtle gold sheen at the
 * very top edge of the letters (light on water). Beneath, a ripple
 * mark: organic rings widening downward, thinning and fading as they
 * spread — shape language shared with every other ripple on the site
 * (see rippleShape.ts).
 */
import { rippleArcsMarkup, RIPPLE_ARC_VIEWBOX } from './rippleShape';

export function createWordmark(size: 'hero' | 'small' = 'hero'): HTMLElement {
  const el = document.createElement('div');
  el.className = `wordmark wordmark--${size}`;
  el.innerHTML = `
    <span class="wordmark__word">Resonate</span>
    <svg class="wordmark__ripple" viewBox="${RIPPLE_ARC_VIEWBOX}" fill="none"
         aria-hidden="true" focusable="false">
      ${rippleArcsMarkup({
        fills: ['var(--c-mid)', 'var(--c-mid)', 'var(--c-ripple)', 'var(--c-ripple)'],
      })}
    </svg>
  `;
  return el;
}
