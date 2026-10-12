/**
 * Network Status service for detecting online/offline transitions.
 */

export function isOnline() {
  if (typeof navigator !== 'undefined' && 'onLine' in navigator) {
    return navigator.onLine;
  }
  return true;
}

export function subscribeNetworkStatus(callback) {
  if (typeof window === 'undefined') {
    return () => {};
  }

  const handleOnline = () => callback({ online: true });
  const handleOffline = () => callback({ online: false });

  window.addEventListener('online', handleOnline);
  window.addEventListener('offline', handleOffline);

  return () => {
    window.removeEventListener('online', handleOnline);
    window.removeEventListener('offline', handleOffline);
  };
}

