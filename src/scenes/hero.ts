/**
 * Scenes 1–3: the hook, the ceiling, and the surfacing pivot where the
 * Resonate wordmark is revealed. Also mounts the closing ripple video
 * on scene 8 so all three water-arc backgrounds live in one place.
 */
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { createWordmark } from '../components/wordmark';
import { mountVideoBg } from '../components/videoSlot';
import { prefersReducedMotion } from '../scroll';

export function initHeroScenes(): void {
  // Wordmark always mounts — it is content, not motion.
  const slot = document.getElementById('wordmark-slot');
  if (slot) slot.appendChild(createWordmark('hero'));

  const actSink = document.getElementById('act-sink');
  const scene3 = document.getElementById('scene-3');
  const scene8 = document.getElementById('scene-8');

  // Video slots render CSS/GSAP fallbacks until the MP4s load.
  if (actSink) mountVideoBg(actSink, 'sink.mp4', 'sink');
  if (scene3) mountVideoBg(scene3, 'surface-break.mp4', 'surface');
  if (scene8) mountVideoBg(scene8, 'ripple.mp4', 'ripple');

  if (prefersReducedMotion()) return;

  // Wordmark reveal scrubbed with the surfacing moment.
  if (slot && scene3) {
    gsap.fromTo(
      slot,
      { opacity: 0, y: 36, scale: 0.94 },
      {
        opacity: 1,
        y: 0,
        scale: 1,
        ease: 'power1.out',
        scrollTrigger: {
          trigger: scene3,
          start: 'top 65%',
          end: 'center 50%',
          scrub: true,
        },
      }
    );
    slot.classList.remove('reveal'); // has its own scrubbed reveal
  }
}

/**
 * Generic gentle reveals for all copy across the page: slow fade with a
 * soft rise, no bounce. Runs once per element; skipped entirely under
 * reduced motion so everything is simply visible.
 */
export function initReveals(): void {
  if (prefersReducedMotion()) return;

  document.querySelectorAll<HTMLElement>('.reveal').forEach((el) => {
    const dir = el.dataset.reveal;
    const from: gsap.TweenVars =
      dir === 'left'
        ? { opacity: 0, x: -24 }
        : dir === 'right'
          ? { opacity: 0, x: 24 }
          : { opacity: 0, y: 28 };
    gsap.fromTo(
      el,
      from,
      {
        opacity: 1,
        x: 0,
        y: 0,
        duration: 1.1,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: el,
          start: 'top 82%',
          toggleActions: 'play none none reverse',
        },
      }
    );
  });

  ScrollTrigger.refresh();
}
