import React from 'react';
import { useLanguage } from '../../features/localization/LanguageContext';
import InteractiveMap from '../../features/map/InteractiveMap';

export default function MapView() {
  const { currentLanguage } = useLanguage();

  return (
    <div className="map-view-page">
      <InteractiveMap language={currentLanguage} />
    </div>
  );
}
