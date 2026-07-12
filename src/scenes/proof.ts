/**
 * Scene 7 — the proof. Each build's pre-rendered device video (HyperFrames)
 * sits in a sticky-pinned container; it lazy-loads near the viewport and
 * plays while its block is on screen.
 *
 * If a video fails to load, the block falls back to its static screenshots:
 * a GSAP cross-fade cycle with a slow Ken Burns drift, inside a simple
 * framed card — the scene reads completely either way.
 */
import gsap from 'gsap';
import { prefersReducedMotion } from '../scroll';

export function initProofScenes(): void {
  document.querySelectorAll<HTMLElement>('.proof-media').forEach((media) => {
    const video = media.querySelector<HTMLVideoElement>('.proof-video');
    const fallback = media.querySelector<HTMLElement>('.proof-fallback');
    if (!video) return;

    // Timed HTML overlays (chips + beat labels) synced to the video clock,
    // so the text stays live (language toggle) while icons live in the video.
    const cues = Array.from(media.querySelectorAll<HTMLElement>('.proof-cue'));
    video.addEventListener('timeupdate', () => {
      const t = video.currentTime;
      cues.forEach((cue) => {
        const start = Number(cue.dataset.cueStart);
        const end = Number(cue.dataset.cueEnd);
        cue.classList.toggle('is-on', t >= start && t < end);
      });
    });

    if (prefersReducedMotion()) {
      // Static page: show the first screenshot, skip video entirely.
      video.remove();
      if (fallback) {
        fallback.hidden = false;
        loadFallbackImages(fallback);
      }
      return;
    }

    const src = `${import.meta.env.BASE_URL}${video.dataset.src}`;

    video.addEventListener(
      'error',
      () => {
        video.remove();
        media.classList.add('is-fallback');
        if (fallback) activateFallback(fallback);
      },
      { once: true }
    );

    // Lazy-load near the viewport; play/pause with visibility. The play
    // trigger can fire before the src is attached, so re-attempt playback
    // once data arrives while the block is still on screen.
    let visible = false;
    const tryPlay = () => {
      if (visible && video.isConnected) {
        video.play().catch(() => {
          /* autoplay refused — poster frame remains */
        });
      }
    };

    video.addEventListener('loadeddata', tryPlay);

    const loader = new IntersectionObserver(
      (entries) => {
        if (!entries.some((e) => e.isIntersecting)) return;
        loader.disconnect();
        video.preload = 'auto';
        video.src = src;
      },
      { rootMargin: '75% 0px' }
    );
    loader.observe(media);

    const player = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          visible = e.isIntersecting;
          if (!video.isConnected) return;
          if (visible) tryPlay();
          else video.pause();
        });
      },
      { threshold: 0.25 }
    );
    player.observe(media);
  });
}

function loadFallbackImages(fallback: HTMLElement): void {
  fallback.querySelectorAll<HTMLImageElement>('img[data-src]').forEach((img) => {
    img.src = `${import.meta.env.BASE_URL}images/proof/${img.dataset.src?.split('/').pop()}`;
    img.loading = 'lazy';
  });
}

function activateFallback(fallback: HTMLElement): void {
  fallback.hidden = false;
  loadFallbackImages(fallback);

  const imgs = Array.from(fallback.querySelectorAll<HTMLImageElement>('img'));
  if (imgs.length < 2) return;

  const HOLD = 2.5;
  const FADE = 0.6;
  const tl = gsap.timeline({ repeat: -1, repeatDelay: HOLD });

  imgs.forEach((img, i) => {
    // Slow Ken Burns drift while each image is frontmost.
    gsap.fromTo(
      img,
      { scale: 1 },
      {
        scale: 1.05,
        duration: HOLD + FADE,
        ease: 'sine.inOut',
        repeat: -1,
        repeatDelay: (imgs.length - 1) * (HOLD + FADE),
        delay: i * (HOLD + FADE),
      }
    );
    if (i === 0) return;
    tl.to(img, { opacity: 1, duration: FADE, ease: 'power1.inOut' }, i * (HOLD + FADE) - FADE);
  });
  // Cycle back to the first image at the end of each loop.
  tl.to(imgs.slice(1), { opacity: 0, duration: FADE, ease: 'power1.inOut' });
}
