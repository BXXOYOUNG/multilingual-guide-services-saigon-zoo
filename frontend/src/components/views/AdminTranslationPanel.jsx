import React, { useEffect, useRef, useState } from 'react';
import { useTranslation } from '../../features/localization/useTranslation';
import messages from '../../features/localization/translationMessages';
import { adminApi } from '../../services/adminApi';
import { hasBrowserTranslation, startBrowserTranslations, translationAvailability } from '../../services/browserTranslation';

const LANGUAGES = { vi: 'Tiếng Việt', en: 'English', fr: 'Français', 'zh-Hans': '简体中文', ja: '日本語', ko: '한국어' };

export default function AdminTranslationPanel({ poiId, sourceLanguage, title, description, sourceReady, disabled, onSaved }) {
  const { language } = useTranslation();
  const m = messages[language] || messages.vi;
  const [rows, setRows] = useState([]);
  const [busy, setBusy] = useState(false);
  const [canCancel, setCanCancel] = useState(false);
  const [error, setError] = useState('');
  const [saveStatus, setSaveStatus] = useState('idle');
  const [savedCount, setSavedCount] = useState(0);
  const [snapshot, setSnapshot] = useState('');
  const [availability, setAvailability] = useState({});
  const [expiresAt, setExpiresAt] = useState(0);
  const [expired, setExpired] = useState(false);
  const supported = hasBrowserTranslation();
  const inFlight = useRef(false);
  const controller = useRef(null);
  const alive = useRef(true);
  const selectAllRef = useRef(null);
  const sourceKey = JSON.stringify([sourceLanguage, title, description]);
  const valid = sourceReady && snapshot === sourceKey;
  const blocked = disabled || busy;
  const eligible = rows.filter((row) => row.phase === 'ready' && !row.saved && row.title.trim() && row.description.trim());
  const allSelected = eligible.length > 0 && eligible.every((row) => row.selected && (!row.existing || row.replace));
  const someSelected = eligible.some((row) => row.selected);
  const update = (code, values) => {
    setSaveStatus('idle');
    setRows((items) => items.map((row) => row.language_code === code ? { ...row, ...values } : row));
  };
  useEffect(() => {
    if (selectAllRef.current) selectAllRef.current.indeterminate = someSelected && !allSelected;
  }, [someSelected, allSelected, valid]);

  function selectAll(checked) {
    const codes = new Set(eligible.map((row) => row.language_code));
    setSaveStatus('idle');
    setRows((items) => items.map((row) => codes.has(row.language_code)
      ? { ...row, selected: checked, replace: row.existing ? checked : row.replace } : row));
  }
  useEffect(() => {
    alive.current = true;
    return () => { alive.current = false; controller.current?.abort(); };
  }, []);
  useEffect(() => () => controller.current?.abort(), [sourceKey]);
  useEffect(() => {
    let active = true;
    setAvailability({});
    if (supported) Object.keys(LANGUAGES).filter((code) => code !== sourceLanguage).forEach((code) => {
      translationAvailability(sourceLanguage, code).then((value) => { if (active) setAvailability((previous) => ({ ...previous, [code]: value })); })
        .catch(() => { if (active) setAvailability((previous) => ({ ...previous, [code]: 'unavailable' })); });
    });
    return () => { active = false; };
  }, [sourceLanguage, supported]);
  useEffect(() => {
    if (!expiresAt) return undefined;
    const timer = setTimeout(() => { setExpired(true); controller.current?.abort(); }, Math.max(0, expiresAt - Date.now()));
    return () => clearTimeout(timer);
  }, [expiresAt]);

  async function preview() {
    if (inFlight.current || !sourceReady || !supported) return;
    inFlight.current = true; setBusy(true); setCanCancel(true); setError(''); setSaveStatus('idle');
    const operation = new AbortController(); controller.current = operation;
    const timeout = setTimeout(() => operation.abort(new DOMException('Translation timed out', 'TimeoutError')), 300000);
    let previewReady = false;
    const progress = new Map();
    try {
      const targets = Object.keys(LANGUAGES).filter((code) => code !== sourceLanguage);
      // Native create() must run during this click, before the backend await.
      const translations = startBrowserTranslations({ targets, source: sourceLanguage, title, description,
        signal: operation.signal, onProgress: (code, value) => {
          progress.set(code, value);
          if (previewReady && alive.current && !operation.signal.aborted) update(code, value);
        } });
      const result = await adminApi(`/api/admin/pois/${poiId}/translations/preview`, { method: 'POST',
        signal: operation.signal,
        body: JSON.stringify({ source_language: sourceLanguage, title, description, targets }) });
      if (!alive.current || operation.signal.aborted) return;
      const next = result.results.map((row) => ({ ...row, title: '', description: '', phase: 'downloading',
        ...progress.get(row.language_code), preview_id: result.preview_id, selected: false, replace: false }));
      setRows(next); setExpired(false); setExpiresAt(Date.now() + result.expires_in * 1000);
      setSnapshot(sourceKey);
      previewReady = true;
      const outcomes = await translations;
      if (alive.current) outcomes.forEach(({ language_code: code, value, error: failure }) => {
        update(code, failure ? { phase: 'error', error: failure }
          : operation.signal.aborted ? { phase: 'error', error: 'cancelled' }
            : { ...value, phase: 'ready', error: null });
      });
    } catch (cause) {
      operation.abort();
      if (alive.current) setError(cause.name === 'AbortError' ? m.cancelled : cause.message);
    }
    finally { clearTimeout(timeout); inFlight.current = false; if (alive.current) { setBusy(false); setCanCancel(false); } }
  }

  // Called directly by a click. Start every create() before awaiting any promise
  // so downloading models has the user activation required by Chrome.
  async function translate(codes) {
    if (inFlight.current || !valid || expired || !supported) return;
    inFlight.current = true; setBusy(true); setCanCancel(true); setError(''); setSaveStatus('idle');
    const operation = new AbortController(); controller.current = operation;
    const timeout = setTimeout(() => operation.abort(new DOMException('Translation timed out', 'TimeoutError')), 300000);
    try {
      codes.forEach((code) => update(code, { phase: 'downloading', progress: 0, error: null, selected: false }));
      const outcomes = await startBrowserTranslations({ targets: codes, source: sourceLanguage, title, description,
        signal: operation.signal, onProgress: (code, value) => { if (alive.current && !operation.signal.aborted) update(code, value); } });
      if (alive.current) outcomes.forEach(({ language_code: code, value, error: failure }) => {
        update(code, failure ? { phase: 'error', error: failure }
          : operation.signal.aborted ? { phase: 'error', error: 'cancelled' }
            : { ...value, phase: 'ready', error: null });
      });
    } finally { clearTimeout(timeout); inFlight.current = false; if (alive.current) { setBusy(false); setCanCancel(false); } }
  }

  async function save() {
    if (inFlight.current || disabled || !valid || expired) return;
    const selected = rows.filter((row) => row.selected && row.phase === 'ready' && !row.saved);
    if (!selected.length || selected.some((row) => !row.title.trim() || !row.description.trim() || (row.existing && !row.replace))) return;
    inFlight.current = true; setBusy(true); setError(''); setSaveStatus('saving');
    try {
      await adminApi(`/api/admin/pois/${poiId}/translations/commit`, { method: 'POST', body: JSON.stringify({
          preview_id: selected[0].preview_id, items: selected.map((row) => ({ language_code: row.language_code, title: row.title,
            description: row.description, replace_existing: row.replace })),
        }) });
      if (!alive.current) return;
      setRows((previous) => previous.map((row) => selected.some((item) => item.language_code === row.language_code)
        ? { ...row, saved: true, selected: false } : row));
      setSavedCount(selected.length); setSaveStatus('saved');
      try { await onSaved?.(); }
      catch { if (alive.current) setError(m.refreshFailed); }
    } catch (cause) {
      if (alive.current) { setSaveStatus('error'); setError(cause.message || m.saveFailed); }
    }
    finally { inFlight.current = false; if (alive.current) setBusy(false); }
  }

  return <section className="admin-translation-panel" aria-busy={busy}>
    <header><h3>{m.heading}</h3><span>{m.source}: <strong>{LANGUAGES[sourceLanguage]}</strong></span></header>
    <p>{m.intro}</p><p className="admin-translation-notice">{m.publicNotice}</p>
    <p>{m.browserInfo}</p>
    {!supported && <p role="status">{m.configure}</p>}
    {!sourceReady && <p role="status">{m.saveFirst}</p>}
    <div className="admin-workflow-actions">
      <button type="button" className="btn" disabled={blocked || !sourceReady || !supported} onClick={preview}>{rows.length ? m.translateAllAgain : m.translateAll}</button>
      {valid && !expired && rows.some((row) => !row.saved && row.phase !== 'ready' && availability[row.language_code] !== 'unavailable') && <button type="button" className="btn" disabled={blocked || !supported}
        onClick={() => translate(rows.filter((row) => !row.saved && row.phase !== 'ready' && availability[row.language_code] !== 'unavailable').map((row) => row.language_code))}>{m.translate}</button>}
      {canCancel && <button type="button" className="btn btn-secondary" onClick={() => controller.current?.abort()}>{m.cancel}</button>}
    </div>
    {busy && canCancel && <p role="status">{m.busy}</p>}
    {error && <p role="alert">{error}</p>}
    {rows.length > 0 && !valid && <p role="status">{m.saveFirst}</p>}
    {expired && <p role="alert">{m.previewExpired}</p>}
    {valid && <><p>{m.review} {m.expired}</p>
      <label className="admin-checkbox"><input ref={selectAllRef} type="checkbox" checked={allSelected}
        disabled={blocked || expired || !eligible.length} onChange={(event) => selectAll(event.target.checked)} />{m.selectAll}</label>
      <div className="admin-translation-grid">
      {rows.map((row) => <fieldset key={row.language_code} disabled={blocked || row.saved || expired}>
        <legend>{LANGUAGES[row.language_code]}{row.saved ? ` · ${m.saved}` : ''}</legend>
        {row.error && <p role="alert">{m[row.error] || m.failed}</p>}
        {availability[row.language_code] === 'unavailable' && <p>{m.pairUnavailable}</p>}
        {row.phase !== 'ready' && !row.saved && <>
          {row.phase === 'downloading' && <p role="status">{m.downloading} {row.progress ?? 0}%</p>}
          {row.phase === 'translating' && <p role="status">{m.busy}</p>}
          <button type="button" className="btn btn-secondary" disabled={!supported || availability[row.language_code] === 'unavailable'} onClick={() => translate([row.language_code])}>{row.error ? m.retry : m.translateOne}</button>
        </>}
        {row.phase === 'ready' && <>
          <span className="admin-translation-badge">{row.existing ? m.existing : m.newContent}</span>
          {row.existing && <details><summary>{m.compare}</summary><strong>{row.existing_title}</strong><p className="admin-translation-existing">{row.existing_description}</p></details>}
          <label>{m.title}<input maxLength={180} value={row.title} onChange={(event) => update(row.language_code, { title: event.target.value, selected: false })} /></label>
          <label>{m.description}<textarea rows={6} maxLength={10000} value={row.description} onChange={(event) => update(row.language_code, { description: event.target.value, selected: false })} /></label>
          {row.existing && <label className="admin-checkbox"><input type="checkbox" checked={row.replace} onChange={(event) => update(row.language_code, { replace: event.target.checked, selected: false })} />{m.replace}</label>}
          {!row.saved && <label className="admin-checkbox"><input type="checkbox" checked={row.selected} disabled={(row.existing && !row.replace) || !row.title.trim() || !row.description.trim()}
            onChange={(event) => update(row.language_code, { selected: event.target.checked })} />{m.select}</label>}
        </>}
      </fieldset>)}
    </div><button type="button" className="btn" onClick={save} disabled={blocked || expired || !rows.some((row) => row.selected && row.phase === 'ready' && !row.saved)}>{saveStatus === 'saving' ? m.saving : saveStatus === 'saved' ? m.saveComplete : m.save}</button>
      <p role="status" aria-live="polite">{saveStatus === 'saving' ? m.saving
        : saveStatus === 'saved' ? m.saveSuccess.replace('{count}', String(savedCount)) : ''}</p>
      {saveStatus === 'error' && <p role="alert">{m.saveFailed} {error}</p>}
      <p>{m.audioNotice}</p></>}
  </section>;
}
