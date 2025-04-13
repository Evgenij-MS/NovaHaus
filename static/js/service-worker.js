const CACHE_NAME = 'novahaus-v1';
const urlsToCache = [
  '/',
  '/static/css/global.css',
  '/static/js/scripts.js',
  '/static/js/slider.js',
  '/static/js/language.js',
  '/static/js/chatbot.js',
  '/static/images/logo.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});