/**
 * Service Worker registration module for Saigon Zoo Guide PWA.
 * Safe registration utility handling lifecycle events.
 */

export function registerServiceWorker(config = {}) {
  if (typeof window === 'undefined' || !('serviceWorker' in navigator)) {
    console.info('[PWA] Service Worker is not supported by this browser.');
    return Promise.resolve(null);
  }

  return new Promise((resolve) => {
    window.addEventListener('load', () => {
      const swUrl = '/sw.js';

      navigator.serviceWorker
        .register(swUrl, { scope: '/' })
        .then((registration) => {
          console.info('[PWA] Service Worker registered with scope:', registration.scope);

          registration.onupdatefound = () => {
            const installingWorker = registration.installing;
            if (!installingWorker) return;

            installingWorker.onstatechange = () => {
              if (installingWorker.state === 'installed') {
                if (navigator.serviceWorker.controller) {
                  console.info('[PWA] New content is available and will be used when all tabs are closed.');
                  if (config.onUpdate) config.onUpdate(registration);
                } else {
                  console.info('[PWA] Content is cached for offline use.');
                  if (config.onSuccess) config.onSuccess(registration);
                }
              }
            };
          };

          resolve(registration);
        })
        .catch((error) => {
          console.warn('[PWA] Error during Service Worker registration:', error);
          resolve(null);
        });
    });
  });
}

export function unregisterServiceWorker() {
  if (typeof window !== 'undefined' && 'serviceWorker' in navigator) {
    navigator.serviceWorker.ready
      .then((registration) => {
        registration.unregister();
      })
      .catch((error) => {
        console.warn('[PWA] Error unregistering Service Worker:', error);
      });
  }
}

