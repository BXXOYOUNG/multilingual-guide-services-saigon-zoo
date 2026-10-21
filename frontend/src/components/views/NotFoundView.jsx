import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from '../../features/localization/useTranslation';

export default function NotFoundView() {
  const { t } = useTranslation();
  return <div className="card" style={{ textAlign: 'center' }}><h2>404 · {t('page.notFound')}</h2><p style={{ marginBottom: 16 }}>{t('page.notFoundBody')}</p><Link to="/" className="btn">{t('page.home')}</Link></div>;
}
