import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useLanguage } from '../../features/localization/LanguageContext';
import { useTranslation } from '../../features/localization/useTranslation';
import { loadPoisWithFallback } from '../../features/map/poiLoader';

export default function ItineraryView() {
  const { currentLanguage } = useLanguage();
  const { t } = useTranslation();
  const [pois, setPois] = useState(null);
  useEffect(() => {
    let mounted = true;
    loadPoisWithFallback(currentLanguage).then(({ pois: stops }) => { if (mounted) setPois(stops.filter((poi) => Number.isFinite(poi.latitude) && Number.isFinite(poi.longitude))); }).catch(() => { if (mounted) setPois([]); });
    return () => { mounted = false; };
  }, [currentLanguage]);
  const routeOptions = [
    { title: t('itinerary.shortTitle'), description: t('itinerary.shortDesc'), stops: 3 },
    { title: t('itinerary.familyTitle'), description: t('itinerary.familyDesc'), stops: 5 },
    { title: t('itinerary.fullTitle'), description: t('itinerary.fullDesc'), stops: 8 },
  ];

  return <div className="itinerary-page">
    <section className="subpage-hero itinerary-hero"><span className="eyebrow">{t('itinerary.eyebrow')}</span><h1>{t('itinerary.title')}</h1><p>{t('itinerary.description')}</p><Link to="/map" className="btn hero-primary">{t('home.ctaMap')} <span>↗</span></Link></section>
    {pois === null ? <div className="card">{t('map.loading')}</div> : pois.length === 0 ? <div className="card">{t('itinerary.noPois')}</div> : <div className="itinerary-grid">{routeOptions.map((route, index) => {
      const stops = pois.slice(0, Math.min(route.stops, pois.length));
      const first = stops[0];
      return <article className={`itinerary-card itinerary-card-${index + 1}`} key={route.title}>
        <div className="itinerary-card-top"><span className="itinerary-index">0{index + 1}</span><span>{t('itinerary.minutes', { count: stops.length * 12 })}</span></div>
        <h2>{route.title}</h2><p>{route.description}</p><div className="itinerary-stop-count">{t('itinerary.stops', { count: stops.length })}</div>
        <ol className="itinerary-stops">{stops.map((poi, stopIndex) => <li key={poi.id}><span>{String(stopIndex + 1).padStart(2, '0')}</span><Link to={`/map?poi=${poi.id}`}>{poi.name}</Link></li>)}</ol>
        <Link className="btn itinerary-start" to={first ? `/map?poi=${first.id}` : '/map'}>{t('itinerary.start')} <span>↗</span></Link>
      </article>;
    })}</div>}
  </div>;
}
