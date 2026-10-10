# Alice's Cabinet

- `alicecabinet.com`: the public home page, a cabinet with one drawer per tool.
- `trip.alicecabinet.com`: the Japan trip dashboard.

The other drawers are separate sites with their own repositories:
- Kokoro: `brain-rewire`, at `kokoro.alicecabinet.com`
- The Way: `life-tools`, at `theway.alicecabinet.com`

The tools are locked with Cloudflare Access. The home page stays public.

- `src/home.html`, `src/scene.js` and `src/japan-trip.html` are the sources. Run `python3 build.py` to write `public/`.
- `worker.js` picks the page by address.
- `public/sw.js` lets the pages open offline after the first visit.
- Tests: `node test/routes.mjs`. Screenshots: `python3 test/shots.py`, which needs `wrangler dev --port 8790`.
