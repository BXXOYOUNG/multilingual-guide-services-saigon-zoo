import React, { useCallback, useEffect, useRef, useState } from 'react';
import { QRCodeSVG } from 'qrcode.react';
import { Link } from 'react-router-dom';
import { useTranslation } from '../../features/localization/useTranslation';

async function api(url, options = {}) {
  const response = await fetch(url, { credentials: 'same-origin', ...options, headers: { 'Content-Type': 'application/json', ...(options.headers || {}) } });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.error?.message || body.detail || `Request failed (${response.status})`);
  }
  return response.status === 204 ? null : response.json();
}

const LANGS = ['vi', 'en', 'fr', 'zh-Hans', 'ja', 'ko'];
const LANGUAGE_NAMES = { vi: 'Tiếng Việt', en: 'English', fr: 'Français', 'zh-Hans': '中文', ja: '日本語', ko: '한국어' };

export default function AdminView() {
  const { t, language: appLanguage } = useTranslation();
  const [user, setUser] = useState(null);
  const [sessionLoading, setSessionLoading] = useState(true);
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState('');
  const [status, setStatus] = useState('all');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [language, setLanguage] = useState(appLanguage);
  const [pois, setPois] = useState([]);
  const [assets, setAssets] = useState([]);
  const [selected, setSelected] = useState(null);
  const [editingPoi, setEditingPoi] = useState(null);
  const [message, setMessage] = useState('');
  const [working, setWorking] = useState(false);
  const [packageQr, setPackageQr] = useState(null);
  const [poiQr, setPoiQr] = useState(null);
  const [showNewPoi, setShowNewPoi] = useState(false);
  const [showPasswordForm, setShowPasswordForm] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try { const [poiRows, assetRows] = await Promise.all([
      api(`/api/admin/pois?language=${language}`),
      api(`/api/admin/audio-assets?language=${language}`),
    ]);
    setPois(poiRows);
    setAssets(assetRows); } finally { setLoading(false); }
  }, [language]);

  useEffect(() => { api('/api/admin/auth/session').then(setUser).catch(() => setUser(null)).finally(() => setSessionLoading(false)); }, []);
  useEffect(() => { setLanguage(appLanguage); }, [appLanguage]);
  useEffect(() => { if (user) load().catch((error) => setMessage(error.message)); }, [user, load]);

  async function signIn(event) {
    event.preventDefault(); setWorking(true); setMessage('');
    try {
      const result = await api('/api/admin/auth/login', { method: 'POST', body: JSON.stringify({ username, password }) });
      setUser(result); setPassword(''); setMessage(t('admin.loginSuccess'));
    } catch (error) { setMessage(error.message); }
    finally { setWorking(false); }
  }

  async function signOut() {
    await api('/api/admin/auth/logout', { method: 'POST' }).catch(() => {});
    setUser(null); setMessage(t('admin.logoutDone'));
  }

  async function createPackage() {
    const selectedAssets = assets.filter((asset) => !asset.package_id);
    if (!selectedAssets.length) { setMessage(t('admin.packageNoAssets')); return; }
    setWorking(true);
    try {
      const totalBytes = selectedAssets.reduce((sum, asset) => sum + (asset.file_size || Math.max(0, asset.duration) * 7000), 0);
      const pack = await api('/audio/packages', { method: 'POST', body: JSON.stringify({
        name: `Audio guide (${language.toUpperCase()})`, language_code: language,
        description: 'Offline audio package.',
        file_url: `packages/${language}/${Date.now()}.manifest.json`, file_size: totalBytes, is_offline: true,
      }) });
      for (const asset of selectedAssets) await api(`/audio/packages/${pack.id}/assets/${asset.id}`, { method: 'POST' });
      setPackageQr({ id: pack.id, name: pack.name });
      setMessage(t('admin.packageDone', { count: selectedAssets.length }));
      await load();
    } catch (error) { setMessage(error.message); }
    finally { setWorking(false); }
  }

  async function deactivate(poi) {
    if (!window.confirm(t('admin.confirmHide', { name: poi.name }))) return;
    try { await api(`/api/admin/pois/${poi.id}`, { method: 'DELETE' }); setMessage(t('admin.hiddenDone')); await load(); }
    catch (error) { setMessage(error.message); }
  }

  if (sessionLoading) return <div className="admin-empty" role="status">{t('admin.processing')}</div>;
  if (!user) return <section className="card admin-login">
    <span className="eyebrow">TCV / CONTENT STUDIO</span>
    <h2>{t('admin.login')}</h2>
    <form onSubmit={signIn} className="admin-form">
      <label>{t('admin.username')}<input autoComplete="username" value={username} onChange={(event) => setUsername(event.target.value)} required /></label>
      <label>{t('admin.password')}<input type="password" autoComplete="current-password" value={password} onChange={(event) => setPassword(event.target.value)} required /></label>
      <button className="btn" disabled={working}>{working ? t('admin.processing') : t('admin.loginSubmit')}</button>
    </form>
    {message && <p role="status">{message}</p>}
    <p>{t('admin.accountNote')}</p>
  </section>;

  const normalizedQuery = query.trim().toLocaleLowerCase();
  const visiblePois = pois.filter((poi) => (!normalizedQuery || `${poi.title} ${poi.name} ${poi.category}`.toLocaleLowerCase().includes(normalizedQuery)) && (status === 'all' || (status === 'active' ? poi.is_active : status === 'hidden' ? !poi.is_active : !poi.audio_url)));
  return <section className="admin-content">
    <div className="card admin-session"><div><h2>{t('admin.greeting', { name: user.username })}</h2><p>{t('admin.editorialNote')}</p></div><div className="admin-actions"><Link className="btn" to="/admin/analytics">{t('admin.openDashboard')}</Link><button className="btn btn-secondary" onClick={() => setShowPasswordForm((value) => !value)}>{t('admin.changePassword')}</button><button className="btn btn-secondary" onClick={signOut}>{t('admin.logout')}</button></div></div>
    {message && <div className="admin-notice" role="status"><span>{message}</span><button type="button" aria-label={t('admin.close')} onClick={() => setMessage('')}>×</button></div>}
    <div className="admin-summary">{[[t('admin.allPois'), pois.length], [t('admin.active'), pois.filter((poi) => poi.is_active).length], [t('admin.audioAvailable'), pois.filter((poi) => poi.audio_url).length], [t('admin.noLocalization'), pois.filter((poi) => !poi.has_localization).length]].map(([label, count]) => <article key={label}><span>{label}</span><strong>{loading ? '—' : count}</strong></article>)}</div>
    {showPasswordForm && <AdminDialog onClose={() => setShowPasswordForm(false)} label={t('admin.changePassword')}><PasswordForm onClose={() => setShowPasswordForm(false)} onSaved={() => setMessage(t('admin.passwordChanged'))} /></AdminDialog>}
    <div className="card admin-library">
      <div className="admin-section-heading"><div><span className="eyebrow">CONTENT LIBRARY</span><h2>{t('admin.poiContent')}</h2></div><button className="btn" onClick={() => setShowNewPoi(true)}>{t('admin.addPoi')}</button></div>
      <div className="admin-toolbar">
        <label className="admin-search">{t('admin.search')}<input type="search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder={t('admin.searchHint')} /></label>
        <label>{t('admin.language')}<select value={language} onChange={(event) => { setLanguage(event.target.value); setSelected(null); }}>{LANGS.map((lang) => <option key={lang} value={lang}>{LANGUAGE_NAMES[lang]}</option>)}</select></label>
        <label>{t('admin.filter')}<select value={status} onChange={(event) => setStatus(event.target.value)}><option value="all">{t('admin.allPois')}</option><option value="active">{t('admin.active')}</option><option value="hidden">{t('admin.hidden')}</option><option value="noAudio">{t('admin.noAudio')}</option></select></label>
      </div>
      {loading ? <p className="admin-empty" role="status">{t('admin.processing')}</p> : <>
        <p className="admin-result-count">{visiblePois.length} / {pois.length} POI</p>
        {!visiblePois.length && <p className="admin-empty">{t('admin.emptyResults')}</p>}
        {visiblePois.map((poi) => <article className="admin-poi-row" key={poi.id}>
          <div className="admin-poi-info"><div className="admin-poi-heading"><strong>{poi.title || poi.name}</strong><span className={`admin-badge ${poi.is_active ? 'is-active' : ''}`}>{poi.is_active ? t('admin.active') : t('admin.hidden')}</span></div><p>{poi.category} · {poi.latitude ?? '—'}, {poi.longitude ?? '—'}</p><div className="admin-poi-tags"><span className={`admin-badge ${poi.audio_url ? 'is-active' : 'is-warning'}`}>{poi.audio_url ? t('admin.audioAvailable') : t('admin.noAudio')}</span>{!poi.has_localization && <span className="admin-badge is-warning">{t('admin.noLocalization')}</span>}{poi.tts_status && <span className="admin-badge">{poi.tts_status}</span>}</div></div>
          <div className="admin-actions"><button className="btn btn-secondary" onClick={() => setSelected(poi)}>{t('admin.editTranslation')}</button><button className="btn btn-secondary" onClick={() => setEditingPoi(poi)}>{t('admin.editPoi')}</button><button className="btn btn-secondary" onClick={() => setPoiQr(poi)}>{t('admin.qrPoi')}</button>{poi.is_active && <button className="btn admin-danger" onClick={() => deactivate(poi)}>{t('admin.hidePoi')}</button>}</div>
        </article>)}
      </>}
      {showNewPoi && <AdminDialog onClose={() => setShowNewPoi(false)} label={t('admin.addPoi')}><div className="card"><h2>{t('admin.addPoi')}</h2><NewPoiForm language={language} onSaved={async () => { setShowNewPoi(false); await load(); setMessage(t('admin.savedPoi')); }} /></div></AdminDialog>}
    </div>
    <div className="card admin-package"><span className="eyebrow">OFFLINE AUDIO</span><h2>{t('admin.package')}</h2><p>{t('admin.packageReady', { count: assets.filter((asset) => !asset.package_id).length, language: language.toUpperCase() })}</p><button className="btn" disabled={working} onClick={createPackage}>{t('admin.createPackage')}</button>
      {packageQr && <div className="package-qr"><QRCodeSVG value={`TCV-PACKAGE:${packageQr.id}`} size={220} /><p>{packageQr.name}</p><code>TCV-PACKAGE:{packageQr.id}</code><p>{t('admin.packageQrInstruction')}</p></div>}
    </div>
    {poiQr && <AdminDialog onClose={() => setPoiQr(null)} label={t('admin.qrPoi')}><div className="card package-qr"><h2>{t('admin.poiQrTitle', { name: poiQr.title })}</h2><QRCodeSVG value={`TCV-POI:${poiQr.id}`} size={220} /><code>TCV-POI:{poiQr.id}</code><p>{t('admin.poiQrInstruction')}</p><button className="btn btn-secondary" onClick={() => setPoiQr(null)}>{t('admin.close')}</button></div></AdminDialog>}
    {selected && <AdminDialog onClose={() => setSelected(null)} label={t('admin.editTranslation')}><LocalizationEditor key={`${selected.id}-${language}`} poi={selected} language={language} onClose={() => setSelected(null)} onSaved={async () => { setSelected(null); await load(); setMessage(t('admin.translationSaved')); }} /></AdminDialog>}
    {editingPoi && <AdminDialog onClose={() => setEditingPoi(null)} label={t('admin.editPoi')}><PoiEditor key={editingPoi.id} poi={editingPoi} onClose={() => setEditingPoi(null)} onSaved={async () => { setEditingPoi(null); await load(); setMessage(t('admin.poiUpdated')); }} /></AdminDialog>}
  </section>;
}

