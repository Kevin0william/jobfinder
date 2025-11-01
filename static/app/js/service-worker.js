const CACHE_NAME = "jobfinder-cache-v1";
const urlsToCache = [
    "/", // ta page d'accueil
    // "/static/app/css/style.css",
    "/static/app/manifest.json",
    "/static/app/icons/1.jpg",
    "/static/app/icons/kevin.jpg",
];

// Installation du service worker
self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
        .then(cache => cache.addAll(urlsToCache))
        .then(() => self.skipWaiting())
    );
});

// Activation
self.addEventListener("activate", event => {
    event.waitUntil(
        caches.keys().then(cacheNames =>
            Promise.all(
                cacheNames
                .filter(name => name !== CACHE_NAME)
                .map(name => caches.delete(name))
            )
        )
    );
    self.clients.claim();
});

// Interception des requêtes
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
        .then(response => response || fetch(event.request))
    );
});