import React from 'react';
import { RouterProvider } from 'react-router-dom';
import { router } from './router';
import { LanguageProvider } from '../features/localization/LanguageContext';
import LanguageSelectorModal from '../features/localization/LanguageSelectorModal';

export default function App() {
  return (
    <LanguageProvider>
      <RouterProvider router={router} />
      <LanguageSelectorModal />
    </LanguageProvider>
  );
}

