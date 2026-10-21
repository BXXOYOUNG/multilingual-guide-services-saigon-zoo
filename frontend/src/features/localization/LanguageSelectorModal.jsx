import React from 'react';
import { SUPPORTED_LANGUAGES } from './languages';
import { useLanguage } from './LanguageContext';
import { useTranslation } from './useTranslation';

export default function LanguageSelectorModal() {
  const { currentLanguage, hasSelectedLanguage, isSelectorOpen, saveError, selectLanguage, closeLanguageSelector } = useLanguage();
  const { t } = useTranslation();
  if (!isSelectorOpen) return null;

  async function handleSelect(code) {
    try { await selectLanguage(code); } catch { /* The context provides the visible error. */ }
  }

  return <div className="language-modal-backdrop" role="presentation">
    <section className="language-modal" role="dialog" aria-modal="true" aria-labelledby="language-modal-title">
      <header className="language-modal-heading">
        <div><span className="eyebrow">SAIGON ZOO</span><h2 id="language-modal-title">{hasSelectedLanguage ? t('language.choose') : t('language.welcome')}</h2><p>{hasSelectedLanguage ? t('language.change') : t('language.start')}</p></div>
        {hasSelectedLanguage && <button type="button" className="language-modal-close" onClick={closeLanguageSelector} aria-label={t('language.close')}>✕</button>}
      </header>
      {saveError && <p className="language-modal-error" role="alert">{t('language.saveError')}</p>}
      <div className="language-options">
        {SUPPORTED_LANGUAGES.map((lang) => <button type="button" key={lang.code} className={`language-option ${currentLanguage === lang.code && hasSelectedLanguage ? 'selected' : ''}`} onClick={() => handleSelect(lang.code)}>
          <span className="language-flag">{lang.flag}</span><span className="language-option-name"><strong>{lang.nativeName}</strong>{lang.name !== lang.nativeName && <small>{lang.name}</small>}</span>
          {currentLanguage === lang.code && hasSelectedLanguage && <span className="language-check">✓</span>}
        </button>)}
      </div>
    </section>
  </div>;
}
