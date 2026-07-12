/**
 * The ripple motif as a site-wide visual signature:
 *
 * 1. Scene dividers — a small organic ripple mark (exact same shape
 *    language as the wordmark's ripple, via rippleShape.ts) straddling
 *    each boundary between scenes, easing in as the visitor scrolls
 *    past. Understated by design.
 *
 * 2. Scroll progress — fixed in the bottom-left corner: gently uneven
 *    rings that draw themselves in as the page is scrolled, one ring
 *    per quarter of the journey, with a small gold drop at completion.
 */
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { prefersReducedMotion } from '../scroll';
import { organicRingPath, rippleArcsMarkup, RIPPLE_ARC_VIEWBOX } from './rippleShape';

const DIVIDER_SVG = `
  <svg viewBox="${RIPPLE_ARC_VIEWBOX}" fill="none" aria-hidden="true" focusable="false">
    ${rippleArcsMarkup({ className: 'divider-ring' })}
  </svg>`;

export function initSceneDividers(): void {
  // A divider at every boundary: after scenes 1 through 7.
  for (let i = 1; i <= 7; i++) {
    const scene = document.getElementById(`scene-${i}`);
    if (!scene) continue;

    const divider = document.createElement('div');
    divider.className = 'scene-divider';
    divider.setAttribute('aria-hidden', 'true');
    divider.innerHTML = DIVIDER_SVG;
    scene.appendChild(divider);

    if (prefersReducedMotion()) continue;

    // Rings spread gently outward as the boundary crosses the viewport.
    gsap.fromTo(
      divider.querySelectorAll('.divider-ring'),
      { scale: 0.55, transformOrigin: '50% 0%', opacity: 0 },
      {
        scale: 1,
        opacity: 1,
        ease: 'power1.out',
        stagger: 0.12,
        scrollTrigger: {
          trigger: divider,
          start: 'top 92%',
          end: 'top 55%',
          scrub: true,
        },
      }
    );
  }
}

export function initScrollProgress(): void {
  if (prefersReducedMotion()) return;

  // Uneven spacing, thinner and fainter as the rings expand — the same
  // energy falloff as the wordmark ripple.
  const radii = [7.1, 11.7, 16.8, 22.4];
  const strokeWidths = [1.8, 1.55, 1.3, 1];
  const opacities = [0.95, 0.78, 0.6, 0.42];
  const widget = document.createElement('div');
  widget.className = 'scroll-progress';
  widget.setAttribute('aria-hidden', 'true');
  widget.innerHTML = `
    <svg viewBox="0 0 50 50" fill="none">
      <circle class="progress-drop" cx="25" cy="25" r="3"/>
      ${radii
        .map(
          (r, i) =>
            `<path class="progress-ring" d="${organicRingPath(25, 25, r, 21 + i * 4)}"
               stroke-width="${strokeWidths[i]}" stroke-linecap="round"
               opacity="${opacities[i]}" transform="rotate(-90 25 25)"/>`
        )
        .join('')}
    </svg>`;
  document.body.appendChild(widget);

  const rings = Array.from(widget.querySelectorAll<SVGPathElement>('.progress-ring'));
  const circumferences = rings.map((ring) => ring.getTotalLength());
  rings.forEach((ring, i) => {
    ring.style.strokeDasharray = String(circumferences[i]);
    ring.style.strokeDashoffset = String(circumferences[i]);
  });

  ScrollTrigger.create({
    start: 0,
    end: 'max',
    onUpdate: (self) => {
      rings.forEach((ring, i) => {
        // Ring i draws in across its quarter of the scroll.
        const segment = Math.min(1, Math.max(0, self.progress * rings.length - i));
        ring.style.strokeDashoffset = String(circumferences[i] * (1 - segment));
      });
      widget.classList.toggle('scroll-progress--complete', self.progress > 0.995);
    },
  });
}
