import React, { lazy, Suspense, useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { useLanguage } from '../../features/localization/LanguageContext';
import { useTranslation } from '../../features/localization/useTranslation';
import { useSearchParams } from 'react-router-dom';
import { loadPoisWithFallback } from '../../features/map/poiLoader';
import { deleteItem, getAllItems, STORES } from '../../db/indexedDB';
import { downloadAudioPackage, listOfflineAudio, parseQrPayload, resolvePlayableAudio } from '../../features/offline/audioPackages';
import { trackEvent } from '../../services/analytics';

const QrScanner = lazy(() => import('../../features/qr/QrScanner'));

export default function ExploreView() {
  const { currentLanguage } = useLanguage();
  const { t } = useTranslation();
  const [searchParams, setSearchParams] = useSearchParams();
  const requestedPackageId = searchParams.get('package');
  const [pois, setPois] = useState([]);
  const [packages, setPackages] = useState([]);
  const [audio, setAudio] = useState([]);
  const [scanning, setScanning] = useState(false);
  const [busy, setBusy] = useState(false);
  const [progress, setProgress] = useState(null);
  const [message, setMessage] = useState('');
  const [playing, setPlaying] = useState('');
  const audioRef = useRef(null);
  const objectUrlRef = useRef(null);
  const activePlaybackRef = useRef(null);
  const downloadAbortRef = useRef(null);
  const handledPackageRef = useRef('');

  const refresh = useCallback(async () => {
    const [cachedPackages, cachedAudio, cachedPois] = await Promise.all([
      getAllItems(STORES.PACKAGES), listOfflineAudio(), getAllItems(STORES.POIS),
    ]);
    setPackages(cachedPackages);
    setAudio(cachedAudio);
    try {
      const result = await loadPoisWithFallback(currentLanguage);
      setPois(result.pois);
    } catch {
      setPois((cachedPois || []).filter((poi) => poi.language === currentLanguage));
    }
  }, [currentLanguage]);

  useEffect(() => { refresh().catch((error) => setMessage(error.message)); }, [refresh]);
  useEffect(() => {
    if (!requestedPackageId || handledPackageRef.current === requestedPackageId) return undefined;
    handledPackageRef.current = requestedPackageId;
    const controller = new AbortController();
    downloadAbortRef.current = controller;
    setBusy(true);
    setMessage('');
    downloadAudioPackage(requestedPackageId, setProgress, controller.signal)
      .then(async (pack) => {
        setMessage(t('explore.packageDownloaded', { count: pack.assetCount, name: pack.name }));
        await refresh();
        setSearchParams({}, { replace: true });
      })
      .catch((error) => setMessage(error.name === 'AbortError' ? t('explore.cancelled') : error.message || t('explore.processError')))
      .finally(() => { downloadAbortRef.current = null; setBusy(false); setProgress(null); });
    return undefined;
  }, [requestedPackageId, refresh, setSearchParams, t]);
  useEffect(() => () => {
    audioRef.current?.pause();
    if (objectUrlRef.current) URL.revokeObjectURL(objectUrlRef.current);
  }, []);

  const onScan = useCallback(async (payload) => {
    setScanning(false);
    setBusy(true);
    setMessage('');
    try {
      const qr = parseQrPayload(payload);
      if (qr.type === 'PACKAGE') {
        const controller = new AbortController();
        downloadAbortRef.current = controller;
        const pack = await downloadAudioPackage(qr.id, setProgress, controller.signal);
        setMessage(t('explore.packageDownloaded', { count: pack.assetCount, name: pack.name }));
      } else {
        const asset = await resolvePlayableAudio(qr.id, currentLanguage);
        trackEvent({ event_type: 'qr_scan', poi_id: qr.id, language_code: currentLanguage });
        if (objectUrlRef.current) URL.revokeObjectURL(objectUrlRef.current);
        objectUrlRef.current = asset.local ? asset.url : null;
        audioRef.current.src = asset.url;
        await audioRef.current.play();
        activePlaybackRef.current = { poiId: qr.id, language: currentLanguage, audioId: asset.id, startedAt: Date.now() };
        trackEvent({ event_type: 'playback_start', poi_id: qr.id, language_code: currentLanguage, audio_id: asset.id });
        setPlaying(qr.id);
        setMessage(t('explore.scanPlaying'));
      }
      await refresh();
    } catch (error) { setMessage(error.name === 'AbortError' ? t('explore.cancelled') : error.message || t('explore.processError')); }
    finally { downloadAbortRef.current = null; setBusy(false); setProgress(null); }
  }, [currentLanguage, refresh, t]);

  const poiById = useMemo(() => new Map(pois.map((poi) => [poi.id, poi])), [pois]);

  async function playLocal(item) {
    try {
      if (objectUrlRef.current) URL.revokeObjectURL(objectUrlRef.current);
      objectUrlRef.current = URL.createObjectURL(item.blob);
      audioRef.current.src = objectUrlRef.current;
      await audioRef.current.play();
      activePlaybackRef.current = { poiId: item.poiId, language: item.language, audioId: item.assetId, startedAt: Date.now() };
      setPlaying(item.id);
      trackEvent({ event_type: 'playback_start', poi_id: item.poiId, language_code: item.language, audio_id: item.assetId });
      setMessage(t('explore.offlinePlaying', { name: poiById.get(item.poiId)?.name || t('nav.map') }));
    } catch (error) { setMessage(error.message || t('explore.playError')); }
  }

  async function removePackage(packageId) {
    const entries = audio.filter((item) => item.packageId === packageId);
    await Promise.all(entries.map((item) => deleteItem(STORES.OFFLINE_AUDIO, item.id)));
    await deleteItem(STORES.PACKAGES, packageId);
    setMessage(t('explore.packageDeleted'));
    await refresh();
  }

  function finishPlayback() {
    const playback = activePlaybackRef.current;
    if (playback) {
      trackEvent({ event_type: 'playback_complete', poi_id: playback.poiId, language_code: playback.language, audio_id: playback.audioId, duration: Math.floor(audioRef.current?.duration || 0) });
      activePlaybackRef.current = null;
    }
    setPlaying('');
  }

  return <section className="explore-page">
    <div className="card">
      <h2>{t('explore.title')}</h2>
      <p>{t('explore.description')}</p>
      <div className="explore-scan-action-box">
        <button
          type="button"
          className="btn btn-qr-scan"
          disabled={busy}
          onClick={() => { setMessage(''); setScanning(true); }}
        >
          <span className="qr-btn-icon-shape" aria-hidden="true">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M3 7V5a2 2 0 0 1 2-2h2" />
              <path d="M17 3h2a2 2 0 0 1 2 2v2" />
              <path d="M21 17v2a2 2 0 0 1-2 2h-2" />
              <path d="M7 21H5a2 2 0 0 1-2-2v-2" />
              <rect x="7" y="7" width="10" height="10" rx="1.5" />
            </svg>
          </span>
          <span className="qr-btn-label">{t('explore.scan')}</span>
          <span className="qr-btn-arrow" aria-hidden="true">→</span>
        </button>
      </div>
      {busy && <p role="status">{t('explore.loading', { progress: progress ? `${progress.completed}/${progress.total}` : t('explore.downloading') })}</p>}
      {downloadAbortRef.current && <button className="btn btn-secondary" onClick={() => downloadAbortRef.current?.abort()}>{t('explore.cancel')}</button>}
      {message && <p role="status">{message}</p>}
      <audio ref={audioRef} controls style={{ width: '100%', marginTop: 12 }} onEnded={finishPlayback} />
    </div>
    {scanning && <Suspense fallback={<div className="card">{t('qr.starting')}</div>}><QrScanner onScan={onScan} onClose={() => setScanning(false)} /></Suspense>}
    <div className="card"><h2>{t('explore.packages', { count: packages.length })}</h2>
      {packages.length === 0 ? <p>{t('explore.noPackages')}</p> : packages.map((pack) => <div key={pack.id} className="offline-package-row">
        <div><strong>{pack.name}</strong><p>{pack.assetCount} · {pack.language.toUpperCase()} · {pack.integrityStatus}</p></div>
        <button className="btn btn-secondary" onClick={() => removePackage(pack.id).catch(() => setMessage(t('explore.removeError')))}>{t('explore.delete')}</button>
      </div>)}
    </div>
    <div className="card"><h2>{t('explore.offlinePoints')}</h2>
      {audio.filter((item) => item.language === currentLanguage).map((item) => <div key={item.id} className="offline-package-row">
        <div><strong>{poiById.get(item.poiId)?.name || `POI ${item.poiId.slice(-5)}`}</strong><p>{item.size ? `${(item.size / 1024 / 1024).toFixed(1)} MB` : 'MP3'}</p></div>
        <button className="btn" onClick={() => playLocal(item)}>{playing === item.id ? t('explore.replay') : t('explore.play')}</button>
      </div>)}
      {audio.filter((item) => item.language === currentLanguage).length === 0 && <p>{t('explore.noAudio')}</p>}
    </div>
  </section>;
}

