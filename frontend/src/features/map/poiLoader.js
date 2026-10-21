import { fetchPois } from '../../services/poiRepository';
import { getAllItems, getItem, setItem, STORES } from '../../db/indexedDB';

/**
 * Loads POIs for a language, attempting server first then local storage fallback.
 * Follows UC-02 Main Flow (Steps 1-4), Alternative Path A2, and Exception Path E1.
 * 
 * @param {string} language
 * @param {(lang: string) => Promise<any[]>} [fetchImpl]
 * @returns {Promise<{ pois: any[], source: 'server' | 'offline' }>}
 */
export async function loadPoisWithFallback(language, fetchImpl = fetchPois) {
  try {
    // Main Flow Step 2 & 3: Attempt to fetch from server
    const serverPois = await fetchImpl(language);
    
    // Cache the retrieved POIs locally for offline use (A2 support)
    try {
      // One snapshot per language: switching language must not overwrite another.
      await setItem(STORES.APP_STATE, { pois: serverPois, cachedAt: Date.now() }, `pois:${language}`);

    } catch (cacheError) {
      console.warn('[poiLoader] Failed to cache POIs to local IndexedDB:', cacheError);
    }

    return { pois: serverPois, source: 'server' };
  } catch (serverError) {
    console.warn('[poiLoader] Server POI fetch failed, attempting offline cache (A2):', serverError);

    // Alternative Path A2: Retrieve stored offline POIs
    try {
      const snapshot = await getItem(STORES.APP_STATE, `pois:${language}`);
      if (snapshot && Array.isArray(snapshot.pois)) return { pois: snapshot.pois, source: 'offline' };
      const storedPois = await getAllItems(STORES.POIS);
      const filteredPois = (storedPois || []).filter(
        (p) => p.language === language,
      );

      if (filteredPois.length > 0) {
        return { pois: filteredPois, source: 'offline' };
      }
    } catch (localError) {
      console.error('[poiLoader] Local POI read failed:', localError);
    }

    // Exception Path E1: Neither server nor local POIs available
    const error = new Error('Không thể tải dữ liệu POI từ máy chủ hoặc bộ nhớ cục bộ.');
    error.code = 'NO_POI_DATA_AVAILABLE';
    error.cause = serverError;
    throw error;
  }
}

