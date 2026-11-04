import React, { useCallback, useEffect, useRef, useState } from 'react';
import { QRCodeSVG } from 'qrcode.react';
import { Link } from 'react-router-dom';
import { adminApi as api } from '../../services/adminApi';
import { PoiWorkflowEditor, LocalizationWorkflowEditor } from './AdminPoiWorkflow';
import { useTranslation } from '../../features/localization/useTranslation';


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
  const [packageList, setPackageList] = useState([]);
  const [selected, setSelected] = useState(null);
  const [editingPoi, setEditingPoi] = useState(null);
  const [message, setMessage] = useState('');
  const [working, setWorking] = useState(false);
  const [packageQr, setPackageQr] = useState(null);
  const [poiQr, setPoiQr] = useState(null);
  const [showNewPoi, setShowNewPoi] = useState(false);
  const [showPasswordForm, setShowPasswordForm] = useState(false);

  const load = useCallback(async (silent = false) => {
    if (!silent) setLoading(true);
    try { const [poiRows, packageRows] = await Promise.all([
      api(`/api/admin/pois?language=${language}`),
      api('/audio/packages'),
    ]);
    setPois(poiRows);
    setPackageList(packageRows.filter((pack) => pack.language_code === language)); } finally { setLoading(false); }
  }, [language]);

  useEffect(() => { api('/api/admin/auth/session').then(setUser).catch(() => setUser(null)).finally(() => setSessionLoading(false)); }, []);
  useEffect(() => { setLanguage(appLanguage); setSelected(null); setEditingPoi(null); setShowNewPoi(false); }, [appLanguage]);
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
    setWorking(true);
    try {
      const pack = await api('/api/admin/audio-packages', { method: 'POST', body: JSON.stringify({ name: `Audio guide (${language.toUpperCase()})`, language_code: language }) });
      setPackageQr({ id: pack.id, name: pack.name });
      setMessage(t('admin.packageDone', { count: pack.asset_count }));
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
      {showNewPoi && <AdminDialog onClose={() => setShowNewPoi(false)} label={t('admin.addPoi')}><PoiWorkflowEditor language={language} onClose={() => setShowNewPoi(false)} onSaved={async () => { await load(true); }} /></AdminDialog>}
    </div>
    <div className="card admin-package"><span className="eyebrow">OFFLINE AUDIO</span><h2>{t('admin.package')}</h2><p>{t('workflow.packageHint')}</p><button className="btn" disabled={working} onClick={createPackage}>{t('workflow.packagePublish')}</button>{packageList.map((pack) => <div key={pack.id} className="offline-package-row"><div><strong>{pack.name}</strong><p>{pack.asset_count} audio</p></div><button type="button" className="btn btn-secondary" onClick={() => setPackageQr(pack)}>{t('admin.qrPoi')}</button></div>)}
      {packageQr && <div className="package-qr"><QRCodeSVG value={`TCV-PACKAGE:${packageQr.id}`} size={220} /><p>{packageQr.name}</p><code>TCV-PACKAGE:{packageQr.id}</code><p>{t('admin.packageQrInstruction')}</p></div>}
    </div>
    {poiQr && <AdminDialog onClose={() => setPoiQr(null)} label={t('admin.qrPoi')}><div className="card package-qr"><h2>{t('admin.poiQrTitle', { name: poiQr.title })}</h2><QRCodeSVG value={`TCV-POI:${poiQr.id}`} size={220} /><code>TCV-POI:{poiQr.id}</code><p>{t('admin.poiQrInstruction')}</p><button className="btn btn-secondary" onClick={() => setPoiQr(null)}>{t('admin.close')}</button></div></AdminDialog>}
    {selected && <AdminDialog onClose={() => setSelected(null)} label={t('admin.editTranslation')}><LocalizationWorkflowEditor key={`${selected.id}-${language}`} poi={selected} language={language} onClose={() => setSelected(null)} onSaved={() => load(true)} /></AdminDialog>}
    {editingPoi && <AdminDialog onClose={() => setEditingPoi(null)} label={t('admin.editPoi')}><PoiWorkflowEditor key={editingPoi.id} poi={editingPoi} language={language} onClose={() => setEditingPoi(null)} onSaved={() => load(true)} /></AdminDialog>}
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
