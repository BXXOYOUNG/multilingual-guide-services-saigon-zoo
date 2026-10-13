const API_BASE_URL = (import.meta.env?.VITE_API_BASE_URL ?? '').replace(/\/+$/, '');

export class PoiApiError extends Error {
  constructor(message, { status, code = null, details = [] }) {
    super(message);
    this.name = 'PoiApiError';
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

function isPoi(value) {
  return (
    value !== null &&
    typeof value === 'object' &&
    typeof value.id === 'string' &&
    typeof value.name === 'string' &&
    typeof value.description === 'string' &&
    typeof value.latitude === 'number' &&
    typeof value.longitude === 'number'
  );
}

export async function fetchPois(language, fetchImpl = globalThis.fetch) {
  if (typeof language !== 'string' || language.length === 0) {
    throw new TypeError('A language code is required to load POIs');
  }

  const query = new URLSearchParams({ language });
  const response = await fetchImpl(`${API_BASE_URL}/api/pois?${query}`);

  if (!response.ok) {
    let body = null;
    try {
      body = await response.json();
    } catch {
      body = null;
    }

    const error = body?.error;
    throw new PoiApiError(
      typeof error?.message === 'string'
        ? error.message
        : `POI request failed with status ${response.status}`,
      {
        status: response.status,
        code: typeof error?.code === 'string' ? error.code : null,
        details: Array.isArray(error?.details) ? error.details : [],
      },
    );
  }

  const pois = await response.json();
  if (!Array.isArray(pois) || !pois.every(isPoi)) {
    throw new Error('POI response does not match the expected schema');
  }
  return pois;
}
