const CACHE_NAME = "jobfinder-cache-v1";
const urlsToCache = [
    "/", // index
    "/inscription/", // page d'inscription
    "/connexion/", // page de connexion
    "/accueil/", // page d'accueil
    "/deconnexion/", // déconnexion
    "/creation_offre/", // création d'offre
    "/produit/", // liste des produits
    "/creation_produit/", // création produit
    "/user_list/", // liste des utilisateurs
    "/profil/", // profil
    "/notification/", // notifications
    "/notif_all/", // toutes notifications
    "/add_page/", // ajout page
    "/boost_page/", // boost page
    "/options_avance/", // options avancées
    "/static/app/manifest.json",
    "/static/app/icons/jobfinder.jpg",
    // ajoute ici tous tes fichiers CSS/JS
];

// INSTALL
self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(urlsToCache);
        }).then(() => self.skipWaiting())
    );
});

// ACTIVATE
self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames
                .filter((name) => name !== CACHE_NAME)
                .map((name) => caches.delete(name))
            );
        }).then(() => self.clients.claim())
    );
});

// FETCH avec mise à jour automatique
self.addEventListener("fetch", (event) => {
    // On ignore les requêtes qui ne sont pas GET
    if (event.request.method !== "GET") return;

    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            const fetchPromise = fetch(event.request)
                .then((networkResponse) => {
                    // Met à jour le cache seulement si la réponse est valide
                    if (networkResponse && networkResponse.status === 200) {
                        caches.open(CACHE_NAME).then((cache) => {
                            cache.put(event.request, networkResponse.clone());
                        });
                    }
                    return networkResponse;
                })
                .catch(() => {
                    // Si réseau indisponible, on renvoie le cache
                    return cachedResponse;
                });

            // On renvoie soit le cache immédiatement, soit la réponse réseau
            return cachedResponse || fetchPromise;
        })
    );
});