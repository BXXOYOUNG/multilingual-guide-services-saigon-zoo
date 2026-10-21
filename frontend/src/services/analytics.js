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

export async function trackEvent(event) {
  try {
    const body = {
      device_id: storedId(localStorage, 'tcv_device_id'),
      visitor_id: storedId(localStorage, 'tcv_visitor_id'),
      session_id: storedId(sessionStorage, 'tcv_session_id'),
      ...event,
    };
    await fetch('/api/analytics/events', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      keepalive: true,
    });
  } catch {
    // Analytics must not interrupt visitor playback or navigation.
  }
}
