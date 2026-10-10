/**
 * Language persistence layer for UC-01.
 * Uses IndexedDB (STORES.APP_STATE) with localStorage fallback.
 */

import { getItem, setItem, deleteItem, STORES } from '../../db/indexedDB';
import { isLanguageSupported } from './languages';

const LANGUAGE_KEY = 'selected_language';
const LOCAL_STORAGE_KEY = 'saigon_zoo_selected_language';

/**
 * Loads the stored language code from client storage.
 * @returns {Promise<string|null>} Resolves with stored code or null if first launch.
 */
export async function getStoredLanguage() {
  try {
    // 1. Try loading from IndexedDB
    try {
      const stored = await getItem(STORES.APP_STATE, LANGUAGE_KEY);
      if (stored && isLanguageSupported(stored)) {
        return stored;
      }
    } catch (idbErr) {
      console.warn('[Localization] IndexedDB read failed, trying localStorage:', idbErr);
    }

    // 2. Fallback to localStorage
    if (typeof window !== 'undefined' && window.localStorage) {
      const localStored = window.localStorage.getItem(LOCAL_STORAGE_KEY);
      if (localStored && isLanguageSupported(localStored)) {
        return localStored;
      }
    }

    return null;
  } catch (error) {
    console.error('[Localization] Error retrieving stored language:', error);
    return null;
  }
}

/**
 * Saves the selected language to client storage.
 * @param {string} languageCode
 * @returns {Promise<void>}
 * @throws {Error} If language cannot be saved (Exception E1)
 */
export async function saveStoredLanguage(languageCode) {
  if (!isLanguageSupported(languageCode)) {
    throw new Error(`Ngôn ngữ không được hỗ trợ: ${languageCode}`);
  }

  let saved = false;
  let lastError = null;

  // 1. Save to IndexedDB
  try {
    await setItem(STORES.APP_STATE, languageCode, LANGUAGE_KEY);
    saved = true;
  } catch (idbErr) {
    console.warn('[Localization] IndexedDB write failed:', idbErr);
    lastError = idbErr;
  }

  // 2. Save to localStorage as redundancy
  try {
    if (typeof window !== 'undefined' && window.localStorage) {
      window.localStorage.setItem(LOCAL_STORAGE_KEY, languageCode);
      saved = true;
    }
  } catch (lsErr) {
    console.warn('[Localization] LocalStorage write failed:', lsErr);
    lastError = lsErr;
  }

  if (!saved) {
    throw new Error(
      `E1: Không thể lưu ngôn ngữ đã chọn (${lastError?.message || 'Lỗi lưu trữ'})`
    );
  }
}

/**
 * Clears the stored language (useful for testing first-launch flow).
 * @returns {Promise<void>}
 */
export async function clearStoredLanguage() {
  try {
    await deleteItem(STORES.APP_STATE, LANGUAGE_KEY);
  } catch (_) {}

  try {
    if (typeof window !== 'undefined' && window.localStorage) {
      window.localStorage.removeItem(LOCAL_STORAGE_KEY);
    }
  } catch (_) {}
}

