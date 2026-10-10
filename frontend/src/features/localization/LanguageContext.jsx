import React, { createContext, useContext, useState, useEffect } from 'react';
import { DEFAULT_LANGUAGE, getLanguageByCode } from './languages';
import { getStoredLanguage, saveStoredLanguage } from './languageStorage';

const LanguageContext = createContext(null);

export function LanguageProvider({ children }) {
  const [currentLanguage, setCurrentLanguage] = useState(DEFAULT_LANGUAGE);
  const [hasSelectedLanguage, setHasSelectedLanguage] = useState(false);
  const [isLoadingLanguage, setIsLoadingLanguage] = useState(true);
  const [isSelectorOpen, setIsSelectorOpen] = useState(false);
  const [saveError, setSaveError] = useState(null);

  // On initial mount: check if language was already stored (UC-01 Step 1-2 & Path A1)
  useEffect(() => {
    async function initLanguage() {
      try {
        const stored = await getStoredLanguage();
        if (stored) {
          // Alternative Path A1: Language already saved previously
          setCurrentLanguage(stored);
          setHasSelectedLanguage(true);
          setIsSelectorOpen(false);
        } else {
          // First launch: Prompt visitor to select language (Step 3)
          setHasSelectedLanguage(false);
          setIsSelectorOpen(true);
        }
      } catch (err) {
        console.warn('[LanguageContext] Failed to load stored language:', err);
        setHasSelectedLanguage(false);
        setIsSelectorOpen(true);
      } finally {
        setIsLoadingLanguage(false);
      }
    }

    initLanguage();
  }, []);

  /**
   * Selects and persists language (UC-01 Steps 4, 5, 6).
   * Handles Exception Path E1 if saving fails.
   */
  const selectLanguage = async (code) => {
    setSaveError(null);
    try {
      await saveStoredLanguage(code);
      setCurrentLanguage(code);
      setHasSelectedLanguage(true);
      setIsSelectorOpen(false);
    } catch (err) {
      console.error('[LanguageContext] Error saving language (E1):', err);
      // Exception Path E1: Notification and do not mark as completed
      setSaveError(err.message || 'Không thể lưu ngôn ngữ đã chọn. Vui lòng thử lại.');
      throw err;
    }
  };

  const openLanguageSelector = () => {
    setSaveError(null);
    setIsSelectorOpen(true);
  };

  const closeLanguageSelector = () => {
    // Cannot close on first launch until a language is chosen
    if (hasSelectedLanguage) {
      setIsSelectorOpen(false);
      setSaveError(null);
    }
  };

  const value = {
    currentLanguage,
    currentLanguageInfo: getLanguageByCode(currentLanguage),
    hasSelectedLanguage,
    isLoadingLanguage,
    isSelectorOpen,
    saveError,
    selectLanguage,
    openLanguageSelector,
    closeLanguageSelector,
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}

