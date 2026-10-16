#!/usr/bin/env python3
"""Build the iPhone app packages from ../notebook.html.

  pwa/                    : web app to host anywhere over HTTPS, then Safari > Share > Add to Home Screen
  capacitor/www/          : same files, bundled into the native iOS app (Capacitor)
  mjg-todo-pwa.zip        : pwa/ zipped for drag-and-drop hosting (e.g. Netlify Drop)

Run again after every change to notebook.html:  python3 build_app.py
"""
import pathlib, shutil, zipfile, hashlib

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent / 'notebook.html'
PWA = HERE / 'pwa'
WWW = HERE / 'capacitor' / 'www'
NAME, SHORT = '하고 싶은 일 목록', '하고 싶은 일'

body = SRC.read_text(encoding='utf-8')
version = hashlib.sha1(body.encode()).hexdigest()[:10]

head = f'''<!doctype html>
<html lang="ko"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#FBE9EC">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="{SHORT}">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/icon-180.png">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<style>html,body{{height:100%}}:root{{padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}}body{{margin:0;-webkit-user-select:none;user-select:none}}input,.text{{-webkit-user-select:text;user-select:text}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head><body>
'''
tail = f'''
<script>
// Offline support when served over http(s); the native (Capacitor) app ships its files already.
if ('serviceWorker' in navigator && /^https?:$/.test(location.protocol)) {{
  navigator.serviceWorker.register('sw.js').catch(() => {{}});
}}
</script>
</body></html>
'''
manifest = f'''{{
  "name": "{NAME}",
  "short_name": "{SHORT}",
  "lang": "ko",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "background_color": "#FBE9EC",
  "theme_color": "#FBE9EC",
  "icons": [
    {{ "src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png" }},
    {{ "src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png" }},
    {{ "src": "icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }}
  ]
}}
'''
sw = f'''// Cache the app shell so it opens without a connection. Bumped on every build.
const CACHE = 'mjg-todo-{version}';
const SHELL = ['./', 'index.html', 'manifest.webmanifest', 'icons/icon-180.png', 'icons/icon-192.png', 'icons/icon-512.png'];
self.addEventListener('install', e => {{
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
}});
self.addEventListener('activate', e => {{
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
}});
self.addEventListener('fetch', e => {{
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin === location.origin) {{
    // network first for the page itself so updates arrive, cache as fallback
    if (req.mode === 'navigate') {{
      e.respondWith(fetch(req).then(r => {{ caches.open(CACHE).then(c => c.put('index.html', r.clone())); return r; }}).catch(() => caches.match('index.html')));
      return;
    }}
    e.respondWith(caches.match(req).then(hit => hit || fetch(req)));
  }} else if (/fonts\\.(googleapis|gstatic)\\.com$/.test(url.hostname)) {{
    e.respondWith(caches.open(CACHE).then(c => c.match(req).then(hit => {{
      const net = fetch(req).then(r => {{ c.put(req, r.clone()); return r; }}).catch(() => hit);
      return hit || net;
    }})));
  }}
}});
'''

PWA.mkdir(exist_ok=True)
(PWA / 'index.html').write_text(head + body + tail, encoding='utf-8')
(PWA / 'manifest.webmanifest').write_text(manifest, encoding='utf-8')
(PWA / 'sw.js').write_text(sw, encoding='utf-8')

if WWW.parent.exists():
    if WWW.exists(): shutil.rmtree(WWW)
    shutil.copytree(PWA, WWW)

with zipfile.ZipFile(HERE / 'mjg-todo-pwa.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for f in sorted(PWA.rglob('*')):
        if f.is_file(): z.write(f, f.relative_to(PWA))
print('built', version, '->', PWA, WWW if WWW.exists() else '(no capacitor/)')
