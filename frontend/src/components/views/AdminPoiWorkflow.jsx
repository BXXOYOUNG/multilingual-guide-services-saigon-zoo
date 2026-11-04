import React, { useEffect, useRef, useState } from 'react';
import { useTranslation } from '../../features/localization/useTranslation';
import { adminApi as api, uploadPoiImage } from '../../services/adminApi';

const LANGUAGE_NAMES = { vi: 'Tiếng Việt', en: 'English', fr: 'Français', 'zh-Hans': '简体中文', ja: '日本語', ko: '한국어' };

export function NarrationPanel({ poiId, language, initialTaskId, initialStatus, onChanged, controllerRef, onBusyChange }) {
  const { t } = useTranslation();
  const [voices, setVoices] = useState([]);
  const [voice, setVoice] = useState('');
  const [jobId, setJobId] = useState(initialTaskId || null);
  const [status, setStatus] = useState(initialStatus || 'draft');
  const [error, setError] = useState('');
  const [audioUrl, setAudioUrl] = useState('');
  const [requesting, setRequesting] = useState(false);
  const active = status === 'Pending' || status === 'Processing';
  const audioRef = useRef(null);
  const changedRef = useRef(onChanged);
  changedRef.current = onChanged;
  useEffect(() => { onBusyChange?.(active || requesting); }, [active, requesting, onBusyChange]);

  function notifyChanged() {
    Promise.resolve().then(() => changedRef.current?.()).catch((cause) => setError(cause.message));
  }

  async function preview() {
    const asset = await api(`/audio/assets/resolve?${new URLSearchParams({ poi_id: poiId, language_code: language })}`);
    setAudioUrl(`/audio/assets/${asset.id}/content`);
  }
  useEffect(() => {
    let alive = true;
    api('/api/admin/audio-voices').then((items) => { if (alive) { setVoices(items[language] || []); setVoice(items[language]?.[0] || ''); } }).catch((cause) => { if (alive) setError(cause.message); });
    preview().catch(() => {});
    return () => { alive = false; audioRef.current?.pause(); };
  }, [poiId, language]);
  useEffect(() => {
    if (!jobId || !active) return undefined;
    let stopped = false;
    let timer;
    async function poll() {
      try {
        const job = await api(`/api/admin/audio-jobs/${jobId}`);
        if (stopped) return;
        setStatus(job.status);
        if (job.status === 'Completed') { await preview(); notifyChanged(); }
        else if (job.status === 'Failed') { setError(job.error_message || t('workflow.jobFailed')); notifyChanged(); }
        else timer = setTimeout(poll, 1500);
      } catch (cause) { if (!stopped) { setError(cause.message); timer = setTimeout(poll, 5000); } }
    }
    poll();
    return () => { stopped = true; clearTimeout(timer); };
  }, [jobId, active, poiId, language]);

  async function generate() {
    setRequesting(true); setError(''); audioRef.current?.pause();
    try {
      const job = await api(`/api/admin/pois/${poiId}/localizations/${language}/generate-audio`, { method: 'POST', body: JSON.stringify({ voice: voice || null }) });
      setJobId(job.id); setStatus(job.status); notifyChanged();
    } catch (cause) { setError(cause.message); throw cause; }
    finally { setRequesting(false); }
  }
  if (controllerRef) controllerRef.current = { generate, busy: active || requesting, invalidate: () => { setAudioUrl(''); setStatus('draft'); setJobId(null); } };
  const statusKey = { Pending: 'jobPending', Processing: 'jobProcessing', Completed: 'jobCompleted', Failed: 'jobFailed' }[status];
  return <section className="admin-narration-panel">
    <h3>{t('workflow.audioPreview')} · {LANGUAGE_NAMES[language]}</h3>
    <p>{t('workflow.ttsHint')}</p>
    <label>{t('workflow.voice')}<select value={voice} onChange={(event) => setVoice(event.target.value)} disabled={active || requesting}>{voices.map((item) => <option key={item}>{item}</option>)}</select></label>
    {statusKey && <p className={`admin-job-state state-${status.toLowerCase()}`} role="status">{t(`workflow.${statusKey}`)}</p>}
    {audioUrl && <audio ref={audioRef} src={audioUrl} controls preload="metadata" />}
    {error && <p role="alert">{error}</p>}
  </section>;
}

