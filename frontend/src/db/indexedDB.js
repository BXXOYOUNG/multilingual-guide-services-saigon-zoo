const DB_NAME = 'saigon_zoo_guide';
const DB_VERSION = 1;

export const STORES = {
  APP_STATE: 'app_state',
};

let openDbPromise = null;

function isIndexedDBAvailable() {
  return typeof window !== 'undefined' && Boolean(window.indexedDB);
}

function openDatabase() {
  if (!isIndexedDBAvailable()) {
    return Promise.reject(new Error('IndexedDB is not available in this browser.'));
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
    };

    request.onsuccess = () => {
      resolve(request.result);
    };

    request.onerror = () => {
      openDbPromise = null;
      reject(request.error || new Error('Failed to open IndexedDB.'));
    };

    request.onblocked = () => {
      openDbPromise = null;
      reject(new Error('IndexedDB upgrade is blocked by another open tab.'));
    };
  });

  return openDbPromise;
}

function runStoreOperation(storeName, mode, operation) {
  return openDatabase().then(
    (db) =>
      new Promise((resolve, reject) => {
        if (!db.objectStoreNames.contains(storeName)) {
          reject(new Error(`IndexedDB store does not exist: ${storeName}`));
          return;
        }

        const transaction = db.transaction(storeName, mode);
        const store = transaction.objectStore(storeName);
        const request = operation(store);

        request.onsuccess = () => {
          resolve(request.result);
        };

        request.onerror = () => {
          reject(request.error || new Error(`IndexedDB ${mode} operation failed.`));
        };

        transaction.onerror = () => {
          reject(transaction.error || new Error(`IndexedDB ${mode} transaction failed.`));
        };
      })
  );
}

export function getItem(storeName, key) {
  return runStoreOperation(storeName, 'readonly', (store) => store.get(key));
}

export function setItem(storeName, value, key) {
  return runStoreOperation(storeName, 'readwrite', (store) => store.put(value, key));
}

export function deleteItem(storeName, key) {
  return runStoreOperation(storeName, 'readwrite', (store) => store.delete(key));
}
