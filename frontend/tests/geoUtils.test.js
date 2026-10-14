import test from 'node:test';
import assert from 'node:assert/strict';
import { calculateDistanceMeters, findNearestPoi } from '../src/features/map/geoUtils.js';

test('calculateDistanceMeters accurately calculates distance between two known coordinates', () => {
  // Distance between Saigon Zoo Gate (approx 10.7875, 106.7053) and nearby point
  const lat1 = 10.7875;
  const lon1 = 106.7053;
  const lat2 = 10.7885;
  const lon2 = 106.7053;

  const distance = calculateDistanceMeters(lat1, lon1, lat2, lon2);
  // ~111 meters for 0.001 degree latitude
  assert.ok(distance > 100 && distance < 120, `Expected ~111m, got ${distance}`);

  // Same point should be 0 distance
  assert.equal(calculateDistanceMeters(lat1, lon1, lat1, lon1), 0);
});

test('calculateDistanceMeters handles invalid inputs gracefully', () => {
  assert.equal(calculateDistanceMeters(null, 106.7, 10.7, 106.7), Infinity);
  assert.equal(calculateDistanceMeters(10.7, undefined, 10.7, 106.7), Infinity);
});

test('findNearestPoi identifies closest POI to visitor coordinates', () => {
  const visitorCoords = { latitude: 10.7875, longitude: 106.7053 };
  const pois = [
    { id: 'poi-1', name: 'Far POI', latitude: 10.8000, longitude: 106.7100 },
    { id: 'poi-2', name: 'Nearest POI', latitude: 10.7876, longitude: 106.7054 },
    { id: 'poi-3', name: 'Medium POI', latitude: 10.7900, longitude: 106.7060 },
  ];

  const result = findNearestPoi(visitorCoords, pois);

  assert.equal(result.poi?.id, 'poi-2');
  assert.ok(result.distanceMeters < 50, `Distance should be < 50m, got ${result.distanceMeters}`);
});

test('findNearestPoi handles empty POIs or missing visitor coordinates (UC-02 Path A1)', () => {
  const pois = [{ id: 'poi-1', latitude: 10.7875, longitude: 106.7053 }];

  // GPS unavailable
  const noGpsResult = findNearestPoi(null, pois);
  assert.equal(noGpsResult.poi, null);
  assert.equal(noGpsResult.distanceMeters, Infinity);

  // Empty POI list
  const emptyPoisResult = findNearestPoi({ latitude: 10.7875, longitude: 106.7053 }, []);
  assert.equal(emptyPoisResult.poi, null);
  assert.equal(emptyPoisResult.distanceMeters, Infinity);
});

