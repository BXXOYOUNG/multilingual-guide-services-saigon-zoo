import React, { useEffect, useRef, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  Map as MapLibreMap,
  NavigationControl,
  Marker,
  Popup,
  setWorkerUrl,
} from 'maplibre-gl';
import maplibreWorkerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url';
import 'maplibre-gl/dist/maplibre-gl.css';

import { useGeolocation } from './useGeolocation';
import { calculateDistanceMeters, findNearestPoi } from './geoUtils';
import { loadPoisWithFallback } from './poiLoader';
import { trackEvent } from '../../services/analytics';
import { resolvePlayableAudio } from '../offline/audioPackages';
import AnimalImageCredit from '../../components/AnimalImageCredit';
import { useTranslation } from '../localization/useTranslation';

setWorkerUrl(maplibreWorkerUrl);

// Saigon Zoo coordinates: ~10.7875° N, 106.7053° E
export const DEFAULT_CENTER = [106.7066, 10.78805];
export const DEFAULT_ZOOM = 15.6;

// Standalone basemap style with OpenStreetMap raster tiles
export const OSM_STYLE = {
  version: 8,
  sources: {
    'osm-tiles': {
      type: 'raster',
      tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
      tileSize: 256,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    },
  },
  layers: [
    {
      id: 'osm-tiles-layer',
      type: 'raster',
      source: 'osm-tiles',
      minzoom: 0,
      maxzoom: 19,
    },
  ],
};

/**
 * Interactive Map Component using MapLibre GL (UC-02 / Task T09)
 * 
 * Features:
 * - MapLibre initialization with zoom/navigation controls
 * - POI rendering as markers with popup details
 * - Current GPS location display (with Alternative Path A1 handling if disabled/denied)
 * - Nearest POI discovery and highlight
 * - Offline fallback support via IndexedDB cache (Alternative Path A2)
 * - Error notification when no POI data is available (Exception Path E1)
 */
