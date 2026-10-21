import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from '../../features/localization/useTranslation';

export default function GuideView() {
  const { t } = useTranslation();
  const sections = [
    ['website', 'guide.webTitle', 'guide.webBody', '01'],
    ['phone', 'guide.phoneTitle', 'guide.phoneBody', '02'],
    ['offline', 'guide.offlineTitle', 'guide.offlineBody', '03'],
    ['faq', 'guide.faqTitle', null, '04'],
    ['privacy', 'guide.privacyTitle', 'guide.privacyBody', '05'],
    ['content-manager', 'guide.adminTitle', 'guide.adminBody', '06'],
  ];
  return <div className="guide-page">
    <section className="subpage-hero guide-hero"><span className="eyebrow">{t('guide.eyebrow')}</span><h1>{t('guide.title')}</h1><p>{t('guide.description')}</p></section>
    <div className="guide-layout"><nav className="guide-toc" aria-label={t('guide.title')}>{sections.map(([id, title]) => <a href={`#${id}`} key={id}>{t(title)}</a>)}</nav>
      <div className="guide-content">{sections.map(([id, title, body, number]) => <section className="guide-section" id={id} key={id}><span className="guide-section-number">{number}</span><div><h2>{t(title)}</h2>{body && <p>{t(body)}</p>}
        {id === 'faq' && <div className="guide-faq">{[1, 2, 3].map((item) => <details key={item}><summary>{t(`guide.faq${item}q`)}</summary><p>{t(`guide.faq${item}a`)}</p></details>)}</div>}
        {id === 'offline' && <Link className="btn hero-primary" to="/explore">{t('home.qrAction')} <span>↗</span></Link>}
        {id === 'content-manager' && <Link className="btn btn-secondary" to="/admin">{t('guide.adminLink')} <span>↗</span></Link>}
      </div></section>)}</div>
    </div>
  </div>;
}
