/**
 * Calculates distance between two coordinates in meters using the Haversine formula.
 * @param {number} lat1
 * @param {number} lon1
 * @param {number} lat2
 * @param {number} lon2
 * @returns {number} Distance in meters
 */
export function calculateDistanceMeters(lat1, lon1, lat2, lon2) {
  if (
    typeof lat1 !== 'number' ||
    typeof lon1 !== 'number' ||
    typeof lat2 !== 'number' ||
    typeof lon2 !== 'number'
  ) {
    return Infinity;
  }

  const R = 6371e3; // Earth radius in meters
  const rad = Math.PI / 180;
  const phi1 = lat1 * rad;
  const phi2 = lat2 * rad;
  const deltaPhi = (lat2 - lat1) * rad;
  const deltaLambda = (lon2 - lon1) * rad;

  const a =
    Math.sin(deltaPhi / 2) * Math.sin(deltaPhi / 2) +
    Math.cos(phi1) * Math.cos(phi2) *
    Math.sin(deltaLambda / 2) * Math.sin(deltaLambda / 2);

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

  return R * c;
}

/**
 * Finds the nearest POI to the given visitor coordinates.
 * @param {{ latitude: number, longitude: number }} visitorCoords
 * @param {Array<{ id: string, latitude: number, longitude: number }>} pois
 * @returns {{ poi: object | null, distanceMeters: number }}
 */
export function findNearestPoi(visitorCoords, pois) {
  if (
    !visitorCoords ||
    typeof visitorCoords.latitude !== 'number' ||
    typeof visitorCoords.longitude !== 'number' ||
    !Array.isArray(pois) ||
    pois.length === 0
  ) {
    return { poi: null, distanceMeters: Infinity };
  }

  let nearestPoi = null;
  let minDistance = Infinity;

  for (const poi of pois) {
    if (typeof poi.latitude === 'number' && typeof poi.longitude === 'number') {
      const distance = calculateDistanceMeters(
        visitorCoords.latitude,
        visitorCoords.longitude,
        poi.latitude,
        poi.longitude,
      );
      if (distance < minDistance) {
        minDistance = distance;
        nearestPoi = poi;
      }
    }
  }

  return { poi: nearestPoi, distanceMeters: minDistance };
}
