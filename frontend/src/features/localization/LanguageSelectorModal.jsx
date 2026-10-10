import React from 'react';
import { SUPPORTED_LANGUAGES } from './languages';
import { useLanguage } from './LanguageContext';

export default function LanguageSelectorModal() {
  const {
    currentLanguage,
    hasSelectedLanguage,
    isSelectorOpen,
    saveError,
    selectLanguage,
    closeLanguageSelector,
  } = useLanguage();

  if (!isSelectorOpen) {
    return null;
  }

  const handleSelect = async (code) => {
    try {
      await selectLanguage(code);
    } catch (_) {
      // Error is stored in saveError state in LanguageContext (E1)
    }
  };

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.6)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        padding: '16px',
      }}
    >
      <div
        style={{
          backgroundColor: '#ffffff',
          borderRadius: '12px',
          width: '100%',
          maxWidth: '400px',
          padding: '24px',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.2)',
          display: 'flex',
          flexDirection: 'column',
          gap: '16px',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h2 style={{ fontSize: '1.25rem', color: '#1b5e20', margin: 0 }}>
              {hasSelectedLanguage ? 'Chọn ngôn ngữ thuyết minh' : 'Chào mừng đến Thảo Cầm Viên'}
            </h2>
            <p style={{ fontSize: '0.875rem', color: '#666', marginTop: '4px', margin: 0 }}>
              {hasSelectedLanguage
                ? 'Thay đổi ngôn ngữ cho nội dung thuyết minh:'
                : 'Vui lòng chọn ngôn ngữ để bắt đầu trải nghiệm:'}
            </p>
          </div>
          {hasSelectedLanguage && (
            <button
              onClick={closeLanguageSelector}
              style={{
                background: 'none',
                border: 'none',
                fontSize: '1.25rem',
                cursor: 'pointer',
                color: '#666',
                padding: '4px',
              }}
              title="Đóng"
            >
              ✕
            </button>
          )}
        </div>

        {/* Exception Path E1: Error banner */}
        {saveError && (
          <div
            style={{
              backgroundColor: '#ffebee',
              color: '#c62828',
              padding: '10px 14px',
              borderRadius: '6px',
              fontSize: '0.85rem',
              border: '1px solid #ffcdd2',
            }}
          >
            ⚠️ {saveError}
          </div>
        )}

        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {SUPPORTED_LANGUAGES.map((lang) => {
            const isSelected = currentLanguage === lang.code && hasSelectedLanguage;
            return (
              <button
                key={lang.code}
                onClick={() => handleSelect(lang.code)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '12px 16px',
                  borderRadius: '8px',
                  border: isSelected ? '2px solid #2e7d32' : '1px solid #e0e0e0',
                  backgroundColor: isSelected ? '#e8f5e9' : '#fafafa',
                  cursor: 'pointer',
                  fontSize: '1rem',
                  fontWeight: isSelected ? '600' : 'normal',
                  color: isSelected ? '#1b5e20' : '#212121',
                  transition: 'all 0.2s ease',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <span style={{ fontSize: '1.5rem' }}>{lang.flag}</span>
                  <div style={{ textAlign: 'left' }}>
                    <div>{lang.nativeName}</div>
                    {lang.name !== lang.nativeName && (
                      <div style={{ fontSize: '0.75rem', color: '#888' }}>{lang.name}</div>
                    )}
                  </div>
                </div>
                {isSelected && <span style={{ color: '#2e7d32', fontSize: '1.1rem' }}>✓</span>}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}

