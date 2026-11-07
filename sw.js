// Service worker: cache-first para la app, network-first para el calendario JSON.
const VERSION = 'marcador-v8';
const FILES = ['./', './index.html', './manifest.webmanifest', './calendario/salesianos_alevin.json', './icons/icon-192.png', './icons/icon-512.png', './icons/icon-maskable-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  if (e.request.url.includes('salesianos_alevin.json')) {
    e.respondWith(
      fetch(e.request).then(r => {
        const copy = r.clone(); caches.open(VERSION).then(c => c.put('./calendario/salesianos_alevin.json', copy)); return r;
      }).catch(() => caches.match('./calendario/salesianos_alevin.json'))
    );
    return;
  }
  e.respondWith(
    caches.match(e.request, { ignoreSearch: true }).then(hit => hit || fetch(e.request).then(r => {
      const copy = r.clone(); caches.open(VERSION).then(c => c.put(e.request, copy)); return r;
    }).catch(() => caches.match('./index.html')))
  );
});
