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

async function runWriteOperation(storeName, operation, fallbackMessage) {
  const db = await openDatabase();

  return new Promise((resolve, reject) => {
    let transaction;

    try {
      transaction = db.transaction(storeName, 'readwrite');
      const store = transaction.objectStore(storeName);

      transaction.oncomplete = () => resolve();

      transaction.onerror = () => {
        reject(transaction.error || new Error(fallbackMessage));
      };

      transaction.onabort = () => {
        reject(transaction.error || new Error(fallbackMessage));
      };

      const request = operation(store);

      request.onerror = () => {
        reject(request.error || new Error(fallbackMessage));
      };
    } catch (error) {
      if (transaction) {
        try {
          transaction.abort();
        } catch {
          // Transaction may already have completed or aborted.
        }
      }

      reject(error);
    }
  });
}

/**
 * Stores a value in IndexedDB.
 * Stores with keyPath use the key inside the value.
 * Stores without keyPath require a separate key unless autoIncrement is enabled.
 *
 * @param {string} storeName
 * @param {any} value
 * @param {IDBValidKey} [key]
 * @returns {Promise<void>}
 */
export async function setItem(storeName, value, key) {
  return runWriteOperation(
    storeName,
    (store) => {
      if (store.keyPath !== null) {
        if (key !== undefined) {
          throw new TypeError(
            `Store "${storeName}" uses an inline key path; do not pass a separate key.`,
          );
        }

        return store.put(value);
      }

      if (key === undefined && !store.autoIncrement) {
        throw new TypeError(
          `Store "${storeName}" requires an explicit key.`,
        );
      }

      return key === undefined
        ? store.put(value)
        : store.put(value, key);
    },
    `Failed to set item in ${storeName}.`,
  );
}

/**
 * Deletes an item from a store by key.
 * @param {string} storeName
 * @param {IDBValidKey} key
 * @returns {Promise<void>}
 */
export async function deleteItem(storeName, key) {
  return runWriteOperation(
    storeName,
    (store) => store.delete(key),
    `Failed to delete item from ${storeName}.`,
  );
}

/**
 * Clears all items from a store.
 * @param {string} storeName
 * @returns {Promise<void>}
 */
export async function clearStore(storeName) {
  return runWriteOperation(
    storeName,
    (store) => store.clear(),
    `Failed to clear store ${storeName}.`,
  );
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

