const CACHE_NAME = 'homeyantric-__UI_BUILD_TAG__';
const ASSETS = [
  '/',
  '/index.html',
  '/style.css',
  '/bed-visualizer.js',
  '/favicon.png',
  '/manifest.webmanifest',
  '/branding.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  if (url.pathname.endsWith('.js')) {
    // network-first for JS to avoid stale bundles
    event.respondWith(
      fetch(event.request).then((resp) => {
        return resp;
      }).catch(() => caches.match(event.request))
    );
  } else {
    event.respondWith(
      caches.match(event.request).then((response) => response || fetch(event.request))
    );
  }
});
