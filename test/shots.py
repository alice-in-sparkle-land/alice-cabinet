"""Home page: every theme and time of day, widths, no external requests, Japan page loads."""
import os, sys
from datetime import datetime
from playwright.sync_api import sync_playwright
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots'); os.makedirs(OUT, exist_ok=True)
fails = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for th in ['earth', 'forest', 'sea', 'wind']:
        for ph, hr in [('day', 11), ('dusk', 17), ('night', 22)]:
            ctx = b.new_context(viewport={'width': 412, 'height': 915}, device_scale_factor=2)
            others = [k for k in ['earth', 'forest', 'sea', 'wind'] if k != th]
            # force the theme: Math.random picks index 0 of the pool, so the "last" theme is set to the one before
            ctx.add_init_script("Math.random = () => 0;")
            pg = ctx.new_page(); ext = []; errs = []
            pg.on('request', lambda r: ext.append(r.url) if not r.url.startswith(('http://localhost:8790', 'data:')) else None)
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.clock.install(time=datetime(2026, 10, 10, hr, 5))
            pg.goto('http://localhost:8790/')
            pg.evaluate(f"localStorage.setItem('cab.theme', '{[k for k in ['earth','forest','sea','wind'] if k != th][0] if th != 'earth' else 'forest'}')")
            pg.reload(); pg.wait_for_timeout(250)
            got = pg.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--ac').trim()")
            pg.screenshot(path=f'{OUT}/home_{th}_{ph}.png')
            if ext: fails.append(('external', ext))
            if errs: fails.append(('errors', errs))
            ctx.close()
    ctx = b.new_context(viewport={'width': 360, 'height': 740}); pg = ctx.new_page(); pg.goto('http://localhost:8790/')
    w = pg.evaluate('document.documentElement.scrollWidth')
    if w > 360: fails.append(('scroll360', w))
    links = pg.eval_on_selector_all('a.dr', 'a => a.map(x => x.href)')
    if links != ['https://kokoro.alicecabinet.com/', 'https://theway.alicecabinet.com/', 'https://trip.alicecabinet.com/']: fails.append(('links', links))
    pg.goto('http://localhost:8790/japan-trip.html'); pg.wait_for_timeout(500)
    if 'Japan' not in pg.title(): fails.append(('trip title', pg.title()))
    b.close()
print('FAILS', fails or 'none')
