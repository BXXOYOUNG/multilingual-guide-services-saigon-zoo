import React, { useEffect, useState } from 'react';
import { Outlet, NavLink, Link, useLocation } from 'react-router-dom';
import { useLanguage } from '../../features/localization/LanguageContext';
import { useTranslation } from '../../features/localization/useTranslation';
import { isOnline, subscribeNetworkStatus } from '../../services/networkStatus';
import BrandLogo from './BrandLogo';
import { trackEvent } from '../../services/analytics';

const links = [
  { to: '/', key: 'nav.home', end: true },
  { to: '/map', key: 'nav.map' },
  { to: '/explore', key: 'nav.explore' },
  { to: '/itinerary', key: 'nav.itinerary' },
  { to: '/guide', key: 'nav.help' },
];

export default function PublicLayout() {
  const { currentLanguageInfo, isLoadingLanguage, openLanguageSelector } = useLanguage();
  const { t, language } = useTranslation();
  const location = useLocation();
  const [online, setOnline] = useState(isOnline());
  const [menuOpen, setMenuOpen] = useState(false);
  const [scrollPercent, setScrollPercent] = useState(0);
  const [activeSection, setActiveSection] = useState('');

  useEffect(() => subscribeNetworkStatus(({ online: next }) => setOnline(next)), []);
  useEffect(() => {
    trackEvent({ event_type: 'session_start', language_code: language });
    trackEvent({ event_type: 'page_view', language_code: language });
    setMenuOpen(false);
  }, [location.pathname, language]);
  useEffect(() => {
    const heartbeat = () => { if (document.visibilityState === 'visible') trackEvent({ event_type: 'heartbeat', language_code: language }); };
    heartbeat();
    const timer = window.setInterval(heartbeat, 60_000);
    return () => window.clearInterval(timer);
  }, [language]);

  useEffect(() => {
    const handleScroll = () => {
      const total = document.documentElement.scrollHeight - window.innerHeight;
      if (total > 0) {
        setScrollPercent(Math.min(100, Math.max(0, (window.scrollY / total) * 100)));
      } else {
        setScrollPercent(0);
      }
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, [location.pathname]);

  useEffect(() => {
    if (location.pathname !== '/') {
      setActiveSection('');
      return undefined;
    }
    const sectionIds = ['hero', 'animals', 'audio', 'map', 'routes', 'offline', 'guide'];
    const elements = sectionIds.map((id) => document.getElementById(id)).filter(Boolean);
    if (!elements.length) return undefined;

    const observer = new IntersectionObserver((entries) => {
      const visible = entries.find((entry) => entry.isIntersecting);
      if (visible) {
        setActiveSection(visible.target.id);
      }
    }, { rootMargin: '-20% 0px -55% 0px', threshold: 0.1 });

    elements.forEach((el) => observer.observe(el));
    return () => observer.disconnect();
  }, [location.pathname]);

  const routeToSectionMap = {
    '/': 'hero',
    '/map': 'map',
    '/explore': 'offline',
    '/itinerary': 'routes',
    '/guide': 'guide',
  };

  const handleNavClick = (event, item) => {
    if (location.pathname === '/') {
      const targetSectionId = routeToSectionMap[item.to];
      if (targetSectionId) {
        const targetElement = document.getElementById(targetSectionId);
        if (targetElement) {
          event.preventDefault();
          setMenuOpen(false);
          const headerOffset = 74;
          const elementPosition = targetElement.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth',
          });
          window.history.replaceState(null, '', `#${targetSectionId}`);
        }
      }
    }
  };

  const isLinkActive = (item, isActive) => {
    if (location.pathname === '/') {
      if (item.to === '/map' && activeSection === 'map') return true;
      if (item.to === '/itinerary' && activeSection === 'routes') return true;
      if (item.to === '/explore' && activeSection === 'offline') return true;
      if (item.to === '/guide' && activeSection === 'guide') return true;
      if (item.to === '/' && (!activeSection || activeSection === 'hero' || activeSection === 'animals' || activeSection === 'audio')) return true;
      return false;
    }
    return isActive;
  };

  return <div className="app-container">
    <header className="site-header">
      <div className="scroll-progress-bar" style={{ width: `${scrollPercent}%` }} aria-hidden="true" />
      <Link className="site-brand" to="/" aria-label={t('app.name')}><BrandLogo /></Link>
      <nav className="site-nav" aria-label={t('nav.primary')}>
        {links.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.end}
            onClick={(e) => handleNavClick(e, item)}
            className={({ isActive }) => `site-nav-link ${isLinkActive(item, isActive) ? 'active is-active-section' : ''}`}
          >
            {t(item.key)}
          </NavLink>
        ))}
      </nav>
      <div className="header-tools">
        <button type="button" className="language-chip" onClick={openLanguageSelector} disabled={isLoadingLanguage} aria-label={t('app.language')}>
          {currentLanguageInfo?.nativeName || t('app.language')}
        </button>
        <span className={`connection-state ${online ? 'is-online' : 'is-offline'}`}><i />{online ? t('app.online') : t('app.offline')}</span>
      </div>
      <button type="button" className="mobile-menu-toggle" aria-expanded={menuOpen} aria-controls="mobile-site-nav" onClick={() => setMenuOpen((open) => !open)}>{menuOpen ? t('nav.closeMenu') : t('nav.menu')}</button>
      {menuOpen && <nav id="mobile-site-nav" className="mobile-site-nav" aria-label={t('nav.primary')}>
        {links.map((item) => <NavLink key={item.to} to={item.to} end={item.end} onClick={(e) => handleNavClick(e, item)} className={({ isActive }) => `site-nav-link ${isLinkActive(item, isActive) ? 'active is-active-section' : ''}`}>{t(item.key)}</NavLink>)}
      </nav>}
    </header>
    <div className="demo-mode-banner">{t('app.demoBanner')}</div>
    <main className="app-main"><Outlet /></main>
    <footer className="site-footer">
      <div className="footer-main"><div><Link className="site-brand footer-brand" to="/" aria-label={t('app.name')}><BrandLogo /></Link><p>{t('footer.tagline')}</p></div><div className="footer-links">{links.slice(1).map((item) => <Link key={item.to} to={item.to}>{t(item.key)}</Link>)}<Link to="/admin">{t('footer.contentManager')}</Link></div></div>
      <div className="footer-bottom"><span>{t('footer.demo')}</span><Link to="/guide#privacy">{t('guide.privacyTitle')}</Link></div>
    </footer>
  </div>;
}
