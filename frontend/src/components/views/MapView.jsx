import React, { lazy, Suspense } from 'react';
import { useLanguage } from '../../features/localization/LanguageContext';
import { useTranslation } from '../../features/localization/useTranslation';
const InteractiveMap = lazy(() => import('../../features/map/InteractiveMap'));

export default function MapView() {
  const { currentLanguage } = useLanguage();
  const { t } = useTranslation();

  return (
    <div className="map-view-page">
      <Suspense fallback={<div className="map-canvas-wrapper">{t('map.loading')}</div>}><InteractiveMap language={currentLanguage} /></Suspense>
    </div>
  );
}
