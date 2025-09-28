// Service Worker for NIA Engineering Portal
// Provides offline functionality for critical engineering systems

const CACHE_NAME = 'nia-engineering-v1';
const urlsToCache = [
  '/',
  '/pages/',
  '/pages/index.html',
  '/pages/plenary.html',
  '/pages/plenary-operator.html',
  '/pages/plenary-engineer.html',
  '/pages/committees.html',
  '/pages/engineering.html',
  '/pages/cr21.html',
  '/pages/cr21-operator.html',
  '/pages/cr21-engineer.html',
  '/pages/cr29.html',
  '/pages/cr29-operator.html',
  '/pages/cr29-engineer.html',
  '/pages/cr30.html',
  '/pages/cr30-operator.html',
  '/pages/cr30-engineer.html',
  '/pages/senate.html',
  '/pages/senate-operator.html',
  '/pages/senate-engineer.html',
  '/pages/kvm.html',
  '/pages/network.html',
  '/pages/firewalls.html',
  '/pages/dante.html',
  '/pages/car2.html',
  '/pages/cta.html',
  '/pages/b23.html',
];

// Install event - cache resources
self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function (cache) {
      console.log('Opened cache');
      return cache.addAll(urlsToCache);
    }),
  );
});

// Fetch event - serve from cache when offline
self.addEventListener('fetch', function (event) {
  event.respondWith(
    caches.match(event.request).then(function (response) {
      // Return cached version or fetch from network
      if (response) {
        return response;
      }
      return fetch(event.request);
    }),
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (cacheNames) {
      return Promise.all(
        cacheNames.map(function (cacheName) {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        }),
      );
    }),
  );
});
