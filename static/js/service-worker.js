// service-worker.js (обновлённый)
const CACHE_NAME = 'novahaus-cache-v2';
const OFFLINE_URL = '/offline/';

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll([
                '/',
                OFFLINE_URL,
                'static/css/global.css',
                'static/js/main.js',
                'static/images/logo.webp',
                'static/images/favicon/favicon-192x192.webp'
            ]))
    );
});

self.addEventListener('fetch', event => {
    if (event.request.mode === 'navigate') {
        event.respondWith(
            fetch(event.request).catch(() => caches.match(OFFLINE_URL))
        );
    } else {
        event.respondWith(
            caches.match(event.request).then(response => response || fetch(event.request))
        );
    }
});