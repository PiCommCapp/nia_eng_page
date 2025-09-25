/**
 * NIA Engineering Portal - Service Worker
 *
 * This service worker provides offline capabilities for the engineering portal.
 * It caches critical resources and enables the application to work without a network connection.
 */

// Cache name (update version when making changes)
const CACHE_NAME = 'nia-engineering-portal-v1';

// Resources to cache immediately on installation
const PRECACHE_RESOURCES = [
  '/',
  '/index.html',
  '/js/bookmarks-parser.js',
  '/js/service-worker-register.js',
  '/bookmarks.html'
];

// Install event - precache critical resources
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Service worker: Precaching resources');
        return cache.addAll(PRECACHE_RESOURCES);
      })
      .then(() => {
        // Activate the service worker immediately
        return self.skipWaiting();
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.filter(cacheName => {
          // Delete any old caches that don't match the current cache name
          return cacheName.startsWith('nia-engineering-portal-') && cacheName !== CACHE_NAME;
        }).map(cacheName => {
          console.log('Service worker: Removing old cache', cacheName);
          return caches.delete(cacheName);
        })
      );
    }).then(() => {
      // Take control of clients immediately
      return self.clients.claim();
    })
  );
});

// Fetch event - serve cached resources when offline
self.addEventListener('fetch', event => {
  // For non-GET requests, go to the network
  if (event.request.method !== 'GET') {
    return;
  }

  // For all GET requests, try network first, then fall back to cache
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // If response is valid, clone it and store in cache
        if (response && response.status === 200 && response.type === 'basic') {
          const clonedResponse = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, clonedResponse);
          });
        }
        return response;
      })
      .catch(() => {
        // When network fails, serve from cache
        console.log('Service worker: Serving from cache for', event.request.url);
        return caches.match(event.request);
      })
  );
});

// Message event - handle messages from clients
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