export function PoiWorkflowEditor({ poi = null, language, onSaved, onClose }) {
  const { t } = useTranslation();
  const [poiId, setPoiId] = useState(poi?.id || null);
  const [form, setForm] = useState({ name: poi?.name || '', title: poi?.title || '', category: poi?.category || 'animal_exhibit',
    scientific_name: poi?.scientific_name || '', description: poi?.system_description || poi?.description || '',
    latitude: poi?.latitude ?? '', longitude: poi?.longitude ?? '', image_url: poi?.image_url || '', is_active: poi?.is_active || false });
  const [fence, setFence] = useState({ radius: poi?.geofence_radius || 35, is_active: poi?.geofence_active || false });
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState('');
  const [working, setWorking] = useState(false);
  const [error, setError] = useState('');
  const [saved, setSaved] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [narrationBusy, setNarrationBusy] = useState(false);
  const narrationRef = useRef(null);
  const actionRef = useRef('save');
  const lastSavedContent = useRef({ title: form.title, description: form.description });
  useEffect(() => {
    if (!file) { setPreview(''); return undefined; }
    const url = URL.createObjectURL(file); setPreview(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);
  const update = (key) => (event) => setForm((value) => ({ ...value, [key]: event.target.value }));

  async function save(event) {
    event.preventDefault(); setWorking(true); setError(''); setSaved(false);
    try {
      let id = poiId;
      const payload = { name: form.name, category: form.category, scientific_name: form.scientific_name, description: form.description,
        latitude: Number(form.latitude), longitude: Number(form.longitude), image_url: form.image_url, is_active: form.is_active };
      if (!id) {
        const created = await api('/api/admin/pois', { method: 'POST', body: JSON.stringify({ ...payload,
          initial_localization: { language_code: language, title: form.title, description: form.description } }) });
        id = created.id; setPoiId(id);
      } else {
        await api(`/api/admin/pois/${id}`, { method: 'PUT', body: JSON.stringify(payload) });
        if (!poi) {
          await api(`/api/admin/pois/${id}/localizations/${language}`, { method: 'PUT', body: JSON.stringify({ title: form.title, description: form.description }) });
          if (form.title !== lastSavedContent.current.title || form.description !== lastSavedContent.current.description) narrationRef.current?.invalidate();
        }
      }
      lastSavedContent.current = { title: form.title, description: form.description };
      if (file) {
        const result = await uploadPoiImage(id, file);
        setForm((value) => ({ ...value, image_url: result.image_url })); setFile(null);
      }
      await api(`/api/admin/pois/${id}/geofence`, { method: 'PUT', body: JSON.stringify({ ...fence, radius: Number(fence.radius) }) });
      setSaved(true); await onSaved?.();
      if (actionRef.current === 'generate') setGenerating(true);
    } catch (cause) { setError(cause.message); }
    finally { setWorking(false); }
  }
  useEffect(() => {
    if (!generating || !poiId || !narrationRef.current) return;
    setGenerating(false);
    narrationRef.current.generate().catch(() => {});
  }, [generating, poiId]);

  return <div className="card"><span className="eyebrow">CONTENT WORKFLOW</span><h2>{poi ? t('admin.editPoi') : t('admin.addPoi')}</h2>
    <form className="admin-form admin-workflow-form" onSubmit={save}>
      <fieldset disabled={working || generating}>
        <legend>{t('workflow.basicStep')}</legend>
        <label>{t('admin.systemName')}<input value={form.name} onChange={update('name')} required maxLength={180} /></label>
        {!poi && <label>{t('admin.newPoiTitle')} · {LANGUAGE_NAMES[language]}<input value={form.title} onChange={update('title')} required maxLength={180} /></label>}
        <div className="admin-form-columns"><label>{t('admin.category')}<input value={form.category} onChange={update('category')} required maxLength={100} /></label><label>{t('workflow.scientificName')}<input value={form.scientific_name} onChange={update('scientific_name')} maxLength={180} /></label></div>
        <label>{poi ? t('admin.systemDescription') : `${t('admin.content')} · ${LANGUAGE_NAMES[language]}`}<textarea rows={5} value={form.description} onChange={update('description')} required maxLength={3000} /></label>
        <label>{t('workflow.imageUrl')}<input type="text" value={form.image_url} onChange={(event) => { setFile(null); update('image_url')(event); }} placeholder="https://…" /></label>
        <label>{t('workflow.image')}<input type="file" accept="image/jpeg,image/png,image/webp" onChange={(event) => setFile(event.target.files?.[0] || null)} /></label><small>{t('workflow.imageHint')}</small>
        {(preview || form.image_url) && <img className="admin-image-preview" src={preview || form.image_url} alt={form.name} />}
      </fieldset>
      <fieldset disabled={working || generating}>
        <legend>{t('workflow.publishStep')}</legend>
        <div className="admin-form-columns"><label>{t('admin.latitude')}<input type="number" step="any" min="-90" max="90" value={form.latitude} onChange={update('latitude')} required /></label><label>{t('admin.longitude')}<input type="number" step="any" min="-180" max="180" value={form.longitude} onChange={update('longitude')} required /></label></div>
        <label className="admin-checkbox"><input type="checkbox" checked={form.is_active} onChange={(event) => setForm((value) => ({ ...value, is_active: event.target.checked }))} />{t('admin.visibility')}</label>
        <label>{t('workflow.radius')}<input type="number" min="5" max="500" value={fence.radius} onChange={(event) => setFence((value) => ({ ...value, radius: event.target.value }))} required /></label>
        <label className="admin-checkbox"><input type="checkbox" checked={fence.is_active} onChange={(event) => setFence((value) => ({ ...value, is_active: event.target.checked }))} />{t('workflow.fenceActive')}</label>
        <small>{t('map.demoCoordinateNotice')}</small>
      </fieldset>
      {poiId && !poi && <NarrationPanel key={poiId} poiId={poiId} language={language} controllerRef={narrationRef} onChanged={onSaved} onBusyChange={setNarrationBusy} />}
      <div className="admin-workflow-actions"><button type="submit" className="btn" disabled={working || generating} onClick={() => { actionRef.current = 'save'; }}>{working ? t('admin.processing') : t('admin.save')}</button>
        {!poi && <button type="submit" className="btn" disabled={working || generating || narrationBusy} onClick={() => { actionRef.current = 'generate'; }}>{t('workflow.generate')}</button>}
        <button type="button" className="btn btn-secondary" disabled={working} onClick={onClose}>{t('admin.close')}</button></div>
      {saved && <p role="status">{t('workflow.saved')}</p>}{error && <p role="alert">{error}</p>}
    </form>
  </div>;
}

export function LocalizationWorkflowEditor({ poi, language, onSaved, onClose }) {
  const { t } = useTranslation();
  const [title, setTitle] = useState(poi.title || '');
  const [description, setDescription] = useState(poi.description || '');
  const [working, setWorking] = useState(false);
  const [error, setError] = useState('');
  const [saved, setSaved] = useState(false);
  const [narrationBusy, setNarrationBusy] = useState(false);
  const panel = useRef(null);
  const action = useRef('save');
  const original = useRef({ title: poi.title || '', description: poi.description || '' });
  async function save(event) {
    event.preventDefault(); setWorking(true); setError(''); setSaved(false);
    try {
      await api(`/api/admin/pois/${poi.id}/localizations/${language}`, { method: 'PUT', body: JSON.stringify({ title, description, tts_status: 'draft' }) });
      if (title !== original.current.title || description !== original.current.description) panel.current?.invalidate();
      original.current = { title, description };
      await onSaved?.();
      setSaved(true);
      if (action.current === 'generate') await panel.current.generate();
    } catch (cause) { setError(cause.message); }
    finally { setWorking(false); }
  }
  return <div className="card"><h2>{t('admin.translationTitle', { name: poi.name, language: LANGUAGE_NAMES[language] })}</h2><form className="admin-form" onSubmit={save}>
    <label>{t('admin.newPoiTitle')}<input value={title} onChange={(event) => setTitle(event.target.value)} required maxLength={180} /></label>
    <label>{t('admin.content')}<textarea rows={8} value={description} onChange={(event) => setDescription(event.target.value)} required maxLength={10000} /></label>
    <NarrationPanel poiId={poi.id} language={language} initialTaskId={poi.tts_task_id} initialStatus={poi.tts_status} controllerRef={panel} onChanged={onSaved} onBusyChange={setNarrationBusy} />
    <div className="admin-workflow-actions"><button className="btn btn-secondary" disabled={working} onClick={() => { action.current = 'save'; }}>{t('admin.saveDraft')}</button><button className="btn" disabled={working || narrationBusy} onClick={() => { action.current = 'generate'; }}>{t('workflow.generate')}</button><button type="button" className="btn btn-secondary" onClick={onClose}>{t('admin.close')}</button></div>
    {saved && <p role="status">{t('workflow.saved')}</p>}
    {error && <p role="alert">{error}</p>}
  </form></div>;
}
