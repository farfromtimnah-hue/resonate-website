/**
 * Full-bleed background video slot with a graceful CSS/GSAP fallback.
 *
 * Each slot renders its CSS fallback first and only fades the MP4
 * (sink.mp4, surface-break.mp4, ripple.mp4) in once it actually loads.
 * If the file 404s, the fallback simply remains, so every scene reads
 * complete with or without the clip.
 *
 * Videos are lazy-loaded (IntersectionObserver) and, once loaded, their
 * playback is scrubbed by scroll position via ScrollTrigger.
 */
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { prefersReducedMotion } from '../scroll';

export type FallbackKind = 'sink' | 'surface' | 'ripple';

const RIPPLE_SVG = `
  <svg viewBox="0 0 400 240" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
    <g class="ripple-rings" fill="none" stroke="var(--c-ripple)">
      <ellipse class="ring ring-1" cx="200" cy="120" rx="24" ry="9" stroke-width="2"/>
      <ellipse class="ring ring-2" cx="200" cy="120" rx="70" ry="26" stroke-width="1.5"/>
      <ellipse class="ring ring-3" cx="200" cy="120" rx="130" ry="48" stroke-width="1"/>
      <ellipse class="ring ring-4" cx="200" cy="120" rx="190" ry="70" stroke-width="0.75"/>
    </g>
  </svg>`;

export function mountVideoBg(
  container: HTMLElement,
  file: string,
  kind: FallbackKind
): void {
  const bg = document.createElement('div');
  bg.className = `scene__bg scene__bg--${kind}`;
  bg.setAttribute('aria-hidden', 'true');

  const fallback = document.createElement('div');
  fallback.className = `bg-fallback bg-fallback--${kind}`;
  fallback.innerHTML =
    kind === 'ripple'
      ? RIPPLE_SVG
      : '<div class="bg-fallback__layer bg-fallback__layer--a"></div>' +
        '<div class="bg-fallback__layer bg-fallback__layer--b"></div>';
  bg.appendChild(fallback);
  container.prepend(bg);

  if (prefersReducedMotion()) return; // static fallback only

  animateFallback(fallback, kind, container);
  lazyAttachVideo(bg, file, container);
}

function animateFallback(
  fallback: HTMLElement,
  kind: FallbackKind,
  trigger: HTMLElement
): void {
  const layerA = fallback.querySelector('.bg-fallback__layer--a');
  const layerB = fallback.querySelector('.bg-fallback__layer--b');

  if (kind === 'sink' && layerA && layerB) {
    // Light fading above, depth rising: the shafts of light drift up
    // and dim as the visitor scrolls down — a slow descent.
    gsap.to(layerA, {
      yPercent: -22,
      opacity: 0.25,
      ease: 'none',
      scrollTrigger: { trigger, start: 'top top', end: 'bottom top', scrub: true },
    });
    gsap.to(layerB, {
      yPercent: 12,
      ease: 'none',
      scrollTrigger: { trigger, start: 'top top', end: 'bottom top', scrub: true },
    });
  }

  if (kind === 'surface' && layerA) {
    // The warm gold glow breaks through as the scene is crossed.
    gsap.fromTo(
      layerA,
      { opacity: 0, scale: 0.85 },
      {
        opacity: 1,
        scale: 1.15,
        ease: 'none',
        scrollTrigger: { trigger, start: 'top 80%', end: 'center 45%', scrub: true },
      }
    );
  }
  // ripple: its rings animate via CSS keyframes.
}

function lazyAttachVideo(bg: HTMLElement, file: string, trigger: HTMLElement): void {
  const io = new IntersectionObserver(
    (entries) => {
      if (!entries.some((e) => e.isIntersecting)) return;
      io.disconnect();

      const video = document.createElement('video');
      video.muted = true;
      video.playsInline = true;
      video.preload = 'metadata';
      video.className = 'scene__bg-video';
      video.src = `${import.meta.env.BASE_URL}videos/${file}`;

      video.addEventListener('error', () => video.remove(), { once: true });
      video.addEventListener(
        'loadedmetadata',
        () => {
          gsap.to(video, { opacity: 1, duration: 0.8, ease: 'power1.out' });
          // Scroll position drives playback.
          ScrollTrigger.create({
            trigger,
            start: 'top bottom',
            end: 'bottom top',
            scrub: true,
            onUpdate: (self) => {
              if (video.duration) {
                video.currentTime = self.progress * video.duration;
              }
            },
          });
        },
        { once: true }
      );

      bg.appendChild(video);
    },
    { rootMargin: '50% 0px' }
  );
  io.observe(bg);
}
