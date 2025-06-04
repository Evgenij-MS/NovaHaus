// service-worker.js
const CACHE_NAME = 'novahaus-cache-v3';
const OFFLINE_URL = '/offline/';

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll([
                '/',
                OFFLINE_URL,
                '/static/css/global.css',
                '/static/js/main.js',
                '/static/images/logo.png',
                '/static/images/favicon/favicon-16x16.png',
                '/static/images/favicon/favicon-32x32.png',
                '/static/images/favicon/favicon-96x96.png',
                '/static/images/favicon/android-chrome-192x192.png',
                '/static/images/favicon/android-chrome-512x512.png',
                '/static/images/favicon/apple-touch-icon.png',
                '/static/images/favicon/favicon.ico',
                '/static/images/favicon/splash.png'
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
