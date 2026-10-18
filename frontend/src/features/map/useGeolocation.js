import { useState, useEffect } from 'react';

/**
 * Hook to manage GPS geolocation tracking.
 * Implements UC-02 Step 5-7, and Alternative Path A1 (GPS not available/denied).
 *
 * @param {object} [options]
 * @param {boolean} [options.enableHighAccuracy=true]
 * @param {number} [options.timeout=10000]
 * @param {number} [options.maximumAge=5000]
 */
export function useGeolocation(options = {}) {
  const [coords, setCoords] = useState(null);
  const [error, setError] = useState(null);
  const [isSupported, setIsSupported] = useState(true);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (typeof navigator === 'undefined' || !navigator.geolocation) {
      setIsSupported(false);
      setIsLoading(false);
      setError({
        code: 0,
        message: 'Trình duyệt không hỗ trợ Geolocation API.',
      });
      return;
    }

    const {
      enableHighAccuracy = true,
      timeout = 10000,
      maximumAge = 5000,
    } = options;

    const geoOptions = {
      enableHighAccuracy,
      timeout,
      maximumAge,
    };

    let isMounted = true;

    // First attempt to get current position quickly
    navigator.geolocation.getCurrentPosition(
      (position) => {
        if (!isMounted) return;
        setCoords({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          accuracy: position.coords.accuracy,
        });
        setError(null);
        setIsLoading(false);
      },
      (err) => {
        if (!isMounted) return;
        // Alternative Path A1: GPS unavailable or denied
        setError({
          code: err.code,
          message: err.message,
        });
        setIsLoading(false);
      },
      geoOptions,
    );

    // Watch position for movement updates
    const watchId = navigator.geolocation.watchPosition(
      (position) => {
        if (!isMounted) return;
        setCoords({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          accuracy: position.coords.accuracy,
        });
        setError(null);
        setIsLoading(false);
      },
      (err) => {
        if (!isMounted) return;
        setError({
          code: err.code,
          message: err.message,
        });
      },
      geoOptions,
    );

    return () => {
      isMounted = false;
      if (watchId !== undefined) {
        navigator.geolocation.clearWatch(watchId);
      }
    };
  }, [options.enableHighAccuracy, options.timeout, options.maximumAge]);

  return { coords, error, isSupported, isLoading };
}
