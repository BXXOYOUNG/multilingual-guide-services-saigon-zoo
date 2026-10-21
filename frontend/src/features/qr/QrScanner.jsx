import React, { useEffect, useRef, useState } from 'react';
import { BrowserMultiFormatReader } from '@zxing/browser';
import { useTranslation } from '../localization/useTranslation';

export default function QrScanner({ onScan, onClose }) {
  const { t } = useTranslation();
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const controlsRef = useRef(null);
  const [errorKey, setErrorKey] = useState('');
  const [starting, setStarting] = useState(false);
  const [active, setActive] = useState(false);

  function stopCamera() {
    controlsRef.current?.stop();
    controlsRef.current = null;
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
    if (videoRef.current) videoRef.current.srcObject = null;
    setActive(false);
  }

  async function startCamera() {
    setErrorKey('');
    if (!window.isSecureContext || !navigator.mediaDevices?.getUserMedia) {
      setErrorKey('qr.secure');
      return;
    }
    setStarting(true);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: false, video: { facingMode: { ideal: 'environment' }, width: { ideal: 1280 }, height: { ideal: 720 } } });
      streamRef.current = stream;
      const video = videoRef.current;
      video.srcObject = stream;
      await video.play();
      const reader = new BrowserMultiFormatReader();
      controlsRef.current = await reader.decodeFromVideoElement(video, (result, decodeError) => {
        if (result) {
          stopCamera();
          onScan(result.getText());
        } else if (decodeError && decodeError.name !== 'NotFoundException') setErrorKey('qr.decode');
      });
      setActive(true);
    } catch (cause) {
      stopCamera();
      const errorKeys = { NotAllowedError: 'qr.permission', NotFoundError: 'qr.missing', NotReadableError: 'qr.busy', OverconstrainedError: 'qr.unavailable' };
      setErrorKey(errorKeys[cause.name] || 'qr.unavailable');
    } finally { setStarting(false); }
  }

  useEffect(() => () => {
    controlsRef.current?.stop();
    streamRef.current?.getTracks().forEach((track) => track.stop());
  }, []);

  return <div className="card qr-scanner-card">
    <div className="drawer-header"><div><span className="eyebrow">QR</span><h2>{t('qr.title')}</h2></div><button className="btn btn-secondary" onClick={() => { stopCamera(); onClose(); }}>{t('qr.close')}</button></div>
    <div className="qr-camera-frame">
      <video ref={videoRef} muted playsInline autoPlay />
      {!active && <div className="qr-camera-placeholder"><span aria-hidden="true">⌗</span><p>{t('qr.placeholder')}</p></div>}
      {active && <div className="qr-scan-guide" aria-hidden="true" />}
    </div>
    {errorKey && <p className="qr-error" role="alert">{t(errorKey)}</p>}
    <div className="qr-scanner-footer"><p>{active ? t('qr.searching') : t('qr.instruction')}</p><button className="btn" disabled={starting} onClick={active ? stopCamera : startCamera}>{starting ? t('qr.starting') : active ? t('qr.stop') : t('qr.start')}</button></div>
  </div>;
}
