
/**
 * IndexedDB foundation for the Saigon Zoo multilingual guide.
 * Shared by localization, POI metadata, and offline package features.
 */

const DB_NAME = 'saigon_zoo_guide';
const DB_VERSION = 2;

export const STORES = {
  APP_STATE: 'app_state',
  POIS: 'pois',
  PACKAGES: 'packages',
  TEST: 'test_store',
};

let openDbPromise = null;

function isIndexedDBAvailable() {
  return typeof window !== 'undefined' && Boolean(window.indexedDB);
}

/**
 * Opens and initializes the shared database.
 * Reuses the pending/resolved promise across callers.
 * @returns {Promise<IDBDatabase>}
 */
export function openDatabase() {
  if (!isIndexedDBAvailable()) {
    return Promise.reject(
      new Error('IndexedDB is not available in this browser.'),
    );
  }

  if (openDbPromise) {
    return openDbPromise;
  }

  openDbPromise = new Promise((resolve, reject) => {
    const request = window.indexedDB.open(DB_NAME, DB_VERSION);

    request.onupgradeneeded = () => {
      const db = request.result;

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

    request.onsuccess = () => {
      const db = request.result;

      // Allow a future database-version upgrade to reopen cleanly.
      db.onversionchange = () => {
        db.close();
        openDbPromise = null;
      };

      resolve(db);
    };

    request.onerror = () => {
      openDbPromise = null;
      reject(request.error || new Error('Failed to open IndexedDB.'));
    };
  });

  return openDbPromise;
}

/**
 * Executes one IndexedDB operation and waits for the transaction to finish.
 * @param {string} storeName
 * @param {'readonly' | 'readwrite'} mode
 * @param {(store: IDBObjectStore) => IDBRequest} operation
 * @returns {Promise<any>}
 */
function runStoreOperation(storeName, mode, operation) {
  return openDatabase().then(
    (db) =>
      new Promise((resolve, reject) => {
        let transaction;
        let result;
        let settled = false;

        const rejectOnce = (error) => {
          if (!settled) {
            settled = true;
            reject(error);
          }
        };

        try {
          if (!db.objectStoreNames.contains(storeName)) {
            throw new Error(
              `IndexedDB store does not exist: ${storeName}`,
            );
          }

          transaction = db.transaction(storeName, mode);
          const store = transaction.objectStore(storeName);
          const request = operation(store);

          request.onsuccess = () => {
            result = request.result;
          };

          request.onerror = () => {
            rejectOnce(
              request.error ||
                new Error(`IndexedDB ${mode} operation failed.`),
            );
          };

          transaction.oncomplete = () => {
            if (!settled) {
              settled = true;
              resolve(result);
            }
          };

          transaction.onerror = () => {
            rejectOnce(
              transaction.error ||
                new Error(`IndexedDB ${mode} transaction failed.`),
            );
          };

          transaction.onabort = () => {
            rejectOnce(
              transaction.error ||
                new Error(`IndexedDB ${mode} transaction was aborted.`),
            );
          };
        } catch (error) {
          rejectOnce(error);
        }
      }),
  );
}

/**
 * Gets a value from a store by key.
 * @param {string} storeName
 * @param {IDBValidKey} key
 */
export function getItem(storeName, key) {
  return runStoreOperation(
    storeName,
    'readonly',
    (store) => store.get(key),
  );
}

/**
 * Stores a value.
 * Supports both inline-key stores and stores requiring a separate key.
 * @param {string} storeName
 * @param {any} value
 * @param {IDBValidKey} [key]
 */
export function setItem(storeName, value, key) {
  return runStoreOperation(storeName, 'readwrite', (store) => {
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
  });
}

/**
 * Deletes a value by key.
 */
export function deleteItem(storeName, key) {
  return runStoreOperation(
    storeName,
    'readwrite',
    (store) => store.delete(key),
  );
}

/**
 * Removes all values from a store.
 */
export function clearStore(storeName) {
  return runStoreOperation(
    storeName,
    'readwrite',
    (store) => store.clear(),
  );
}

/**
 * Retrieves all values from a store.
 * @returns {Promise<any[]>}
 */
export function getAllItems(storeName) {
  return runStoreOperation(
    storeName,
    'readonly',
    (store) => store.getAll(),
  );
}

/**
 * Verifies basic IndexedDB read/write/delete operations.
 * @returns {Promise<{success: boolean, message: string}>}
 */
export async function verifyIndexedDB() {
  try {
    const testKey = 'health_check_key';
    const testValue = {
      timestamp: Date.now(),
      status: 'ok',
    };

    await setItem(STORES.TEST, testValue, testKey);

    const retrieved = await getItem(STORES.TEST, testKey);

    if (!retrieved || retrieved.status !== 'ok') {
      return {
        success: false,
        message: 'Retrieved value did not match expected value.',
      };
    }

    await deleteItem(STORES.TEST, testKey);

    return {
      success: true,
      message: 'IndexedDB read/write verification succeeded.',
    };
  } catch (error) {
    return {
      success: false,
      message: error.message || 'IndexedDB verification failed.',
    };
  }
}