export default function InteractiveMap({ language = 'vi' }) {
  const { t } = useTranslation();
  const [searchParams] = useSearchParams();
  const targetPoiId = searchParams.get('poi');
  const [mapContainer, setMapContainer] = useState(null);
  const mapRef = useRef(null);
  const markersRef = useRef([]);
  const visitorMarkerRef = useRef(null);
  const geofenceAudioRef = useRef(null);
  const activeGeofenceRef = useRef(null);
  const triggeredPoisRef = useRef(new Set());

  const [pois, setPois] = useState([]);
  const [dataSource, setDataSource] = useState(null); // 'server' | 'offline'
  const [poiError, setPoiError] = useState(null);
  const [isLoadingPois, setIsLoadingPois] = useState(true);
  const [selectedPoi, setSelectedPoi] = useState(null);
  const [poiAudioUrl, setPoiAudioUrl] = useState('');
  const [poiAudioId, setPoiAudioId] = useState(null);
  const audioRequestRef = useRef(0);
  const preparedAudioRef = useRef(null);
  const manualAudioRef = useRef(null);
  const manualStartedRef = useRef(false);
  const [poiAudioError, setPoiAudioError] = useState('');
  const [poiAudioLoading, setPoiAudioLoading] = useState(false);
  const [geofenceZones, setGeofenceZones] = useState([]);
  const [autoNarrationEnabled, setAutoNarrationEnabled] = useState(false);
  const [autoNarrationMessage, setAutoNarrationMessage] = useState('');
  const [demoLocationOverride, setDemoLocationOverride] = useState(null);
  const [closingPoiDrawer, setClosingPoiDrawer] = useState(false);
  const narrationContextRef = useRef({ language, enabled: autoNarrationEnabled });
  narrationContextRef.current = { language, enabled: autoNarrationEnabled };

  const { coords: visitorCoords, error: gpsError } = useGeolocation();
  const currentCoords = demoLocationOverride || visitorCoords;

  useEffect(() => {
    fetch('/api/geofences').then((response) => response.ok ? response.json() : []).then(setGeofenceZones).catch(() => setGeofenceZones([]));
  }, []);

  useEffect(() => {
    setPoiAudioUrl('');
    setPoiAudioId(null);
    setPoiAudioError('');
    manualStartedRef.current = false;
    if (selectedPoi) {
      trackEvent({ event_type: 'poi_view', poi_id: selectedPoi.id, language_code: language });
      preparePoiAudio();
    }
    return () => {
      audioRequestRef.current += 1;
      if (preparedAudioRef.current?.local) URL.revokeObjectURL(preparedAudioRef.current.url);
      preparedAudioRef.current = null;
    };
  }, [selectedPoi?.id, language]);

  useEffect(() => () => { geofenceAudioRef.current?.pause(); activeGeofenceRef.current = null; }, []);
  useEffect(() => {
    geofenceAudioRef.current?.pause();
    activeGeofenceRef.current = null;
    triggeredPoisRef.current.clear();
    setAutoNarrationMessage('');
  }, [language]);

  async function preparePoiAudio() {
    if (!selectedPoi) return;
    const request = ++audioRequestRef.current;
    setPoiAudioLoading(true);
    setPoiAudioError('');
    try {
      const asset = await resolvePlayableAudio(selectedPoi.id, language);
      if (request !== audioRequestRef.current) {
        if (asset.local) URL.revokeObjectURL(asset.url);
        return;
      }
      if (preparedAudioRef.current?.local) URL.revokeObjectURL(preparedAudioRef.current.url);
      preparedAudioRef.current = asset;
      setPoiAudioId(asset.id);
      setPoiAudioUrl(asset.url);
    } catch (error) {
      if (request === audioRequestRef.current) setPoiAudioError(t('map.audioError'));
    } finally {
      if (request === audioRequestRef.current) setPoiAudioLoading(false);
    }
  }

  function simulateArrival(poi) {
    if (!poiAudioUrl) return;
    const simulatedCoords = { latitude: poi.latitude, longitude: poi.longitude, accuracy: 5 };
    setDemoLocationOverride(simulatedCoords);
    setAutoNarrationEnabled(true);
    triggeredPoisRef.current.add(poi.id);
    activeGeofenceRef.current = poi;
    geofenceAudioRef.current?.pause();
    manualAudioRef.current?.pause();

    const player = new Audio(poiAudioUrl);
    geofenceAudioRef.current = player;
    trackEvent({ event_type: 'geofence_enter', poi_id: poi.id, language_code: language, latitude: poi.latitude, longitude: poi.longitude });
    setAutoNarrationMessage(t('map.autoFinding', { name: poi.name }));
    player.onended = () => {
      trackEvent({ event_type: 'playback_complete', poi_id: poi.id, language_code: language, audio_id: poiAudioId, duration: Math.floor(player.duration || 0) });
      setAutoNarrationMessage(t('map.autoFinished', { name: poi.name }));
    };
    // Start playback in the button's click handler so mobile browsers allow it.
    player.play()
      .then(() => {
        trackEvent({ event_type: 'playback_start', poi_id: poi.id, language_code: language, audio_id: poiAudioId });
        setAutoNarrationMessage(t('map.autoPlaying', { name: poi.name }));
      })
      .catch(() => setAutoNarrationMessage(t('map.audioError')));
  }

  useEffect(() => {
    if (!autoNarrationEnabled || demoLocationOverride || !currentCoords || !pois.length || !geofenceZones.length) return;
    const poiById = new Map(pois.map((poi) => [poi.id, poi]));
    const current = geofenceZones.map((zone) => {
      const poi = poiById.get(zone.poi_id);
      const point = zone.geometry?.coordinates;
      if (!poi || !Array.isArray(point)) return null;
      return { poi, zone, distance: calculateDistanceMeters(currentCoords.latitude, currentCoords.longitude, point[1], point[0]) };
    }).filter((item) => item && item.distance <= item.zone.radius).sort((a, b) => a.distance - b.distance)[0];
    const previous = activeGeofenceRef.current;
    if (previous && (!current || current.poi.id !== previous.id)) {
      geofenceAudioRef.current?.pause();
      trackEvent({ event_type: 'geofence_exit', poi_id: previous.id, language_code: language, latitude: currentCoords.latitude, longitude: currentCoords.longitude });
      activeGeofenceRef.current = null;
    }
    if (!current || activeGeofenceRef.current || triggeredPoisRef.current.has(current.poi.id)) return;
    activeGeofenceRef.current = current.poi;
    triggeredPoisRef.current.add(current.poi.id);
    trackEvent({ event_type: 'geofence_enter', poi_id: current.poi.id, language_code: language, latitude: currentCoords.latitude, longitude: currentCoords.longitude });
    setAutoNarrationMessage(t('map.autoFinding', { name: current.poi.name }));
    fetch(`/audio/assets/resolve?poi_id=${current.poi.id}&language_code=${encodeURIComponent(language)}`)
      .then(async (response) => {
        if (!response.ok) throw new Error('No audio');
        const asset = await response.json();
        if (activeGeofenceRef.current?.id !== current.poi.id || narrationContextRef.current.language !== language || !narrationContextRef.current.enabled) return;
        const player = new Audio(`/audio/assets/${asset.id}/content`);
        geofenceAudioRef.current = player;
        await player.play();
        trackEvent({ event_type: 'playback_start', poi_id: current.poi.id, language_code: language, audio_id: asset.id });
        setAutoNarrationMessage(t('map.autoPlaying', { name: current.poi.name }));
        player.onended = () => {
          trackEvent({ event_type: 'playback_complete', poi_id: current.poi.id, language_code: language, audio_id: asset.id, duration: Math.floor(player.duration || 0) });
          setAutoNarrationMessage(t('map.autoFinished', { name: current.poi.name }));
        };
      })
      .catch(() => {
        if (activeGeofenceRef.current?.id === current.poi.id) setAutoNarrationMessage(t('map.autoNoAudio', { name: current.poi.name }));
      });
  }, [autoNarrationEnabled, demoLocationOverride, currentCoords, pois, geofenceZones, language, t]);

  // 1. Load POIs (UC-02 Step 1-4, A2, E1)
  useEffect(() => {
    let isCancelled = false;

    async function fetchPoiData() {
      setIsLoadingPois(true);
      setPoiError(null);
      try {
        const result = await loadPoisWithFallback(language);
        if (!isCancelled) {
          setPois(result.pois);
          setDataSource(result.source);
        }
      } catch (err) {
        if (!isCancelled) {
          setPoiError(err.message || 'Không thể tải dữ liệu điểm thuyết minh.');
          setPois([]);
        }
      } finally {
        if (!isCancelled) {
          setIsLoadingPois(false);
        }
      }
    }

    fetchPoiData();

    return () => {
      isCancelled = true;
    };
  }, [language]);

  useEffect(() => {
    if (!targetPoiId || !pois.length) return;
    const poi = pois.find((item) => item.id === targetPoiId);
    if (!poi) return;
    setSelectedPoi(poi);
    mapRef.current?.flyTo({ center: [poi.longitude, poi.latitude], zoom: 17, duration: 0 });
  }, [targetPoiId, pois]);

  useEffect(() => {
    setSelectedPoi((selected) => selected ? pois.find((poi) => poi.id === selected.id) || null : null);
  }, [pois]);

  // 2. Initialize MapLibre GL Map
  useEffect(() => {
    if (!mapContainer || mapContainer.nodeType !== 1 || !mapContainer.isConnected) return;

    let map;
    try {
      map = new MapLibreMap({
        container: mapContainer.id,
        style: OSM_STYLE,
        center: DEFAULT_CENTER,
        zoom: DEFAULT_ZOOM,
      });
      map.addControl(new NavigationControl(), 'top-right');
      mapRef.current = map;
    } catch (error) {
      console.error('[map] MapLibre could not initialize its container:', error);
      setPoiError(t('map.contentError'));
      return undefined;
    }

    return () => {
      map.remove();
      if (mapRef.current === map) mapRef.current = null;
    };
  }, [mapContainer]);

  // Compute nearest POI if visitor coordinates exist
  const { poi: nearestPoi, distanceMeters } = findNearestPoi(currentCoords, pois);

  // 3. Update POI markers on map
  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;

    // Clear existing markers
    markersRef.current.forEach((marker) => marker.remove());
    markersRef.current = [];

    // Add markers for all POIs
    pois.forEach((poi) => {
      const isNearest = nearestPoi && nearestPoi.id === poi.id;

      // Create custom HTML element for marker
      const el = document.createElement('div');
      el.className = `map-poi-marker ${isNearest ? 'nearest' : ''}`;
      el.setAttribute('role', 'button');
      el.setAttribute('aria-label', poi.name);
      el.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); setSelectedPoi(poi); }
      });
      el.innerHTML = `
        <div class="marker-pin">
          <span class="marker-icon">${isNearest ? '⭐' : '📍'}</span>
        </div>
      `;

      el.addEventListener('click', () => {
        setSelectedPoi(poi);
      });

      const popupContent = document.createElement('div');
      popupContent.className = 'poi-popup';
      const popupTitle = document.createElement('h3');
      popupTitle.textContent = poi.name;
      popupContent.append(popupTitle);
      const popupDescription = document.createElement('p');
      popupDescription.textContent = poi.description || '';
      popupContent.append(popupDescription);
      if (isNearest) {
        const nearestBadge = document.createElement('span');
        nearestBadge.className = 'nearest-badge';
        nearestBadge.textContent = t('map.nearest');
        popupContent.append(nearestBadge);
      }
      const popup = new Popup({ offset: 25 }).setDOMContent(popupContent);

      const marker = new Marker({ element: el })
        .setLngLat([poi.longitude, poi.latitude])
        .setPopup(popup)
        .addTo(map);

      markersRef.current.push(marker);
    });
  }, [mapContainer, pois, nearestPoi, t]);

  // 4. Update Visitor Position Marker (UC-02 Step 6-7, A1)
  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;

    if (currentCoords) {
      if (!visitorMarkerRef.current) {
        const el = document.createElement('div');
        el.className = 'visitor-location-marker';
        el.innerHTML = '<div class="visitor-pulse"></div><div class="visitor-dot"></div>';

        visitorMarkerRef.current = new Marker({ element: el })
          .setLngLat([currentCoords.longitude, currentCoords.latitude])
          .addTo(map);
      } else {
        visitorMarkerRef.current.setLngLat([currentCoords.longitude, currentCoords.latitude]);
      }
    } else {
      if (visitorMarkerRef.current) {
        visitorMarkerRef.current.remove();
        visitorMarkerRef.current = null;
      }
    }
  }, [mapContainer, currentCoords]);

  const handleCenterOnVisitor = () => {
    if (mapRef.current && currentCoords) {
      mapRef.current.flyTo({
        center: [currentCoords.longitude, currentCoords.latitude],
        zoom: 17,
      });
    }
  };

  const handleCenterOnNearest = () => {
    if (mapRef.current && nearestPoi) {
      mapRef.current.flyTo({
        center: [nearestPoi.longitude, nearestPoi.latitude],
        zoom: 18,
      });
      setSelectedPoi(nearestPoi);
    }
  };

  const handleShowSelectedPoiOnMap = () => {
    if (!selectedPoi) return;
    mapRef.current?.flyTo({
      center: [selectedPoi.longitude, selectedPoi.latitude],
      zoom: 18,
      duration: 650,
    });
    setClosingPoiDrawer(true);
    window.setTimeout(() => {
      setSelectedPoi(null);
      setClosingPoiDrawer(false);
    }, 240);
  };

  return (
    <div className="map-view-container">
      {/* Status Bar */}
      <div className="map-status-bar">
        <div className="status-item gps-warning">{t('map.demoCoordinateNotice')}</div>
        {isLoadingPois && <div className="status-item loading">{t('map.loading')}</div>}
        {dataSource === 'offline' && (
          <div className="status-item offline-badge">{t('map.offline')}</div>
        )}
        {poiError && <div className="status-item error-badge">{t('map.contentError')}</div>}
        {gpsError && !demoLocationOverride && (
          <div className="status-item gps-warning">
            {t('map.gpsDenied')}
          </div>
        )}
        <div className="map-demo-geofence"><button type="button" className="btn btn-secondary" disabled={!geofenceZones.length} onClick={() => { if (autoNarrationEnabled) { geofenceAudioRef.current?.pause(); activeGeofenceRef.current = null; setDemoLocationOverride(null); } setAutoNarrationEnabled((enabled) => !enabled); setAutoNarrationMessage(''); }}>{autoNarrationEnabled ? t('map.autoDisable') : t('map.autoEnable')}</button>{autoNarrationMessage && <span role="status">{autoNarrationMessage}</span>}</div>
      </div>

      {/* Map Canvas */}
      <div className="map-canvas-wrapper" id="saigon-zoo-map-canvas" ref={setMapContainer} />

      {/* Action Controls Overlay */}
      <div className="map-overlay-controls">
        {currentCoords && (
          <button
            type="button"
            className="map-control-btn"
            onClick={handleCenterOnVisitor}
            title={t('map.center')}
          >
            🎯
          </button>
        )}
        {nearestPoi && (
          <button
            type="button"
            className="map-control-btn nearest-btn"
            onClick={handleCenterOnNearest}
            title={t('map.nearest')}
          >
            ⭐ {t('map.nearest')}
          </button>
        )}
      </div>

      {/* Nearest POI Banner (UC-02 Step 8) */}
      {nearestPoi && currentCoords && !selectedPoi && (
        <div className="nearest-poi-card" onClick={handleCenterOnNearest}>
          <div className="nearest-header">
            <span className="badge">{t('map.nearestDistance', { distance: Math.round(distanceMeters) })}</span>
            <h4>{nearestPoi.name}</h4>
          </div>
          <p className="nearest-desc">{nearestPoi.description}</p>
        </div>
      )}

      {/* Selected POI Details Modal / Drawer */}
      {selectedPoi && (
        <div className={`poi-detail-drawer${closingPoiDrawer ? ' closing' : ''}`}>
          <div className="drawer-header">
            <h3>{selectedPoi.name}</h3>
            <button
              type="button"
              className="close-btn"
              onClick={() => setSelectedPoi(null)}
            >
              ✕
            </button>
          </div>
          <p className="drawer-desc">{selectedPoi.description}</p>
          <div className="poi-audio-panel">
            <div className="poi-audio-title"><span aria-hidden="true">♫</span><div><strong>{t('map.audio')}</strong><small>{t('map.language', { language: language.toUpperCase() })}</small></div></div>
            {!poiAudioUrl ? <button type="button" className="btn poi-audio-button" disabled={poiAudioLoading} onClick={preparePoiAudio}>{poiAudioLoading ? t('map.loadingAudio') : t('map.loadAudio')}</button> : <audio ref={manualAudioRef} className="poi-audio-player" controls preload="none" src={poiAudioUrl} onPlay={() => { geofenceAudioRef.current?.pause(); if (!manualStartedRef.current) { trackEvent({ event_type: 'playback_start', poi_id: selectedPoi.id, language_code: language, audio_id: poiAudioId }); manualStartedRef.current = true; } }} onEnded={(event) => { trackEvent({ event_type: 'playback_complete', poi_id: selectedPoi.id, language_code: language, audio_id: poiAudioId, duration: Math.floor(event.currentTarget.duration || 0) }); manualStartedRef.current = false; }} />}
            {poiAudioError && <p className="poi-audio-error" role="status">{poiAudioError}</p>}
          </div>
          {autoNarrationEnabled && <button type="button" className="btn btn-secondary map-simulate-button" disabled={!poiAudioUrl || poiAudioLoading} onClick={() => simulateArrival(selectedPoi)}>{poiAudioLoading ? t('map.loadingAudio') : t('map.simulateArrival')}</button>}
          {selectedPoi.image_url && <img className="poi-detail-image" src={selectedPoi.image_url} alt={selectedPoi.name} />}
          <AnimalImageCredit src={selectedPoi.image_url} />
          {selectedPoi.translation_review_status && <p className="poi-review-note">{t('map.translationReview')}</p>}
          <div className="poi-source-links">
            {selectedPoi.source_url && <a href={selectedPoi.source_url} target="_blank" rel="noreferrer">{t('map.sourceLink')} ↗</a>}
            {selectedPoi.coordinate_source_url && <a href={selectedPoi.coordinate_source_url} target="_blank" rel="noreferrer">{t('map.coordinateSource')} ↗</a>}
          </div>

          <div className="drawer-actions">
            <button type="button" className="btn" onClick={handleShowSelectedPoiOnMap}>
              {t('map.openMap')}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
