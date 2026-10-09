/**
 * Service Worker for Saigon Zoo Multilingual Guide PWA.
 * Provides offline shell caching and safe routing fallbacks.
 */

const CACHE_NAME = 'saigon-zoo-shell-v1';
const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/manifest.json',
];

// Install: Cache initial App Shell assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_URLS);
    }).then(() => {
      return self.skipWaiting();
    }).catch((err) => {
      console.warn('[SW] Precache failed during install:', err);
    })
  );
});

// Activate: Clean up legacy caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((name) => {
          if (name !== CACHE_NAME && name.startsWith('saigon-zoo-shell-')) {
            return caches.delete(name);
          }
        })
      );
    }).then(() => {
      return self.clients.claim();
    })
  );
});

// Fetch: Strategy for navigation and static assets
self.addEventListener('fetch', (event) => {
  const request = event.request;

  // Ignore non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Handle SPA navigation requests: Network-first, fallback to cached /index.html
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(() => {
        return caches.match('/index.html').then((response) => {
          return response || new Response('Offline - Không có kết nối mạng', {
            status: 503,
            headers: { 'Content-Type': 'text/html; charset=utf-8' },
          });
        });
      })
    );
    return;
  }

  // Handle static assets: Cache-first, fallback to network and update cache
  event.respondWith(
    caches.match(request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }

      return fetch(request).then((networkResponse) => {
        // Cache valid same-origin responses
        if (
          networkResponse &&
          networkResponse.status === 200 &&
          networkResponse.type === 'basic'
        ) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, responseToCache);
          });
        }
        return networkResponse;
      }).catch((err) => {
        // Return fallback if needed or let browser handle it
        return cachedResponse || Promise.reject(err);
      });
    })
  );
});

