import React from 'react';
import { Outlet, Link, NavLink } from 'react-router-dom';
import BrandLogo from './BrandLogo';
import { useLanguage } from '../../features/localization/LanguageContext';
import { useTranslation } from '../../features/localization/useTranslation';

export default function AdminLayout() {
  const { currentLanguageInfo, isLoadingLanguage, openLanguageSelector } = useLanguage();
  const { t } = useTranslation();
  return <div className="admin-container">
    <header className="admin-header">
      <div className="admin-identity"><Link to="/" aria-label={t('app.name')}><BrandLogo /></Link><div><h2>{t('admin.title')}</h2><p>{t('admin.subtitle')}</p></div></div>
      <div className="admin-header-actions">
        <button type="button" className="btn btn-secondary" onClick={openLanguageSelector} disabled={isLoadingLanguage} aria-label={t('app.language')}>{currentLanguageInfo?.nativeName}</button>
        <Link to="/" className="btn btn-secondary">{t('admin.back')}</Link>
      </div>
    </header>
    <div className="demo-mode-banner">{t('app.demoBanner')}</div>
    <div className="admin-workspace"><aside className="admin-sidebar"><span className="eyebrow">WORKSPACE</span><nav aria-label={t('admin.title')}><NavLink to="/admin" end>{t('admin.poiContent')}</NavLink><NavLink to="/admin/analytics">{t('admin.analytics')}</NavLink><Link to="/guide#content-manager">{t('nav.help')}</Link></nav><div className="admin-sidebar-note"><span>TCV / AUDIO GUIDE</span><p>{t('admin.subtitle')}</p></div></aside><main className="admin-main"><Outlet /></main></div>
  </div>;
}
