self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('nova-haus-cache').then((cache) => {
            return cache.addAll([
                '/',
                '/static/css/global.css',
                '/static/js/scripts.js',
            ]);
        })
    );
});