function AdminDialog({ children, label, onClose }) {
  const ref = useRef(null);
  const { t } = useTranslation();
  useEffect(() => { const dialog = ref.current; dialog.showModal(); return () => dialog.close(); }, []);
  return <dialog ref={ref} className="admin-dialog" aria-label={label} onCancel={onClose}>
    <button type="button" className="admin-dialog-close" onClick={onClose} aria-label={t('admin.close')}>×</button>{children}
  </dialog>;
}

function PasswordForm({ onClose, onSaved }) {
  const { t } = useTranslation();
  const [current, setCurrent] = useState('');
  const [next, setNext] = useState('');
  const [error, setError] = useState('');
  async function submit(event) {
    event.preventDefault(); setError('');
    try { await api('/api/admin/auth/password', { method: 'POST', body: JSON.stringify({ current_password: current, new_password: next }) }); setCurrent(''); setNext(''); onSaved(); onClose(); }
    catch (cause) { setError(cause.message); }
  }
  return <div className="card"><h2>{t('admin.changePassword')}</h2><form className="admin-form" onSubmit={submit}><label>{t('admin.passwordCurrent')}<input type="password" autoComplete="current-password" value={current} onChange={(event) => setCurrent(event.target.value)} required /></label><label>{t('admin.passwordNew')}<input type="password" autoComplete="new-password" minLength={12} value={next} onChange={(event) => setNext(event.target.value)} required /></label><div><button className="btn">{t('admin.update')}</button> <button type="button" className="btn btn-secondary" onClick={onClose}>{t('admin.close')}</button></div>{error && <p role="alert">{error}</p>}</form></div>;
}

