import React, { lazy, Suspense, useEffect, useRef, useState } from 'react';
import AnimalImageCredit from '../AnimalImageCredit';
import { Link } from 'react-router-dom';
import { QRCodeSVG } from 'qrcode.react';
import { getItem, setItem, STORES } from '../../db/indexedDB';
import { useTranslation } from '../../features/localization/useTranslation';
import { loadPoisWithFallback } from '../../features/map/poiLoader';

const InteractiveMap = lazy(() => import('../../features/map/InteractiveMap'));

const animals = [
  { nameKey: 'animal.elephant', noteKey: 'animal.elephant.note', candidateCode: 'TCV-AN-005', image: '/images/animals/tcv-an-005.jpg', source: 'Charles J. Sharp / CC BY-SA 4.0' },
  { nameKey: 'animal.tiger', noteKey: 'animal.tiger.note', image: '/images/animals/bengal-tiger.jpg', source: 'Gary M. Stolz / U.S. Fish and Wildlife Service' },
  { nameKey: 'animal.giraffe', noteKey: 'animal.giraffe.note', candidateCode: 'TCV-AN-011', image: '/images/animals/tcv-an-011.jpg', source: 'Byrdyak / CC BY-SA 4.0' },
  { nameKey: 'animal.hippo', noteKey: 'animal.hippo.note', candidateCode: 'TCV-AN-001', image: '/images/animals/tcv-an-001.jpg', source: 'Giles Laurent / CC BY-SA 4.0' },
];


