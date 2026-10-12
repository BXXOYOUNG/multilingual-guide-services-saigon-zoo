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

// Install: Cache initial App Shell assets.
// If precaching fails, reject installation instead of accepting
// an incomplete offline shell.
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
      .catch((error) => {
        console.error(
          '[SW] Precache failed; installation aborted:',
          error,
        );
        throw error;
      }),
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


self.addEventListener('fetch', (event) => {
  const request = event.request;

  // Ignore non-GET requests.
  if (request.method !== 'GET') {
    return;
  }

  const requestUrl = new URL(request.url);

  // Do not intercept cross-origin requests.
  if (requestUrl.origin !== self.location.origin) {
    return;
  }

  // Navigation: network first, then cached app shell.
  if (request.mode === 'navigate') {
    event.respondWith(
      (async () => {
        try {
          return await fetch(request);
        } catch {
          const cache = await caches.open(CACHE_NAME);
          const fallback = await cache.match('/index.html');

          if (fallback) {
            return fallback;
          }

          return new Response('Offline - Không có kết nối mạng', {
            status: 503,
            headers: {
              'Content-Type': 'text/html; charset=utf-8',
            },
          });
        }
      })(),
    );
    return;
  }

  // Cache static assets only. Requests without a static destination,
  // such as ordinary API fetches, are left to the browser.
  const cacheableDestinations = [
    'script',
    'style',
    'image',
    'font',
    'worker',
    'manifest',
  ];

  const isStaticAsset =
    cacheableDestinations.includes(request.destination) ||
    requestUrl.pathname.startsWith('/assets/') ||
    requestUrl.pathname === '/manifest.json';

  if (!isStaticAsset) {
    return;
  }

  event.respondWith(
    (async () => {
      const cache = await caches.open(CACHE_NAME);
      const cachedResponse = await cache.match(request);

      if (cachedResponse) {
        return cachedResponse;
      }

      const networkResponse = await fetch(request);

      // Cache successful same-origin responses only.
      if (
        networkResponse.ok &&
        networkResponse.type === 'basic'
      ) {
        try {
          await cache.put(request, networkResponse.clone());
        } catch (error) {
          // Cache failure should not discard a valid network response.
          console.warn('[SW] Failed to cache static asset:', error);
        }
      }

      return networkResponse;
    })(),
  );
});