import React, { useEffect, useRef, useState } from 'react';
import { useTranslation } from '../../features/localization/useTranslation';
import messages from '../../features/localization/translationMessages';
import { adminApi } from '../../services/adminApi';

const LANGUAGES = { vi: 'Tiếng Việt', en: 'English', fr: 'Français', 'zh-Hans': '简体中文', ja: '日本語', ko: '한국어' };

export default function AdminTranslationPanel({ poiId, sourceLanguage, title, description, sourceReady, disabled, onSaved }) {
  const { language } = useTranslation();
  const m = messages[language] || messages.vi;
  const [rows, setRows] = useState([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [snapshot, setSnapshot] = useState('');
  const [configured, setConfigured] = useState(null);
  const inFlight = useRef(false);
  const sourceKey = JSON.stringify([sourceLanguage, title, description]);
  const valid = sourceReady && snapshot === sourceKey;
  const blocked = disabled || busy;
  const update = (code, values) => setRows((items) => items.map((row) => row.language_code === code ? { ...row, ...values } : row));
  useEffect(() => {
    let alive = true;
    adminApi('/api/admin/translation-settings').then((settings) => { if (alive) setConfigured(settings.configured); })
      .catch((cause) => { if (alive) setError(cause.message); });
    return () => { alive = false; };
  }, []);

  async function preview(retry = false) {
    if (inFlight.current) return;
    inFlight.current = true; setBusy(true); setError('');
    try {
      const targets = retry ? rows.filter((row) => row.error).map((row) => row.language_code)
        : Object.keys(LANGUAGES).filter((code) => code !== sourceLanguage);
      const result = await adminApi(`/api/admin/pois/${poiId}/translations/preview`, { method: 'POST',
        body: JSON.stringify({ source_language: sourceLanguage, title, description, targets }) });
      const next = result.results.map((row) => ({ ...row, preview_id: result.preview_id, selected: false, replace: false }));
      setRows((previous) => retry ? previous.map((row) => next.find((item) => item.language_code === row.language_code) || row) : next);
      setSnapshot(sourceKey);
    } catch (cause) { setError(cause.message); }
    finally { inFlight.current = false; setBusy(false); }
  }

  async function save() {
    if (inFlight.current) return;
    inFlight.current = true; setBusy(true); setError('');
    try {
      const selected = rows.filter((row) => row.selected && !row.error && !row.saved);
      // Retry results may belong to another preview. Each preview group commits atomically.
      for (const token of new Set(selected.map((row) => row.preview_id))) {
        const group = selected.filter((row) => row.preview_id === token);
        await adminApi(`/api/admin/pois/${poiId}/translations/commit`, { method: 'POST', body: JSON.stringify({
          preview_id: token, items: group.map((row) => ({ language_code: row.language_code, title: row.title,
            description: row.description, replace_existing: row.replace })),
        }) });
        setRows((previous) => previous.map((row) => group.some((item) => item.language_code === row.language_code)
          ? { ...row, saved: true, selected: false } : row));
      }
      await onSaved?.();
    } catch (cause) { setError(cause.message); }
    finally { inFlight.current = false; setBusy(false); }
  }

  return <section className="admin-translation-panel" aria-busy={busy}>
    <header><h3>{m.heading}</h3><span>{m.source}: <strong>{LANGUAGES[sourceLanguage]}</strong></span></header>
    <p>{m.intro}</p><p className="admin-translation-notice">{m.publicNotice}</p>
    {configured === false && <p role="status">{m.configure}</p>}
    {!sourceReady && <p role="status">{m.saveFirst}</p>}
    <div className="admin-workflow-actions">
      <button type="button" className="btn btn-secondary" disabled={blocked || !sourceReady || configured !== true} onClick={() => preview()}>{busy ? m.busy : m.translate}</button>
      {valid && rows.some((row) => row.error) && <button type="button" className="btn btn-secondary" disabled={blocked} onClick={() => preview(true)}>{m.retry}</button>}
    </div>
    {error && <p role="alert">{error}</p>}
    {rows.length > 0 && !valid && <p role="status">{m.saveFirst}</p>}
    {valid && <><p>{m.review} {m.expired}</p><div className="admin-translation-grid">
      {rows.map((row) => <fieldset key={row.language_code} disabled={blocked || row.saved}>
        <legend>{LANGUAGES[row.language_code]}{row.saved ? ` · ${m.saved}` : ''}</legend>
        {row.error ? <p role="alert">{row.error}</p> : <>
          <span className="admin-translation-badge">{row.existing ? m.existing : m.newContent}</span>
          {row.existing && <details><summary>{m.compare}</summary><strong>{row.existing_title}</strong><p className="admin-translation-existing">{row.existing_description}</p></details>}
          <label>{m.title}<input maxLength={180} value={row.title} onChange={(event) => update(row.language_code, { title: event.target.value })} /></label>
          <label>{m.description}<textarea rows={6} maxLength={10000} value={row.description} onChange={(event) => update(row.language_code, { description: event.target.value })} /></label>
          {row.existing && <label className="admin-checkbox"><input type="checkbox" checked={row.replace} onChange={(event) => update(row.language_code, { replace: event.target.checked, selected: false })} />{m.replace}</label>}
          {!row.saved && <label className="admin-checkbox"><input type="checkbox" checked={row.selected} disabled={(row.existing && !row.replace) || !row.title.trim() || !row.description.trim()}
            onChange={(event) => update(row.language_code, { selected: event.target.checked })} />{m.select}</label>}
        </>}
      </fieldset>)}
    </div><button type="button" className="btn" onClick={save} disabled={blocked || !rows.some((row) => row.selected && !row.error && !row.saved)}>{busy ? m.busy : m.save}</button><p>{m.audioNotice}</p></>}
  </section>;
}
