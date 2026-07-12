/**
 * resonate-cta — privacy-safe WhatsApp redirect.
 *
 * GET /whatsapp?lang=en|pt → 302 to wa.me with a pre-filled message in
 * that language (pt when missing/invalid). The phone number never
 * appears in the site or this repo; it lives only in the WHATSAPP_NUMBER
 * secret, set after deploy with:
 *
 *   npx wrangler secret put WHATSAPP_NUMBER
 *
 * Basic abuse protection: the Referer must be the Resonate site (or a
 * WhatsApp-owned host, so the redirect still works if WhatsApp itself
 * re-requests it); anything else is bounced back to the site instead.
 */

interface Env {
  WHATSAPP_NUMBER?: string;
}

const SITE_URL = 'https://farfromtimnah-hue.github.io/resonate-website/';

const ALLOWED_REFERRER_HOSTS = ['farfromtimnah-hue.github.io', 'resonateai.online'];

const MESSAGES = {
  en: 'Hi Nicole, how are you? I loved what I saw on your site and would love to see how you could help me with my business.',
  pt: 'Oi Nicole, tudo bem? Amei o que vi no seu site e adoraria ver como você pode me ajudar no meu negócio.',
} as const;

function refererAllowed(request: Request): boolean {
  const referer = request.headers.get('Referer');
  if (!referer) return false;
  try {
    const host = new URL(referer).hostname;
    return ALLOWED_REFERRER_HOSTS.some((d) => host === d || host.endsWith(`.${d}`));
  } catch {
    return false;
  }
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    if (request.method !== 'GET' || url.pathname !== '/whatsapp') {
      return new Response('Not found', { status: 404 });
    }

    if (!refererAllowed(request)) {
      return Response.redirect(SITE_URL, 302);
    }

    const number = env.WHATSAPP_NUMBER;
    if (!number) {
      // Secret not set yet — fail soft toward the site rather than a 500.
      return Response.redirect(SITE_URL, 302);
    }

    const lang = url.searchParams.get('lang') === 'en' ? 'en' : 'pt';
    const target = `https://wa.me/${encodeURIComponent(number)}?text=${encodeURIComponent(MESSAGES[lang])}`;
    return new Response(null, {
      status: 302,
      headers: {
        Location: target,
        'Cache-Control': 'no-store',
      },
    });
  },
};
