#!/usr/bin/env python3
"""Builds public/: the home page (with the header scene inlined) and the Japan trip page."""
import os
R = os.path.dirname(os.path.abspath(__file__))
rd = lambda f: open(os.path.join(R, 'src', f), encoding='utf-8').read()
scene = rd('scene.js').replace("'use strict';\n", '')
home = rd('home.html').replace('/*@SCENE@*/', scene)
sw_reg = "<script>if('serviceWorker' in navigator&&location.protocol==='https:')navigator.serviceWorker.register('/sw.js').catch(function(){});</script>\n</body>"
trip = rd('japan-trip.html')
i = trip.rfind('</body>'); trip = trip[:i] + sw_reg + trip[i + len('</body>'):]
os.makedirs(os.path.join(R, 'public'), exist_ok=True)
open(os.path.join(R, 'public', 'home.html'), 'w', encoding='utf-8').write(home)
open(os.path.join(R, 'public', 'japan-trip.html'), 'w', encoding='utf-8').write(trip)
print('built public/home.html and public/japan-trip.html')
