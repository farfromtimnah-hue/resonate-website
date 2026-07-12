/**
 * Organic ripple geometry — the single source of the site's ripple
 * shape language, shared by the wordmark, scene dividers, and the
 * scroll-progress rings.
 *
 * Real ripples are not perfect concentric arcs: each ring wavers
 * slightly, loses weight as it travels outward, and the spacing
 * between rings drifts. These generators bake that in deterministically
 * (seeded sine wobble, no randomness) so every render is identical:
 *
 * - `organicArcPath` — a downward half-ripple drawn as a FILLED shape
 *   whose width swells at the crest and thins to the tips, with a
 *   subtle radial waver. Used by the wordmark and scene dividers.
 * - `organicRingPath` — a closed ring with the same gentle waver,
 *   stroked so it can still draw itself in via dash offset. Used by
 *   the scroll-progress indicator.
 */

const TAU = Math.PI * 2;

/** Smooth periodic waver in [-1, 1]; periodic in t so rings close cleanly. */
function waver(seed: number, t: number): number {
  return (
    Math.sin(TAU * 2 * t + seed * 12.9898) * 0.5 +
    Math.sin(TAU * 3 * t + seed * 78.233) * 0.33 +
    Math.sin(TAU * 5 * t + seed * 37.719) * 0.17
  );
}

const fmt = (n: number): string => String(Math.round(n * 100) / 100);

export interface RippleArcSpec {
  cx: number;
  cy: number;
  rx: number;
  ry: number;
  /** Peak stroke weight at the crest; the tips thin to ~a third of it. */
  width: number;
  seed: number;
  opacity: number;
}

/** Filled tapered half-ripple bulging downward from (cx±rx, cy). */
export function organicArcPath(spec: RippleArcSpec): string {
  const { cx, cy, rx, ry, width, seed } = spec;
  const N = 40;
  const pts: Array<[number, number]> = [];
  const widths: number[] = [];

  for (let i = 0; i <= N; i++) {
    const t = i / N;
    const a = Math.PI * (1 - t); // left tip → crest → right tip
    const wob = 1 + 0.028 * waver(seed, t);
    pts.push([cx + rx * wob * Math.cos(a), cy + ry * wob * Math.sin(a)]);
    // Heavier at the crest, thinning toward both tips, never uniform.
    widths.push(
      width * (0.32 + 0.68 * Math.sin(Math.PI * t)) * (1 + 0.14 * waver(seed + 5, t))
    );
  }

  const outer: string[] = [];
  const inner: string[] = [];
  for (let i = 0; i <= N; i++) {
    const prev = pts[Math.max(0, i - 1)];
    const next = pts[Math.min(N, i + 1)];
    const tx = next[0] - prev[0];
    const ty = next[1] - prev[1];
    const len = Math.hypot(tx, ty) || 1;
    const nx = -ty / len;
    const ny = tx / len;
    const h = widths[i] / 2;
    outer.push(`${fmt(pts[i][0] + nx * h)} ${fmt(pts[i][1] + ny * h)}`);
    inner.push(`${fmt(pts[i][0] - nx * h)} ${fmt(pts[i][1] - ny * h)}`);
  }
  inner.reverse();
  return `M${outer.join(' L')} L${inner.join(' L')} Z`;
}

/** Closed near-circular ring with a subtle waver; meant to be stroked. */
export function organicRingPath(cx: number, cy: number, r: number, seed: number): string {
  const N = 72;
  const cmds: string[] = [];
  for (let i = 0; i < N; i++) {
    const t = i / N;
    const a = TAU * t;
    const rr = r * (1 + 0.02 * waver(seed, t));
    cmds.push(`${fmt(cx + rr * Math.cos(a))} ${fmt(cy + rr * Math.sin(a))}`);
  }
  return `M${cmds.join(' L')} Z`;
}

export const RIPPLE_ARC_VIEWBOX = '0 0 120 40';

/**
 * The canonical ripple mark: four rings widening downward with uneven
 * spacing, each lighter and fainter than the last as the energy fades.
 */
const ARC_SPECS: RippleArcSpec[] = [
  { cx: 60, cy: 5, rx: 20, ry: 13, width: 2.6, seed: 3, opacity: 0.92 },
  { cx: 60.6, cy: 6.5, rx: 32.5, ry: 19.5, width: 1.9, seed: 7, opacity: 0.55 },
  { cx: 59.4, cy: 8, rx: 48.5, ry: 26, width: 1.3, seed: 11, opacity: 0.3 },
  { cx: 60.2, cy: 9, rx: 57.5, ry: 29.5, width: 0.85, seed: 17, opacity: 0.14 },
];

/** Inner SVG markup for the ripple mark (paths only, no <svg> wrapper). */
export function rippleArcsMarkup(opts: { className?: string; fills?: string[] } = {}): string {
  const { className = 'ripple-arc', fills } = opts;
  return ARC_SPECS.map((spec, i) => {
    const fill = fills?.[Math.min(i, (fills?.length ?? 1) - 1)] ?? 'currentColor';
    return `<path class="${className}" d="${organicArcPath(spec)}" fill="${fill}" opacity="${spec.opacity}"/>`;
  }).join('\n    ');
}
