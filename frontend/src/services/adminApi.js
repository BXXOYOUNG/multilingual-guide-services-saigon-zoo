export async function adminApi(url, options = {}) {
  const response = await fetch(url, { credentials: 'same-origin', ...options, headers: { 'Content-Type': 'application/json', ...(options.headers || {}) } });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.error?.message || body.detail || `Request failed (${response.status})`);
  }
  return response.status === 204 ? null : response.json();
}

export async function uploadPoiImage(poiId, file) {
  if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type) || file.size > 5 * 1024 * 1024) {
    throw new Error('JPEG / PNG / WebP, maximum 5 MB.');
  }
  return adminApi(`/api/admin/pois/${poiId}/image`, { method: 'POST', body: file, headers: { 'Content-Type': file.type } });
}
