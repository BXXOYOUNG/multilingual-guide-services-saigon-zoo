/**
 * Cache Storage Wrapper for Saigon Zoo Multilingual Guide PWA.
 * Provides helper functions to interact with the browser CacheStorage API.
 */

export const CACHE_NAMES = {
  STATIC: 'saigon-zoo-static-v1',
  AUDIO: 'saigon-zoo-audio-v1',
  MEDIA: 'saigon-zoo-media-v1',
};

/**
 * Checks if CacheStorage API is supported in the current environment.
 * @returns {boolean}
 */
export function isCacheStorageSupported() {
  return typeof window !== 'undefined' && 'caches' in window;
}

/**
 * Stores a request/response pair in a designated cache.
 * @param {string} cacheName
 * @param {RequestInfo|URL} requestOrUrl
 * @param {Response} response
 * @returns {Promise<void>}
 */
export async function putInCache(cacheName, requestOrUrl, response) {
  if (!isCacheStorageSupported()) {
    throw new Error('CacheStorage is not supported in this environment.');
  }
  const cache = await window.caches.open(cacheName);
  await cache.put(requestOrUrl, response);
}

/**
 * Retrieves a cached Response for a given request/URL.
 * @param {string} cacheName
 * @param {RequestInfo|URL} requestOrUrl
 * @returns {Promise<Response|undefined>}
 */
export async function getFromCache(cacheName, requestOrUrl) {
  if (!isCacheStorageSupported()) {
    return undefined;
  }
  const cache = await window.caches.open(cacheName);
  return cache.match(requestOrUrl);
}

/**
 * Removes a request/URL from a cache.
 * @param {string} cacheName
 * @param {RequestInfo|URL} requestOrUrl
 * @returns {Promise<boolean>}
 */
export async function removeFromCache(cacheName, requestOrUrl) {
  if (!isCacheStorageSupported()) {
    return false;
  }
  const cache = await window.caches.open(cacheName);
  return cache.delete(requestOrUrl);
}

/**
 * Checks whether a request/URL exists in a cache.
 * @param {string} cacheName
 * @param {RequestInfo|URL} requestOrUrl
 * @returns {Promise<boolean>}
 */
export async function hasInCache(cacheName, requestOrUrl) {
  const match = await getFromCache(cacheName, requestOrUrl);
  return match !== undefined;
}

/**
 * Clears an entire cache by name.
 * @param {string} cacheName
 * @returns {Promise<boolean>}
 */
export async function clearCache(cacheName) {
  if (!isCacheStorageSupported()) {
    return false;
  }
  return window.caches.delete(cacheName);
}

/**
 * Lists all active cache names managed by the application.
 * @returns {Promise<string[]>}
 */
export async function getCacheNames() {
  if (!isCacheStorageSupported()) {
    return [];
  }
  return window.caches.keys();
}

/**
 * Self-verification test function for CacheStorage functionality.
 * @returns {Promise<{success: boolean, message: string}>}
 */
export async function verifyCacheStorage() {
  if (!isCacheStorageSupported()) {
    return { success: false, message: 'CacheStorage is not supported.' };
  }
  try {
    const testCacheName = 'saigon-zoo-test-cache';
    const testUrl = '/test-health-check';
    const testPayload = JSON.stringify({ status: 'ok', timestamp: Date.now() });
    const response = new Response(testPayload, {
      headers: { 'Content-Type': 'application/json' },
    });

    await putInCache(testCacheName, testUrl, response);
    const cachedResponse = await getFromCache(testCacheName, testUrl);

    if (!cachedResponse) {
      return { success: false, message: 'Failed to retrieve test response from CacheStorage.' };
    }

    const body = await cachedResponse.json();
    if (body.status !== 'ok') {
      return { success: false, message: 'Cached response body does not match expected value.' };
    }

    await clearCache(testCacheName);
    return { success: true, message: 'CacheStorage verification succeeded.' };
  } catch (error) {
    return { success: false, message: error.message || 'CacheStorage verification failed.' };
  }
}

