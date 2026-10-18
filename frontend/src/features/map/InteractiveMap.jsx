import React, { useEffect, useRef, useState } from 'react';
import {
  Map,
  NavigationControl,
  Marker,
  Popup,
  setWorkerUrl,
} from 'maplibre-gl';
import maplibreWorkerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url';
import 'maplibre-gl/dist/maplibre-gl.css';

import { useGeolocation } from './useGeolocation';
import { findNearestPoi } from './geoUtils';
import { loadPoisWithFallback } from './poiLoader';

setWorkerUrl(maplibreWorkerUrl);

// Saigon Zoo coordinates: ~10.7875° N, 106.7053° E
export const DEFAULT_CENTER = [106.7053, 10.7875];
export const DEFAULT_ZOOM = 16;

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
  const mapContainerRef = useRef(null);
  const mapRef = useRef(null);
  const markersRef = useRef([]);
  const visitorMarkerRef = useRef(null);

  const [pois, setPois] = useState([]);
  const [dataSource, setDataSource] = useState(null); // 'server' | 'offline'
  const [poiError, setPoiError] = useState(null);
  const [isLoadingPois, setIsLoadingPois] = useState(true);
  const [selectedPoi, setSelectedPoi] = useState(null);

  const { coords: visitorCoords, error: gpsError } = useGeolocation();

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

  // 2. Initialize MapLibre GL Map
  useEffect(() => {
    if (!mapContainerRef.current) return;

    const map = new Map({
      container: mapContainerRef.current,
      style: OSM_STYLE,
      center: DEFAULT_CENTER,
      zoom: DEFAULT_ZOOM,
    });

    map.addControl(new NavigationControl(), 'top-right');
    mapRef.current = map;

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  // Compute nearest POI if visitor coordinates exist
  const { poi: nearestPoi, distanceMeters } = findNearestPoi(visitorCoords, pois);

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
      el.innerHTML = `
        <div class="marker-pin">
          <span class="marker-icon">${isNearest ? '⭐' : '📍'}</span>
        </div>
      `;

      el.addEventListener('click', () => {
        setSelectedPoi(poi);
      });

      const popup = new Popup({ offset: 25 }).setHTML(`
        <div class="poi-popup">
          <h3>${poi.name}</h3>
          <p>${poi.description || ''}</p>
          ${isNearest ? '<span class="nearest-badge">Điểm gần bạn nhất</span>' : ''}
        </div>
      `);

      const marker = new Marker({ element: el })
        .setLngLat([poi.longitude, poi.latitude])
        .setPopup(popup)
        .addTo(map);

      markersRef.current.push(marker);
    });
  }, [pois, nearestPoi]);

  // 4. Update Visitor Position Marker (UC-02 Step 6-7, A1)
  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;

    if (visitorCoords) {
      if (!visitorMarkerRef.current) {
        const el = document.createElement('div');
        el.className = 'visitor-location-marker';
        el.innerHTML = '<div class="visitor-pulse"></div><div class="visitor-dot"></div>';

        visitorMarkerRef.current = new Marker({ element: el })
          .setLngLat([visitorCoords.longitude, visitorCoords.latitude])
          .addTo(map);
      } else {
        visitorMarkerRef.current.setLngLat([visitorCoords.longitude, visitorCoords.latitude]);
      }
    } else {
      if (visitorMarkerRef.current) {
        visitorMarkerRef.current.remove();
        visitorMarkerRef.current = null;
      }
    }
  }, [visitorCoords]);

  const handleCenterOnVisitor = () => {
    if (mapRef.current && visitorCoords) {
      mapRef.current.flyTo({
        center: [visitorCoords.longitude, visitorCoords.latitude],
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

  return (
    <div className="map-view-container">
      {/* Status Bar */}
      <div className="map-status-bar">
        {isLoadingPois && <div className="status-item loading">Đang tải điểm thuyết minh...</div>}
        {dataSource === 'offline' && (
          <div className="status-item offline-badge">Đang dùng dữ liệu ngoại tuyến (Offline)</div>
        )}
        {poiError && <div className="status-item error-badge">{poiError}</div>}
        {gpsError && (
          <div className="status-item gps-warning">
            Không có GPS ({gpsError.message || 'Chưa cấp quyền'}) - Bản đồ ở chế độ xem thủ công.
          </div>
        )}
      </div>

      {/* Map Canvas */}
      <div className="map-canvas-wrapper" ref={mapContainerRef} />

      {/* Action Controls Overlay */}
      <div className="map-overlay-controls">
        {visitorCoords && (
          <button
            type="button"
            className="map-control-btn"
            onClick={handleCenterOnVisitor}
            title="Vị trí của bạn"
          >
            🎯
          </button>
        )}
        {nearestPoi && (
          <button
            type="button"
            className="map-control-btn nearest-btn"
            onClick={handleCenterOnNearest}
            title="Đến POI gần nhất"
          >
            ⭐ Gần nhất
          </button>
        )}
      </div>

      {/* Nearest POI Banner (UC-02 Step 8) */}
      {nearestPoi && visitorCoords && (
        <div className="nearest-poi-card" onClick={handleCenterOnNearest}>
          <div className="nearest-header">
            <span className="badge">Gần bạn nhất (~{Math.round(distanceMeters)}m)</span>
            <h4>{nearestPoi.name}</h4>
          </div>
          <p className="nearest-desc">{nearestPoi.description}</p>
        </div>
      )}

      {/* Selected POI Details Modal / Drawer */}
      {selectedPoi && (
        <div className="poi-detail-drawer">
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
          <div className="drawer-actions">
            <button
              type="button"
              className="btn"
              onClick={() => {
                if (mapRef.current) {
                  mapRef.current.flyTo({
                    center: [selectedPoi.longitude, selectedPoi.latitude],
                    zoom: 18,
                  });
                }
              }}
            >
              Xem trên bản đồ
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
