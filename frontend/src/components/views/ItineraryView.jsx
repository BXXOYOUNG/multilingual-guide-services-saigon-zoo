import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useLanguage } from '../../features/localization/LanguageContext';
import { useTranslation } from '../../features/localization/useTranslation';
import { loadPoisWithFallback } from '../../features/map/poiLoader';
import { calculateDistanceMeters } from '../../features/map/geoUtils';

export default function ItineraryView() {
  const { currentLanguage } = useLanguage();
  const { t } = useTranslation();
  const [pois, setPois] = useState(null);
  const [fromId, setFromId] = useState('');
  const [toId, setToId] = useState('');
  useEffect(() => {
    let mounted = true;
    setPois(null);
    loadPoisWithFallback(currentLanguage).then(({ pois: stops }) => { if (mounted) setPois(stops.filter((poi) => Number.isFinite(poi.latitude) && Number.isFinite(poi.longitude))); }).catch(() => { if (mounted) setPois([]); });
    return () => { mounted = false; };
  }, [currentLanguage]);
  const fromPoi = pois?.find((poi) => poi.id === fromId);
  const toPoi = pois?.find((poi) => poi.id === toId);
  const distance = fromPoi && toPoi ? calculateDistanceMeters(fromPoi.latitude, fromPoi.longitude, toPoi.latitude, toPoi.longitude) : null;
  const distanceLabel = Number.isFinite(distance)
    ? `${new Intl.NumberFormat(currentLanguage, { maximumFractionDigits: 0 }).format(distance)} m` : '';
  const routeOptions = [
    { title: t('itinerary.shortTitle'), description: t('itinerary.shortDesc'), stops: 3 },
    { title: t('itinerary.familyTitle'), description: t('itinerary.familyDesc'), stops: 5 },
    { title: t('itinerary.fullTitle'), description: t('itinerary.fullDesc'), stops: 8 },
  ];

  return <div className="itinerary-page">
    <section className="subpage-hero itinerary-hero"><span className="eyebrow">{t('itinerary.eyebrow')}</span><h1>{t('itinerary.title')}</h1><p>{t('itinerary.description')}</p><Link to="/map" className="btn hero-primary">{t('home.ctaMap')} <span>↗</span></Link></section>
    {pois && pois.length > 0 && <section className="poi-distance" aria-labelledby="poi-distance-title">
      <h2 id="poi-distance-title">{t('itinerary.distanceTitle')}</h2>
      <p>{t('itinerary.distanceHint')}</p>
      {pois.length < 2 ? <p>{t('itinerary.distanceNotEnough')}</p> : <>
        <div className="poi-distance-fields">
          <label>{t('itinerary.distanceFrom')}
            <select value={fromPoi ? fromId : ''} onChange={(event) => setFromId(event.target.value)}>
              <option value="">{t('itinerary.distanceChoose')}</option>
              {pois.map((poi) => <option key={poi.id} value={poi.id}>{poi.name}</option>)}
            </select>
          </label>
          <label>{t('itinerary.distanceTo')}
            <select value={toPoi ? toId : ''} onChange={(event) => setToId(event.target.value)}>
              <option value="">{t('itinerary.distanceChoose')}</option>
              {pois.map((poi) => <option key={poi.id} value={poi.id}>{poi.name}</option>)}
            </select>
          </label>
        </div>
        <p className="poi-distance-result" role="status" aria-live="polite">{distanceLabel
          ? t('itinerary.distanceResult', { from: fromPoi.name, to: toPoi.name, distance: distanceLabel })
          : t('itinerary.distanceChooseBoth')}</p>
      </>}
    </section>}
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