function PoiEditor({ poi, onClose, onSaved }) {
  const { t } = useTranslation();
  const [form, setForm] = useState({ name: poi.name || '', category: poi.category || '', description: poi.system_description ?? poi.description ?? '', latitude: poi.latitude, longitude: poi.longitude, image_url: poi.image_url || '', is_active: poi.is_active });
  const [error, setError] = useState('');
  const update = (key) => (event) => setForm((current) => ({ ...current, [key]: event.target.value }));
  async function save(event) {
    event.preventDefault(); setError('');
    try { await api(`/api/admin/pois/${poi.id}`, { method: 'PUT', body: JSON.stringify({ ...form, latitude: Number(form.latitude), longitude: Number(form.longitude) }) }); await onSaved(); }
    catch (cause) { setError(cause.message); }
  }
  return <div className="card"><h2>{t('admin.poiUpdate', { name: poi.name })}</h2><form className="admin-form" onSubmit={save}>
    <label>{t('admin.systemName')}<input value={form.name} onChange={update('name')} required /></label><label>{t('admin.category')}<input value={form.category} onChange={update('category')} required /></label>
    <label>{t('admin.systemDescription')}<textarea rows={4} value={form.description} onChange={update('description')} required /></label>
    <label>{t('admin.latitude')}<input type="number" step="any" min="-90" max="90" value={form.latitude} onChange={update('latitude')} required /></label><label>{t('admin.longitude')}<input type="number" step="any" min="-180" max="180" value={form.longitude} onChange={update('longitude')} required /></label>
    <label><span>{t('admin.visibility')}</span><input type="checkbox" checked={form.is_active} onChange={(event) => setForm((current) => ({ ...current, is_active: event.target.checked }))} /></label>
    <p>{t('admin.locationReview')}</p><div><button className="btn">{t('admin.save')}</button> <button type="button" className="btn btn-secondary" onClick={onClose}>{t('admin.close')}</button></div>{error && <p role="alert">{error}</p>}
  </form></div>;
}

