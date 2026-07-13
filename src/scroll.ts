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

  initScenePins();
  initBackgroundArc();
}

/**
 * Extra scroll distance (in viewport-heights) each scene stays pinned
 * to the viewport before the next scene is allowed to arrive, so its
 * background video and copy can actually be seen and read. Scene 3
 * holds longest: its surface-break clip plays across the pin, and the
 * hold is what makes the break-into-light payoff visible on screen.
 * Scene 7 pins itself per proof block, so it isn't listed here.
 */
const SCENE_HOLDS: Record<string, number> = {
  'scene-1': 0.8,
  'scene-2': 0.8,
  'scene-3': 1.5,
  'scene-4': 0.5,
  'scene-5': 0.5,
  'scene-6': 0.5,
  'scene-8': 0.9,
};

type ProgressFn = (progress: number) => void;
const pinListeners = new Map<string, ProgressFn[]>();

/**
 * Drive something (e.g. scrubbed video playback) from a scene's pinned
 * hold: the callback receives 0→1 across the pin range only, so the
 * driven effect runs entirely while the scene is locked on screen.
 */
export function onScenePinProgress(sceneId: string, fn: ProgressFn): void {
  const list = pinListeners.get(sceneId) ?? [];
  list.push(fn);
  pinListeners.set(sceneId, list);
}

function initScenePins(): void {
  for (const [id, hold] of Object.entries(SCENE_HOLDS)) {
    const scene = document.getElementById(id);
    if (!scene) continue;
    const emit = (self: ScrollTrigger): void => {
      pinListeners.get(id)?.forEach((fn) => fn(self.progress));
    };
    ScrollTrigger.create({
      trigger: scene,
      // Scenes taller than the viewport (e.g. the split cards on small
      // screens) pin once fully scrolled in, not with a clipped bottom.
      start: () =>
        scene.offsetHeight > window.innerHeight + 4 ? 'bottom bottom' : 'top top',
      end: () => `+=${Math.round(window.innerHeight * hold)}`,
      pin: true,
      anticipatePin: 1,
      onUpdate: emit,
      onRefresh: emit,
    });
  }
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
