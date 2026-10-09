/**
 * IndexedDB Wrapper for Saigon Zoo Multilingual Guide PWA.
 * Provides promise-based storage for app state, POI metadata, and offline package states.
 */

const DB_NAME = 'saigon_zoo_offline_db';
const DB_VERSION = 1;

export const STORES = {
  APP_STATE: 'app_state',
  POIS: 'pois',
  PACKAGES: 'packages',
  TEST: 'test_store',
};

/**
 * Opens and initializes the IndexedDB database.
 * @returns {Promise<IDBDatabase>}
 */
export function openDatabase() {
  return new Promise((resolve, reject) => {
    if (typeof window === 'undefined' || !('indexedDB' in window)) {
      return reject(new Error('IndexedDB is not supported in this environment.'));
    }

    const request = window.indexedDB.open(DB_NAME, DB_VERSION);

    request.onupgradeneeded = (event) => {
      const db = event.target.result;

      if (!db.objectStoreNames.contains(STORES.APP_STATE)) {
        db.createObjectStore(STORES.APP_STATE);
      }
      if (!db.objectStoreNames.contains(STORES.POIS)) {
        db.createObjectStore(STORES.POIS, { keyPath: 'id' });
      }
      if (!db.objectStoreNames.contains(STORES.PACKAGES)) {
        db.createObjectStore(STORES.PACKAGES, { keyPath: 'id' });
      }
      if (!db.objectStoreNames.contains(STORES.TEST)) {
        db.createObjectStore(STORES.TEST);
      }
    };

    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error || new Error('Failed to open IndexedDB.'));
  });
}

/**
 * Gets a value from a store by key.
 * @param {string} storeName
 * @param {IDBValidKey} key
 * @returns {Promise<any>}
 */
export async function getItem(storeName, key) {
  const db = await openDatabase();
  return new Promise((resolve, reject) => {
    try {
      const transaction = db.transaction(storeName, 'readonly');
      const store = transaction.objectStore(storeName);
      const request = store.get(key);

      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error || new Error(`Failed to get item from ${storeName}`));
    } catch (err) {
      reject(err);
    }
  });
}

/**
 * Sets a value in a store.
 * @param {string} storeName
 * @param {any} value
 * @param {IDBValidKey} [key] Optional key if store has keyPath or out-of-line keys
 * @returns {Promise<void>}
 */
export async function setItem(storeName, value, key) {
  const db = await openDatabase();
  return new Promise((resolve, reject) => {
    try {
      const transaction = db.transaction(storeName, 'readwrite');
      const store = transaction.objectStore(storeName);
      const request = key !== undefined ? store.put(value, key) : store.put(value);

      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error || new Error(`Failed to set item in ${storeName}`));
    } catch (err) {
      reject(err);
    }
  });
}

/**
 * Deletes an item from a store by key.
 * @param {string} storeName
 * @param {IDBValidKey} key
 * @returns {Promise<void>}
 */
export async function deleteItem(storeName, key) {
  const db = await openDatabase();
  return new Promise((resolve, reject) => {
    try {
      const transaction = db.transaction(storeName, 'readwrite');
      const store = transaction.objectStore(storeName);
      const request = store.delete(key);

      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error || new Error(`Failed to delete item from ${storeName}`));
    } catch (err) {
      reject(err);
    }
  });
}

/**
 * Retrieves all items from a store.
 * @param {string} storeName
 * @returns {Promise<any[]>}
 */
export async function getAllItems(storeName) {
  const db = await openDatabase();
  return new Promise((resolve, reject) => {
    try {
      const transaction = db.transaction(storeName, 'readonly');
      const store = transaction.objectStore(storeName);
      const request = store.getAll();

      request.onsuccess = () => resolve(request.result || []);
      request.onerror = () => reject(request.error || new Error(`Failed to get all items from ${storeName}`));
    } catch (err) {
      reject(err);
    }
  });
}

/**
 * Clears all items in a store.
 * @param {string} storeName
 * @returns {Promise<void>}
 */
export async function clearStore(storeName) {
  const db = await openDatabase();
  return new Promise((resolve, reject) => {
    try {
      const transaction = db.transaction(storeName, 'readwrite');
      const store = transaction.objectStore(storeName);
      const request = store.clear();

      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error || new Error(`Failed to clear store ${storeName}`));
    } catch (err) {
      reject(err);
    }
  });
}

/**
 * Self-verification test function for IndexedDB functionality.
 * Writes a test item, reads it, validates it, and cleans up.
 * @returns {Promise<{success: boolean, message: string}>}
 */
export async function verifyIndexedDB() {
  try {
    const testKey = 'health_check_key';
    const testValue = { timestamp: Date.now(), status: 'ok' };

    await setItem(STORES.TEST, testValue, testKey);
    const retrieved = await getItem(STORES.TEST, testKey);

    if (!retrieved || retrieved.status !== 'ok') {
      return { success: false, message: 'Retrieved value did not match expected value.' };
    }

    await deleteItem(STORES.TEST, testKey);
    return { success: true, message: 'IndexedDB read/write verification succeeded.' };
  } catch (error) {
    return { success: false, message: error.message || 'IndexedDB verification failed.' };
  }
}

