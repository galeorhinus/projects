const CACHE_NAME = 'homeyantric-__UI_BUILD_TAG__';
const ASSETS = [
  '/', // keep HTML/CSS small set; app.js intentionally not cached to avoid staleness
  '/index.html',
  '/style.css',
  '/bed-visualizer.js',
  '/favicon.png',
  '/manifest.webmanifest',
  '/branding.json'
];

self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)));
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  if (url.pathname.endsWith('.js')) {
    // network-first for JS to avoid stale bundles
    event.respondWith(
      fetch(event.request).then((resp) => resp).catch(() => caches.match(event.request))
    );
  } else {
    event.respondWith(
      caches.match(event.request).then((response) => response || fetch(event.request))
    );
  }
});
