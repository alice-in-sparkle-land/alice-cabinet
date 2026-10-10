/* Alice's Cabinet · Cloudflare Worker
   alicecabinet.com        -> the home page (public)
   www.alicecabinet.com    -> redirects to alicecabinet.com
   trip.alicecabinet.com   -> the Japan trip dashboard (locked by Cloudflare Access)
   Other addresses (like the workers.dev one) show the home page. */
const PAGES = { 'trip.alicecabinet.com': '/japan-trip.html' };
const HOME = '/home.html';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === 'www.alicecabinet.com') return Response.redirect('https://alicecabinet.com' + url.pathname + url.search, 301);
    if (url.pathname === '/' || url.pathname === '/index.html') {
      const page = PAGES[url.hostname] || HOME;
      const r = await env.ASSETS.fetch(new Request(new URL(page, url.origin), request));
      const h = new Headers(r.headers);
      h.set('Cache-Control', 'no-cache');
      return new Response(r.body, { status: r.status, headers: h });
    }
    return env.ASSETS.fetch(request);
  }
};
