import { openDatabase, STORES } from '../db/indexedDB';

function randomObjectId() {
  const bytes = new Uint8Array(12);
  crypto.getRandomValues(bytes);
  return Array.from(bytes, (byte) => byte.toString(16).padStart(2, '0')).join('');
}

function storedId(storage, key) {
  let value = storage.getItem(key);
  if (!/^[a-f\d]{24}$/i.test(value || '')) {
    value = randomObjectId();
    storage.setItem(key, value);
  }
  return value;
}

async function enqueuePendingEvent(eventBody) {
  try {
    const db = await openDatabase();
    const tx = db.transaction(STORES.PENDING_EVENTS, 'readwrite');
    tx.objectStore(STORES.PENDING_EVENTS).add(eventBody);
    await new Promise((resolve, reject) => {
      tx.oncomplete = resolve;
      tx.onerror = () => reject(tx.error);
    });
  } catch {
    // Silently ignore storage errors for background analytics
  }
}

let isFlushing = false;
export async function flushPendingEvents() {
  if (isFlushing || typeof navigator !== 'undefined' && !navigator.onLine) return;
  isFlushing = true;
  try {
    const db = await openDatabase();
    const tx = db.transaction(STORES.PENDING_EVENTS, 'readwrite');
    const store = tx.objectStore(STORES.PENDING_EVENTS);
    const request = store.openCursor();

    const itemsToSend = [];
    await new Promise((resolve) => {
      request.onsuccess = (e) => {
        const cursor = e.target.result;
        if (cursor && itemsToSend.length < 50) {
          itemsToSend.push({ key: cursor.key, value: cursor.value });
          cursor.continue();
        } else {
          resolve();
        }
      };
      request.onerror = () => resolve();
    });

    for (const item of itemsToSend) {
      try {
        const res = await fetch('/api/analytics/events', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(item.value),
        });
        if (res.ok || res.status === 400 || res.status === 422) {
          // If accepted or invalid data, remove from pending queue
          const deleteTx = db.transaction(STORES.PENDING_EVENTS, 'readwrite');
          deleteTx.objectStore(STORES.PENDING_EVENTS).delete(item.key);
          await new Promise((r) => { deleteTx.oncomplete = r; deleteTx.onerror = r; });
        } else {
          break; // Server error or rate limited, retry later
        }
      } catch {
        break; // Network still unavailable
      }
    }
  } catch {
    // Ignore queue flush errors
  } finally {
    isFlushing = false;
  }
}

if (typeof window !== 'undefined') {
  window.addEventListener('online', () => {
    flushPendingEvents();
  });
}

export async function trackEvent(event) {
  const body = {
    device_id: storedId(localStorage, 'tcv_device_id'),
    visitor_id: storedId(localStorage, 'tcv_visitor_id'),
    session_id: storedId(sessionStorage, 'tcv_session_id'),
    ...event,
  };

  try {
    const response = await fetch('/api/analytics/events', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      keepalive: true,
    });
    if (!response.ok && response.status !== 400 && response.status !== 422) {
      // Save for retry on network / 5xx errors
      await enqueuePendingEvent(body);
    } else {
      // Opportunistically flush pending offline events if connected
      flushPendingEvents();
    }
  } catch {
    // Network failure (offline mode) -> Save to IndexedDB queue
    await enqueuePendingEvent(body);
  }
}
