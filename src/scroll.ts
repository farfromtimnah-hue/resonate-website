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
 *
 * Text color is driven by the SAME trigger and the same progress value
 * as the background, never a separate one: the `surfaced` class flips
 * exactly where the interpolated background's luminance crosses the
 * point at which dark text becomes higher-contrast than light text, so
 * text and background brightness stay inversely matched at every
 * scroll position (not just the endpoints).
 */
function initBackgroundArc(): void {
  const bg = document.querySelector<HTMLElement>('.bg-arc');
  const pivot = document.querySelector<HTMLElement>('#scene-3');
  if (!bg || !pivot) return;

  const DEEP = [10, 26, 43]; // --c-deep
  const LIGHT = [245, 242, 236]; // --c-light
  const INK = [18, 40, 63]; // --c-ink, dark text after the flip
  const PALE = LIGHT; // light text before the flip

  const luminance = (rgb: number[]): number => {
    const [r, g, b] = rgb.map((c) => {
      const s = c / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  const contrast = (a: number, b: number): number =>
    (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
  const mixBg = (m: number): number[] =>
    DEEP.map((d, i) => Math.round(d + (LIGHT[i] - d) * m));

  // Solve once for the crossover mix where dark text overtakes light
  // text in contrast against the interpolated background (~0.52).
  let flip = 0.5;
  for (let m = 0; m <= 1; m += 0.005) {
    const bgLum = luminance(mixBg(m));
    if (contrast(luminance(INK), bgLum) >= contrast(luminance(PALE), bgLum)) {
      flip = m;
      break;
    }
  }

  const apply = (progress: number): void => {
    // Smoothstep lingers in the readable extremes and crosses the
    // low-contrast midtones quickly — like breaking a water surface.
    const m = progress * progress * (3 - 2 * progress);
    const [r, g, b] = mixBg(m);
    bg.style.backgroundColor = `rgb(${r} ${g} ${b})`;
    const root = document.documentElement;
    root.classList.toggle('surfaced', m >= flip);
    // Near the crossover both pairings sit at their contrast minimum;
    // CSS adds a faint halo + full opacity to the pivot copy here.
    root.classList.toggle('arc-mid', m > flip - 0.18 && m < flip + 0.18);
  };

  ScrollTrigger.create({
    trigger: pivot,
    start: 'top 60%',
    end: 'bottom 90%',
    onUpdate: (self) => apply(self.progress),
    onRefresh: (self) => apply(self.progress),
  });
}
