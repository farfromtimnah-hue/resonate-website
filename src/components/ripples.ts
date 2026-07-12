/**
 * The ripple motif as a site-wide visual signature:
 *
 * 1. Scene dividers — a small concentric-arc mark (same family as the
 *    wordmark's ripple) straddling each boundary between scenes, easing
 *    in as the visitor scrolls past. Understated by design.
 *
 * 2. Scroll progress — fixed in the bottom-left corner: concentric
 *    rings that draw themselves in as the page is scrolled, one ring
 *    per quarter of the journey, with a small gold drop at completion.
 */
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { prefersReducedMotion } from '../scroll';

const DIVIDER_SVG = `
  <svg viewBox="0 0 120 34" fill="none" aria-hidden="true" focusable="false">
    <path class="divider-ring" d="M40 6 A 20 14 0 0 0 80 6"
          stroke-width="2.5" stroke-linecap="round" opacity="0.9"/>
    <path class="divider-ring" d="M26 8 A 34 22 0 0 0 94 8"
          stroke-width="2" stroke-linecap="round" opacity="0.5"/>
    <path class="divider-ring" d="M12 10 A 48 30 0 0 0 108 10"
          stroke-width="1.5" stroke-linecap="round" opacity="0.25"/>
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

  const radii = [7, 12, 17, 22];
  const widget = document.createElement('div');
  widget.className = 'scroll-progress';
  widget.setAttribute('aria-hidden', 'true');
  widget.innerHTML = `
    <svg viewBox="0 0 50 50" fill="none">
      <circle class="progress-drop" cx="25" cy="25" r="3"/>
      ${radii
        .map(
          (r) =>
            `<circle class="progress-ring" cx="25" cy="25" r="${r}"
               stroke-width="${r < 20 ? 1.7 : 1.3}" stroke-linecap="round"
               transform="rotate(-90 25 25)"/>`
        )
        .join('')}
    </svg>`;
  document.body.appendChild(widget);

  const rings = Array.from(widget.querySelectorAll<SVGCircleElement>('.progress-ring'));
  const circumferences = radii.map((r) => 2 * Math.PI * r);
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
