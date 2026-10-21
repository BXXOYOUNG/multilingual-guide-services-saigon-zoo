import { deleteItem, getAllItems, getItem, setItem, STORES } from '../../db/indexedDB';
import { loadPoisWithFallback } from '../map/poiLoader';

const OBJECT_ID = /^[a-f\d]{24}$/i;

export function parseQrPayload(payload) {
  const match = /^TCV-(PACKAGE|POI):([a-f\d]{24})$/i.exec(String(payload || '').trim());
  if (!match) throw new Error('Mã QR không đúng định dạng gói audio/POI Thảo Cầm Viên.');
  return { type: match[1].toUpperCase(), id: match[2].toLowerCase() };
}

export async function downloadAudioPackage(packageId, onProgress = () => {}, signal) {
  if (!OBJECT_ID.test(packageId)) throw new Error('Mã gói audio không hợp lệ.');
  const manifestResponse = await fetch(`/audio/packages/${packageId}/manifest`, { signal });
  if (!manifestResponse.ok) throw new Error(`Không tải được gói audio (${manifestResponse.status}).`);
  const manifest = await manifestResponse.json();
  if (!manifest.package?.is_offline) throw new Error('Gói này chưa được bật tải offline.');
  if (manifest.integrity_status === 'invalid') throw new Error('Gói audio không vượt qua kiểm tra toàn vẹn.');
  if (!manifest.assets?.length) throw new Error('Gói này chưa có audio sẵn sàng.');
  if (manifest.integrity_status === 'unverified' && !window.confirm('Máy chủ chưa xác minh được toàn bộ checksum của gói này. Tiếp tục tải bản demo?')) {
    throw new Error('Đã hủy tải gói audio.');
  }

  const estimatedBytes = manifest.assets.reduce((sum, asset) => sum + (asset.size_bytes || Math.max(0, asset.duration || 0) * 7000), 0);
  if (navigator.storage?.estimate) {
    const { quota, usage } = await navigator.storage.estimate();
    if (quota && quota - (usage || 0) < estimatedBytes * 1.15) throw new Error('Thiết bị có thể không đủ dung lượng cho gói audio.');
  }
  if (navigator.storage?.persist) await navigator.storage.persist().catch(() => false);

  const savedIds = [];
  const previousEntries = new Map();
  const previousPackage = await getItem(STORES.PACKAGES, packageId).catch(() => null);
  try {
    await loadPoisWithFallback(manifest.package.language_code);
    for (let index = 0; index < manifest.assets.length; index += 1) {
      const asset = manifest.assets[index];
      const response = await fetch(`/audio/assets/${asset.id}/content`, { signal });
      if (!response.ok) throw new Error(`Không tải được audio (${response.status}).`);
      const blob = await response.blob();
      if (!blob.size) throw new Error('Audio tải về bị rỗng.');
      if (asset.size_bytes != null && blob.size !== asset.size_bytes) throw new Error('Kích thước audio tải về không khớp.');
      if (/^[a-f\d]{64}$/i.test(asset.checksum || '')) {
        const digest = await crypto.subtle.digest('SHA-256', await blob.arrayBuffer());
        const actual = Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, '0')).join('');
        if (actual !== asset.checksum.toLowerCase()) throw new Error('Checksum audio tải về không khớp.');
      }
      const id = `${packageId}:${asset.poi_id}:${asset.language_code}`;
      if (!previousEntries.has(id)) previousEntries.set(id, await getItem(STORES.OFFLINE_AUDIO, id).catch(() => null));
      await setItem(STORES.OFFLINE_AUDIO, {
        id,
        packageId,
        poiId: asset.poi_id,
        language: asset.language_code,
        assetId: asset.id,
        blob,
        mimeType: blob.type || 'audio/mpeg',
        size: blob.size,
        downloadedAt: Date.now(),
      });
      savedIds.push(id);
      onProgress({ completed: index + 1, total: manifest.assets.length, bytes: blob.size });
    }
    const record = {
      id: packageId,
      name: manifest.package.name,
      description: manifest.package.description,
      language: manifest.package.language_code,
      integrityStatus: manifest.integrity_status,
      assetCount: savedIds.length,
      downloadedAt: Date.now(),
    };
    await setItem(STORES.PACKAGES, record);
    return record;
  } catch (error) {
    await Promise.all(savedIds.map((id) => {
      const previous = previousEntries.get(id);
      return previous ? setItem(STORES.OFFLINE_AUDIO, previous).catch(() => {}) : deleteItem(STORES.OFFLINE_AUDIO, id).catch(() => {});
    }));
    if (previousPackage) await setItem(STORES.PACKAGES, previousPackage).catch(() => {});
    throw error;
  }
}

export async function listOfflineAudio() {
  return getAllItems(STORES.OFFLINE_AUDIO);
}

// A downloaded recording remains usable without contacting the server.
export async function resolvePlayableAudio(poiId, language) {
  const local = await listOfflineAudio().catch(() => []);
  const item = local.find((entry) => entry.poiId === poiId && entry.language === language && entry.blob?.size);
  if (item) return { id: item.assetId, url: URL.createObjectURL(item.blob), local: true };
  const response = await fetch(`/audio/assets/resolve?${new URLSearchParams({ poi_id: poiId, language_code: language })}`);
  if (!response.ok) throw new Error(`Audio unavailable (${response.status})`);
  const asset = await response.json();
  return { id: asset.id, url: `/audio/assets/${asset.id}/content`, local: false };
}
