/**
 * Smooth scroll (Lenis) + GSAP ScrollTrigger wiring, and the page-wide
 * dark-to-light background arc: submerged dark through scenes 1–2,
 * surfacing into warm light across scene 3, warm and open after.
 *
 * With prefers-reduced-motion, none of this runs — scenes get static
 * backgrounds from CSS (html.reduced-motion) and all content is shown.
 */
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Lenis from 'lenis';

gsap.registerPlugin(ScrollTrigger);

export const prefersReducedMotion = (): boolean =>
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

export let lenis: Lenis | null = null;

export function initScroll(): void {
  if (prefersReducedMotion()) {
    document.documentElement.classList.add('reduced-motion');
    return;
  }

  lenis = new Lenis({
    duration: 1.15,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  });

  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((time) => {
    lenis?.raf(time * 1000);
  });
  gsap.ticker.lagSmoothing(0);

  initBackgroundArc();
}

/**
 * One fixed layer behind all scenes carries the page background color.
 * Scroll across scene 3 scrubs it from deep dark to warm light — the
 * surfacing moment. Scenes themselves stay transparent.
 */
function initBackgroundArc(): void {
  const bg = document.querySelector<HTMLElement>('.bg-arc');
  const pivot = document.querySelector<HTMLElement>('#scene-3');
  if (!bg || !pivot) return;

  gsap.fromTo(
    bg,
    { backgroundColor: '#0a1a2b' },
    {
      backgroundColor: '#f5f2ec',
      ease: 'none',
      scrollTrigger: {
        trigger: pivot,
        start: 'top 60%',
        end: 'bottom 90%',
        scrub: true,
      },
    }
  );

  // Flip a class at the midpoint so components needing a discrete
  // light/dark state (e.g. text colors) can follow the arc.
  ScrollTrigger.create({
    trigger: pivot,
    start: 'center 60%',
    onEnter: () => document.documentElement.classList.add('surfaced'),
    onLeaveBack: () => document.documentElement.classList.remove('surfaced'),
  });
}