function NewPoiForm({ language, onSaved }) {
  const { t } = useTranslation();
  const [form, setForm] = useState({ name: '', title: '', category: '', description: '', latitude: '', longitude: '' });
  const [error, setError] = useState('');
  const update = (key) => (event) => setForm((current) => ({ ...current, [key]: event.target.value }));
  async function save(event) {
    event.preventDefault(); setError('');
    try {
      const created = await api('/api/admin/pois', { method: 'POST', body: JSON.stringify({ name: form.name, category: form.category, description: form.description, latitude: Number(form.latitude), longitude: Number(form.longitude), image_url: '', is_active: false }) });
      await api(`/api/admin/pois/${created.id}/localizations/${language}`, { method: 'PUT', body: JSON.stringify({ title: form.title, description: form.description, tts_status: 'draft' }) });
      await onSaved();
    } catch (cause) { setError(cause.message); }
  }
  return <form className="admin-form" onSubmit={save}>
    <label>{t('admin.systemName')}<input value={form.name} onChange={update('name')} required /></label>
    <label>{t('admin.newPoiTitle')}<input value={form.title} onChange={update('title')} required /></label>
    <label>{t('admin.category')}<input value={form.category} onChange={update('category')} required /></label>
    <label>{t('admin.descriptionDraft')}<textarea rows={4} value={form.description} onChange={update('description')} required /></label>
    <label>{t('admin.latitude')}<input type="number" step="any" min="-90" max="90" value={form.latitude} onChange={update('latitude')} required /></label>
    <label>{t('admin.longitude')}<input type="number" step="any" min="-180" max="180" value={form.longitude} onChange={update('longitude')} required /></label>
    <p>{t('admin.locationHidden')}</p>
    <button className="btn">{t('admin.createPoi')}</button>{error && <p role="alert">{error}</p>}
  </form>;
}

function LocalizationEditor({ poi, language, onClose, onSaved }) {
  const { t } = useTranslation();
  const [title, setTitle] = useState(poi.title || '');
  const [description, setDescription] = useState(poi.description || '');
  const [error, setError] = useState('');
  async function save(event) {
    event.preventDefault(); setError('');
    try { await api(`/api/admin/pois/${poi.id}/localizations/${language}`, { method: 'PUT', body: JSON.stringify({ title, description, tts_status: 'draft' }) }); await onSaved(); }
    catch (cause) { setError(cause.message); }
  }
  return <div className="card"><h2>{t('admin.translationTitle', { name: poi.name, language })}</h2><form className="admin-form" onSubmit={save}><label>{t('admin.newPoiTitle')}<input value={title} onChange={(event) => setTitle(event.target.value)} required /></label><label>{t('admin.content')}<textarea rows={8} value={description} onChange={(event) => setDescription(event.target.value)} required /></label><div><button className="btn">{t('admin.saveDraft')}</button> <button type="button" className="btn btn-secondary" onClick={onClose}>{t('admin.close')}</button></div>{error && <p role="alert">{error}</p>}</form><p>{t('admin.translationReview')}</p></div>;
}
