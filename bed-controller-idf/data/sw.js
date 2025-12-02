const CACHE_NAME = 'homeyantric-v3';
const ASSETS = [
  '/',
  '/index.html',
  '/style.css',
  '/app.js',
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
  event.respondWith(
    caches.match(event.request).then((response) => response || fetch(event.request))
  );
});
