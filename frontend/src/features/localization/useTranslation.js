import { useCallback } from 'react';
import { useLanguage } from './LanguageContext';
import { translate } from './messages';

export function useTranslation() {
  const { currentLanguage } = useLanguage();
  const t = useCallback((key, values) => translate(currentLanguage, key, values), [currentLanguage]);
  return { t, language: currentLanguage };
}
