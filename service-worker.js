const CACHE_NAME = 'mon-cache-v1';
const urlsToCache = [
  '/',
  '/offline.html',
  '/static/img/pagne1.jpg',
  '/static/img/pagne2.png',
  '/static/img/pagne3.jpg',
  '/static/img/aboya_img.jpg',
  '/static/img/icons/icon-192.png',
  '/static/img/icons/icon-512.png'
];

// Installation : mise en cache initiale
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
      .then(() => self.skipWaiting())
  );
});

// Activation : suppression des anciens caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(key => key !== CACHE_NAME)
            .map(key => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

// Interception des requêtes
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(cachedResponse => {
      // Si la ressource est en cache, on la renvoie directement
      if (cachedResponse) {
        return cachedResponse;
      }
      // Sinon, on fait la requête réseau
      return fetch(event.request).catch(() => {
        // En cas d'échec réseau, on renvoie offline.html en fallback
        return caches.match('/offline.html');
      });
    })
  );
});
