/**
 * Supported languages in Saigon Zoo Multilingual Guide System (UC-01).
 */

export const SUPPORTED_LANGUAGES = [
  { code: 'vi', name: 'Tiếng Việt', nativeName: 'Tiếng Việt', flag: '🇻🇳' },
  { code: 'en', name: 'English', nativeName: 'English', flag: '🇬🇧' },
  { code: 'fr', name: 'Français', nativeName: 'Français', flag: '🇫🇷' },
  { code: 'zh', name: 'Chinese', nativeName: '中文', flag: '🇨🇳' },
  { code: 'ja', name: 'Japanese', nativeName: '日本語', flag: '🇯🇵' },
  { code: 'ko', name: 'Korean', nativeName: '한국어', flag: '🇰🇷' },
];

export const DEFAULT_LANGUAGE = 'vi';

/**
 * Checks whether a language code is supported.
 * @param {string} code
 * @returns {boolean}
 */
export function isLanguageSupported(code) {
  return SUPPORTED_LANGUAGES.some((lang) => lang.code === code);
}

/**
 * Finds language info by code.
 * @param {string} code
 * @returns {{code: string, name: string, nativeName: string, flag: string}|undefined}
 */
export function getLanguageByCode(code) {
  return SUPPORTED_LANGUAGES.find((lang) => lang.code === code);
}