export default function HomeView() {
  const { t, language } = useTranslation();
  const [catalog, setCatalog] = useState(null);
  const [offlinePackages, setOfflinePackages] = useState([]);
  const [selectedAnimal, setSelectedAnimal] = useState(null);
  const [routePois, setRoutePois] = useState(null);
  const carouselRef = useRef(null);
  const selectedCatalogAnimal = selectedAnimal?.kind === 'catalog' ? selectedAnimal.animal : null;
  const selectedFeaturedAnimal = selectedAnimal?.kind === 'featured' ? selectedAnimal.animal : null;
  const selectedAnimalInfo = selectedCatalogAnimal || (selectedFeaturedAnimal ? catalog?.find((entry) => selectedFeaturedAnimal.candidateCode && entry.candidate_code === selectedFeaturedAnimal.candidateCode) : null);
  const selectedAnimalName = selectedAnimalInfo?.name || (selectedFeaturedAnimal ? t(selectedFeaturedAnimal.nameKey) : '');
  const selectedAnimalImage = selectedCatalogAnimal?.image_url || selectedFeaturedAnimal?.image;
  const selectedAnimalDescription = selectedAnimalInfo?.description || (selectedFeaturedAnimal ? t(selectedFeaturedAnimal.noteKey) : '');

  useEffect(() => {
    let mounted = true;
    fetch(`/api/pois/catalog?${new URLSearchParams({ language })}`).then((response) => {
      if (!response.ok) throw new Error('Catalog unavailable');
      return response.json();
    }).then((entries) => { if (mounted) setCatalog(entries); }).catch(() => { if (mounted) setCatalog(null); });
    return () => { mounted = false; };
  }, [language]);

  useEffect(() => {
    let mounted = true;
    let fetched = false;
    const labels = { vi: 'Tiếng Việt', en: 'English', fr: 'Français', 'zh-Hans': '简体中文', ja: '日本語', ko: '한국어' };
    const apply = (rows) => {
      const byLanguage = new Map();
      for (const row of rows || []) if (!byLanguage.has(row.language_code)) byLanguage.set(row.language_code, { ...row, language: row.language_code, label: labels[row.language_code] || row.language_code });
      if (mounted) setOfflinePackages([...byLanguage.values()]);
    };
    getItem(STORES.APP_STATE, 'public_audio_packages').then((rows) => { if (!fetched) apply(rows); }).catch(() => {});
    fetch('/audio/packages').then((response) => { if (!response.ok) throw new Error('Packages unavailable'); return response.json(); })
      .then((rows) => { fetched = true; apply(rows); return setItem(STORES.APP_STATE, rows, 'public_audio_packages'); }).catch(() => {});
    return () => { mounted = false; };
  }, []);

  useEffect(() => {
    let mounted = true;
    loadPoisWithFallback(language).then(({ pois: stops }) => {
      if (mounted) setRoutePois(stops.filter((poi) => Number.isFinite(poi.latitude) && Number.isFinite(poi.longitude)));
    }).catch(() => {
      if (mounted) setRoutePois([]);
    });
    return () => { mounted = false; };
  }, [language]);

  const routeOptions = [
    { title: t('itinerary.shortTitle'), description: t('itinerary.shortDesc'), stops: 3 },
    { title: t('itinerary.familyTitle'), description: t('itinerary.familyDesc'), stops: 5 },
    { title: t('itinerary.fullTitle'), description: t('itinerary.fullDesc'), stops: 8 },
  ];

  useEffect(() => {
    const revealElements = document.querySelectorAll('.scroll-reveal');
    if (!revealElements.length) return undefined;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    revealElements.forEach((el) => observer.observe(el));
    return () => observer.disconnect();
  }, [catalog, routePois]);

  const moveCarousel = (direction) => carouselRef.current?.scrollBy({ left: direction * Math.min(360, carouselRef.current.clientWidth * .78), behavior: 'smooth' });
  const mapId = (animal) => catalog?.find((entry) => animal.candidateCode && entry.candidate_code === animal.candidateCode)?.id;

  const scrollToSection = (event, targetId) => {
    event.preventDefault();
    const targetElement = document.getElementById(targetId);
    if (targetElement) {
      const headerOffset = 74;
      const elementPosition = targetElement.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth',
      });
      window.history.replaceState(null, '', `#${targetId}`);
    }
  };

  return <div className="home-page">
    {/* Section 01: Hero / Welcome */}
    <section id="hero" className="home-hero home-hero-modern">
      <div className="home-hero-copy"><span className="eyebrow">{t('home.newEyebrow')}</span><h1>{t('home.newTitle')}</h1><p>{t('home.newDescription')}</p>
        <div className="home-hero-actions"><a className="btn hero-primary" href="#map" onClick={(e) => scrollToSection(e, 'map')}>{t('home.ctaMap')} <span aria-hidden="true">↓</span></a><a className="btn hero-secondary" href="#routes" onClick={(e) => scrollToSection(e, 'routes')}>{t('home.ctaRoute')} <span aria-hidden="true">↓</span></a></div>
        <span className="home-scroll-note">{t('home.scrollHint')} <span aria-hidden="true">↓</span></span>
      </div>
      <div className="home-hero-visual"><img src="/images/animals/tcv-an-005.jpg" alt={t('animal.elephant')} /><div className="hero-image-caption">{t('home.caption')}</div><div className="hero-visit-note"><strong>1864</strong><span>Saigon Zoo<br />& Botanical Gardens</span></div></div>
      <div className="hero-glow" aria-hidden="true" />
    </section>

    {/* Section 02: Animal Discovery with Sticky Spotlight */}
    <section id="animals" className="home-section animal-section home-carousel-section scroll-reveal">
      <div className="section-heading"><div><span className="eyebrow">{t('home.meet')}</span><h2>{t('home.carouselTitle')}</h2><p className="section-subtitle">{t('home.carouselDesc')}</p></div><div className="carousel-controls"><button type="button" aria-label="Previous animals" onClick={() => moveCarousel(-1)}>←</button><button type="button" aria-label="Next animals" onClick={() => moveCarousel(1)}>→</button></div></div>
      
      {/* Desktop Sticky Storytelling Spotlight (960px+) */}
      <div className="sticky-story-container">
        <aside className="sticky-story-visual" aria-hidden="true">
          <img src={selectedFeaturedAnimal?.image || animals[0].image} alt="" />
          <div className="visual-caption">
            <h3>{selectedFeaturedAnimal ? t(selectedFeaturedAnimal.nameKey) : t(animals[0].nameKey)}</h3>
            <p>{selectedFeaturedAnimal ? t(selectedFeaturedAnimal.noteKey) : t(animals[0].noteKey)}</p>
          </div>
        </aside>

        <div className="sticky-story-feed">
          <div className="animal-carousel" ref={carouselRef}>{animals.map((animal, index) => <button type="button" className={`animal-card animal-carousel-card ${selectedFeaturedAnimal?.nameKey === animal.nameKey ? 'selected' : ''}`} key={animal.nameKey} onClick={() => setSelectedAnimal({ kind: 'featured', animal })} aria-label={t(animal.nameKey)}>
            <div className="animal-photo"><img src={animal.image} alt={t(animal.nameKey)} loading="lazy" /><span className="photo-number">0{index + 1}</span></div>
            <div className="animal-info"><div><h3>{t(animal.nameKey)}</h3><p>{t(animal.noteKey)}</p></div><span className="animal-arrow" aria-hidden="true">↗</span></div>
          </button>)}</div>
        </div>
      </div>
    </section>

    {/* Section 03: Audio Experience */}
    <section id="audio" className="home-section listen-section scroll-reveal"><div className="section-heading"><div><span className="eyebrow">{t('home.listenEyebrow')}</span><h2>{t('home.listenTitle')}</h2></div></div>
      <div className="listening-grid">
        <article className="listening-card listening-card-dark"><span className="listening-number">01</span><h3>{t('home.listenWebTitle')}</h3><p>{t('home.listenWebBody')}</p><a href="#map" onClick={(e) => scrollToSection(e, 'map')}>{t('nav.map')} <span>↓</span></a></article>
        <article className="listening-card"><span className="listening-number">02</span><h3>{t('home.listenArrivalTitle')}</h3><p>{t('home.listenArrivalBody')}</p><a href="#map" onClick={(e) => scrollToSection(e, 'map')}>{t('nav.map')} <span>↓</span></a></article>
        <article className="listening-card"><span className="listening-number">03</span><h3>{t('home.listenOfflineTitle')}</h3><p>{t('home.listenOfflineBody')}</p><a href="#offline" onClick={(e) => scrollToSection(e, 'offline')}>{t('home.qrAction')} <span>↓</span></a></article>
      </div>
      <Link className="inline-guide-link" to="/guide#offline">{t('home.howLink')} <span>↗</span></Link>
    </section>

    {/* Section 04: Interactive Map Section */}
    <section id="map" className="home-section map-section scroll-reveal">
      <div className="section-heading">
        <div><span className="eyebrow">{t('nav.map')}</span><h2>{t('home.ctaMap')}</h2><p className="section-subtitle">{t('map.demoCoordinateNotice')}</p></div>
        <Link className="btn btn-secondary" to="/map" style={{ borderRadius: '999px', fontSize: '0.8rem' }}>{t('map.openMap')} ↗</Link>
      </div>
      <div className="home-embedded-map" style={{ height: '560px', borderRadius: '24px', overflow: 'hidden', border: '1px solid var(--border-color)', position: 'relative' }}>
        <Suspense fallback={<div className="card" style={{ display: 'grid', placeItems: 'center', height: '100%' }}>{t('map.loading')}</div>}>
          <InteractiveMap language={language} />
        </Suspense>
      </div>
    </section>

    {/* Section 05: Suggested Routes */}
    <section id="routes" className="home-section routes-section scroll-reveal">
      <div className="section-heading">
        <div><span className="eyebrow">{t('itinerary.eyebrow')}</span><h2>{t('itinerary.title')}</h2><p className="section-subtitle">{t('itinerary.description')}</p></div>
        <Link className="btn btn-secondary" to="/itinerary" style={{ borderRadius: '999px', fontSize: '0.8rem' }}>{t('home.routeAction')} ↗</Link>
      </div>
      {routePois === null ? <div className="card">{t('map.loading')}</div> : routePois.length === 0 ? <div className="card">{t('itinerary.noPois')}</div> : <div className="itinerary-grid" style={{ padding: 0 }}>{routeOptions.map((route, index) => {
        const stops = routePois.slice(0, Math.min(route.stops, routePois.length));
        const first = stops[0];
        return <article className={`itinerary-card itinerary-card-${index + 1}`} key={route.title}>
          <div className="itinerary-card-top"><span className="itinerary-index">0{index + 1}</span><span>{t('itinerary.minutes', { count: stops.length * 12 })}</span></div>
          <h3>{route.title}</h3><p>{route.description}</p><div className="itinerary-stop-count">{t('itinerary.stops', { count: stops.length })}</div>
          <ol className="itinerary-stops">{stops.map((poi, stopIndex) => <li key={poi.id}><span>{String(stopIndex + 1).padStart(2, '0')}</span><Link to={`/map?poi=${poi.id}`}>{poi.name}</Link></li>)}</ol>
          <Link className="btn itinerary-start" to={first ? `/map?poi=${first.id}` : '/map'}>{t('itinerary.start')} <span>↗</span></Link>
        </article>;
      })}</div>}
    </section>

    {/* Section 06: Offline Audio Preparation */}
    <section className="home-section offline-section scroll-reveal" id="offline"><div className="offline-copy"><span className="eyebrow">{t('home.qrEyebrow')}</span><h2>{t('home.qrTitle')}</h2><p>{t('home.qrDescription')}</p><Link className="btn hero-primary" to="/explore">{t('home.qrAction')} <span>↗</span></Link><small>{t('home.qrHint')}</small></div>
      <div className="offline-qr-track">{offlinePackages.map((pack) => <article className="offline-qr-card" key={pack.language}><QRCodeSVG value={`TCV-PACKAGE:${pack.id}`} size={106} level="M" includeMargin /><strong>{pack.label}</strong><Link to={`/explore?package=${pack.id}`}>{t('explore.downloadPackage')}</Link></article>)}</div>
    </section>

    {/* Section 07: Getting Started / Visitor Guide */}
    <section id="guide" className="home-section guide-promo scroll-reveal" style={{ display: 'grid', gap: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
        <div><span className="eyebrow">SAIGON ZOO GUIDE</span><h2>{t('home.guideTitle')}</h2><p>{t('home.guideDescription')}</p></div>
        <Link className="btn btn-secondary" to="/guide">{t('nav.help')} <span>↗</span></Link>
      </div>
      <div className="guide-faq" style={{ marginTop: 0 }}>
        {[1, 2, 3].map((item) => <details key={item}><summary>{t(`guide.faq${item}q`)}</summary><p>{t(`guide.faq${item}a`)}</p></details>)}
      </div>
    </section>

    {catalog?.length > 0 && <section className="home-section species-index"><div className="section-heading"><div><span className="eyebrow">{t('home.catalog')}</span><h2>{catalog.length} {t('home.animals')}</h2></div></div><div className="species-list species-gallery">{catalog.map((animal) => <button type="button" className="species-row" key={animal.id} onClick={() => setSelectedAnimal({ kind: 'catalog', animal })}><div className="species-photo">{animal.image_url && <img src={animal.image_url} alt={animal.name} loading="lazy" decoding="async" onError={(event) => { event.currentTarget.style.visibility = 'hidden'; }} />}<span className="species-photo-label">{animal.name}</span></div><div className="species-card-copy"><AnimalImageCredit src={animal.image_url} linked={false} /><div className="species-row-heading"><div><h3>{animal.name}</h3><em>{animal.scientific_name}</em></div><span className={`species-map-status ${animal.map_available ? 'available' : ''}`}>{animal.map_available ? t('home.mapAvailable') : t('home.mapUnavailable')}</span></div><p>{animal.description}</p><span className="species-row-action">{t('home.viewDetails')} <span aria-hidden="true">→</span></span></div></button>)}</div></section>}

    {selectedAnimal && <div className="animal-detail-backdrop" role="presentation" onClick={() => setSelectedAnimal(null)}><section className="animal-detail-dialog" role="dialog" aria-modal="true" aria-labelledby="animal-detail-title" onClick={(event) => event.stopPropagation()}>
      <button type="button" className="animal-detail-close" aria-label={t('admin.close')} onClick={() => setSelectedAnimal(null)}>×</button>{selectedAnimalImage && <img src={selectedAnimalImage} alt={selectedAnimalName} />}
      <div className="animal-detail-copy"><span className="eyebrow">{t('home.meet')}</span><h2 id="animal-detail-title">{selectedAnimalName}</h2>{selectedAnimalInfo?.scientific_name && <em>{selectedAnimalInfo.scientific_name}</em>}<p>{selectedAnimalDescription}</p><AnimalImageCredit src={selectedAnimalImage} />{(selectedCatalogAnimal?.map_available || mapId(selectedFeaturedAnimal || {})) ? <Link className="btn animal-map-link" to={selectedCatalogAnimal ? `/map?poi=${selectedCatalogAnimal.id}` : mapId(selectedFeaturedAnimal) ? `/map?poi=${mapId(selectedFeaturedAnimal)}` : '/map'} onClick={() => setSelectedAnimal(null)}>{t('home.viewMap')} <span>↗</span></Link> : <p>{t('home.mapUnavailable')}</p>}</div>
    </section></div>}
  </div>;
}
