import React, { useCallback, useEffect, useRef, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { adminApi } from '../../services/adminApi';
import { useTranslation } from '../../features/localization/useTranslation';

export default function AdminPasswordGate({ children }) {
  const { t } = useTranslation();
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [current, setCurrent] = useState('');
  const [next, setNext] = useState('');
  const [confirm, setConfirm] = useState('');
  const [error, setError] = useState('');
  const [working, setWorking] = useState(false);
  const requestVersion = useRef(0);

  const refresh = useCallback(async () => {
    const version = ++requestVersion.current;
    try {
      const result = await adminApi('/api/admin/auth/session');
      if (version === requestVersion.current) { setSession(result); setError(''); }
    } catch (cause) {
      if (version === requestVersion.current) {
        if (cause.status === 401) setSession(null);
        setError(cause.message);
      }
    } finally {
      if (version === requestVersion.current) setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
    const expired = () => setSession((value) => ({ ...value, password_change_required: true }));
    const timer = window.setInterval(refresh, 15_000);
    window.addEventListener('admin-auth-changed', refresh);
    window.addEventListener('admin-password-expired', expired);
    window.addEventListener('focus', refresh);
    return () => {
      ++requestVersion.current;
      window.clearInterval(timer);
      window.removeEventListener('admin-auth-changed', refresh);
      window.removeEventListener('admin-password-expired', expired);
      window.removeEventListener('focus', refresh);
    };
  }, [refresh]);

  useEffect(() => { refresh(); }, [pathname, refresh]);
  useEffect(() => {
    if (!session?.password_expires_at || session.password_change_required) return undefined;
    const timer = window.setTimeout(() => {
      setSession((value) => ({ ...value, password_change_required: true }));
    }, Math.max(0, Date.parse(session.password_expires_at) - Date.now()));
    return () => window.clearTimeout(timer);
  }, [session]);

  async function submit(event) {
    event.preventDefault(); setError('');
    if (next !== confirm) { setError('Mật khẩu xác nhận không khớp.'); return; }
    setWorking(true);
    try {
      await adminApi('/api/admin/auth/password', {
        method: 'POST', body: JSON.stringify({ current_password: current, new_password: next }),
      });
      setCurrent(''); setNext(''); setConfirm('');
      await refresh();
    } catch (cause) { setError(cause.message); }
    finally { setWorking(false); }
  }

  async function logout() {
    setWorking(true);
    try {
      await adminApi('/api/admin/auth/logout', { method: 'POST' });
      ++requestVersion.current;
      setSession(null); setCurrent(''); setNext(''); setConfirm('');
      navigate('/admin');
    } catch (cause) { setError(cause.message); }
    finally { setWorking(false); }
  }

  if (loading) return <div className="card" role="status">{t('admin.processing')}</div>;
  if (!session?.password_change_required) return <>
    {session?.password_expires_at && <p className="admin-notice">Mật khẩu cần được đổi trước {new Date(session.password_expires_at).toLocaleTimeString('vi-VN')} (chu kỳ 5 phút).</p>}
    {children}
  </>;
  return <section className="card admin-login">
    <h2>Bắt buộc đổi mật khẩu</h2>
    <p role="alert">Mật khẩu đã hết hạn sau 5 phút. Hãy đổi mật khẩu để tiếp tục quản trị.</p>
    <form className="admin-form" onSubmit={submit}>
      <label>{t('admin.passwordCurrent')}<input type="password" autoComplete="current-password" value={current} onChange={(event) => setCurrent(event.target.value)} required /></label>
      <label>{t('admin.passwordNew')}<input type="password" autoComplete="new-password" minLength={12} maxLength={256} value={next} onChange={(event) => setNext(event.target.value)} required /></label>
      <label>Xác nhận mật khẩu mới<input type="password" autoComplete="new-password" minLength={12} maxLength={256} value={confirm} onChange={(event) => setConfirm(event.target.value)} required /></label>
      <p>Mật khẩu mới cần ít nhất 12 ký tự và khác mật khẩu hiện tại.</p>
      {error && <p role="alert">{error}</p>}
      <div className="admin-actions"><button className="btn" disabled={working}>{working ? t('admin.processing') : t('admin.update')}</button><button type="button" className="btn btn-secondary" disabled={working} onClick={logout}>{t('admin.logout')}</button></div>
    </form>
  </section>;
}
