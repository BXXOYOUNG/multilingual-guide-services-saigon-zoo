import React, { useEffect, useRef, useState } from 'react';
import AnimalImageCredit from '../AnimalImageCredit';
import { Link } from 'react-router-dom';
import { QRCodeSVG } from 'qrcode.react';
import { useTranslation } from '../../features/localization/useTranslation';

const animals = [
  { nameKey: 'animal.elephant', noteKey: 'animal.elephant.note', candidateCode: 'TCV-AN-005', image: '/images/animals/tcv-an-005.jpg', source: 'Charles J. Sharp / CC BY-SA 4.0' },
  { nameKey: 'animal.tiger', noteKey: 'animal.tiger.note', image: '/images/animals/bengal-tiger.jpg', source: 'Gary M. Stolz / U.S. Fish and Wildlife Service' },
  { nameKey: 'animal.giraffe', noteKey: 'animal.giraffe.note', candidateCode: 'TCV-AN-011', image: '/images/animals/tcv-an-011.jpg', source: 'Byrdyak / CC BY-SA 4.0' },
  { nameKey: 'animal.hippo', noteKey: 'animal.hippo.note', candidateCode: 'TCV-AN-001', image: '/images/animals/tcv-an-001.jpg', source: 'Giles Laurent / CC BY-SA 4.0' },
];
const offlinePackages = [
  { language: 'vi', label: 'Tiếng Việt', id: '6ad77ec98e1fe8641925e75e' },
  { language: 'en', label: 'English', id: '6ad776328e1fe8641925e759' },
  { language: 'fr', label: 'Français', id: '6ad77ece8e1fe8641925e75f' },
  { language: 'zh-Hans', label: '中文', id: '6ad77ed48e1fe8641925e760' },
  { language: 'ja', label: '日本語', id: '6ad77ed98e1fe8641925e761' },
  { language: 'ko', label: '한국어', id: '6ad77edf8e1fe8641925e762' },
];

export default function HomeView() {
  const { t, language } = useTranslation();
  const [catalog, setCatalog] = useState(null);
  const [selectedAnimal, setSelectedAnimal] = useState(null);
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

  const moveCarousel = (direction) => carouselRef.current?.scrollBy({ left: direction * Math.min(360, carouselRef.current.clientWidth * .78), behavior: 'smooth' });
  const mapId = (animal) => catalog?.find((entry) => animal.candidateCode && entry.candidate_code === animal.candidateCode)?.id;

  return <div className="home-page">
    <section className="home-hero home-hero-modern">
      <div className="home-hero-copy"><span className="eyebrow">{t('home.newEyebrow')}</span><h1>{t('home.newTitle')}</h1><p>{t('home.newDescription')}</p>
        <div className="home-hero-actions"><Link className="btn hero-primary" to="/map">{t('home.ctaMap')} <span aria-hidden="true">↗</span></Link><Link className="btn hero-secondary" to="/itinerary">{t('home.ctaRoute')}</Link></div>
        <span className="home-scroll-note">{t('home.scrollHint')} <span aria-hidden="true">↓</span></span>
      </div>
      <div className="home-hero-visual"><img src="/images/animals/tcv-an-005.jpg" alt={t('animal.elephant')} /><div className="hero-image-caption">{t('home.caption')}</div><div className="hero-visit-note"><strong>1864</strong><span>Saigon Zoo<br />& Botanical Gardens</span></div></div>
      <div className="hero-glow" aria-hidden="true" />
    </section>

    <section className="home-section animal-section home-carousel-section">
      <div className="section-heading"><div><span className="eyebrow">{t('home.meet')}</span><h2>{t('home.carouselTitle')}</h2><p className="section-subtitle">{t('home.carouselDesc')}</p></div><div className="carousel-controls"><button type="button" aria-label="Previous animals" onClick={() => moveCarousel(-1)}>←</button><button type="button" aria-label="Next animals" onClick={() => moveCarousel(1)}>→</button></div></div>
      <div className="animal-carousel" ref={carouselRef}>{animals.map((animal, index) => <button type="button" className="animal-card animal-carousel-card" key={animal.nameKey} onClick={() => setSelectedAnimal({ kind: 'featured', animal })} aria-label={t(animal.nameKey)}>
        <div className="animal-photo"><img src={animal.image} alt={t(animal.nameKey)} loading="lazy" /><span className="photo-number">0{index + 1}</span></div>
        <div className="animal-info"><div><h3>{t(animal.nameKey)}</h3><p>{t(animal.noteKey)}</p></div><span className="animal-arrow" aria-hidden="true">↗</span></div>
      </button>)}</div>
    </section>

    <section className="home-section listen-section"><div className="section-heading"><div><span className="eyebrow">{t('home.listenEyebrow')}</span><h2>{t('home.listenTitle')}</h2></div></div>
      <div className="listening-grid">
        <article className="listening-card listening-card-dark"><span className="listening-number">01</span><h3>{t('home.listenWebTitle')}</h3><p>{t('home.listenWebBody')}</p><Link to="/map">{t('nav.map')} <span>↗</span></Link></article>
        <article className="listening-card"><span className="listening-number">02</span><h3>{t('home.listenArrivalTitle')}</h3><p>{t('home.listenArrivalBody')}</p><Link to="/map">{t('nav.map')} <span>↗</span></Link></article>
        <article className="listening-card"><span className="listening-number">03</span><h3>{t('home.listenOfflineTitle')}</h3><p>{t('home.listenOfflineBody')}</p><Link to="/explore">{t('home.qrAction')} <span>↗</span></Link></article>
      </div>
      <Link className="inline-guide-link" to="/guide#offline">{t('home.howLink')} <span>↗</span></Link>
    </section>

    <section className="home-section offline-section" id="offline-download"><div className="offline-copy"><span className="eyebrow">{t('home.qrEyebrow')}</span><h2>{t('home.qrTitle')}</h2><p>{t('home.qrDescription')}</p><Link className="btn hero-primary" to="/explore">{t('home.qrAction')} <span>↗</span></Link><small>{t('home.qrHint')}</small></div>
      <div className="offline-qr-track">{offlinePackages.map((pack) => <article className="offline-qr-card" key={pack.language}><QRCodeSVG value={`TCV-PACKAGE:${pack.id}`} size={106} level="M" includeMargin /><strong>{pack.label}</strong><Link to={`/explore?package=${pack.id}`}>{t('explore.downloadPackage')}</Link></article>)}</div>
    </section>

    <section className="home-section route-feature"><div><span className="eyebrow">{t('home.routeEyebrow')}</span><h2>{t('home.routeTitle')}</h2><p>{t('home.routeDescription')}</p><Link className="btn hero-primary" to="/itinerary">{t('home.routeAction')} <span>↗</span></Link></div><div className="route-feature-art"><span className="route-line" /><span className="route-point route-point-one">01</span><span className="route-point route-point-two">02</span><span className="route-point route-point-three">03</span><small>Saigon Zoo · Suggested walk</small></div></section>

    <section className="home-section guide-promo"><div><span className="eyebrow">SAIGON ZOO GUIDE</span><h2>{t('home.guideTitle')}</h2><p>{t('home.guideDescription')}</p></div><Link className="btn btn-secondary" to="/guide">{t('nav.help')} <span>↗</span></Link></section>

    {catalog?.length > 0 && <section className="home-section species-index"><div className="section-heading"><div><span className="eyebrow">{t('home.catalog')}</span><h2>{catalog.length} {t('home.animals')}</h2></div></div><div className="species-list species-gallery">{catalog.map((animal) => <button type="button" className="species-row" key={animal.id} onClick={() => setSelectedAnimal({ kind: 'catalog', animal })}><div className="species-photo">{animal.image_url && <img src={animal.image_url} alt={animal.name} loading="lazy" decoding="async" onError={(event) => { event.currentTarget.style.visibility = 'hidden'; }} />}<span className="species-photo-label">{animal.name}</span></div><div className="species-card-copy"><AnimalImageCredit src={animal.image_url} linked={false} /><div className="species-row-heading"><div><h3>{animal.name}</h3><em>{animal.scientific_name}</em></div><span className={`species-map-status ${animal.map_available ? 'available' : ''}`}>{animal.map_available ? t('home.mapAvailable') : t('home.mapUnavailable')}</span></div><p>{animal.description}</p><span className="species-row-action">{t('home.viewDetails')} <span aria-hidden="true">→</span></span></div></button>)}</div></section>}

    {selectedAnimal && <div className="animal-detail-backdrop" role="presentation" onClick={() => setSelectedAnimal(null)}><section className="animal-detail-dialog" role="dialog" aria-modal="true" aria-labelledby="animal-detail-title" onClick={(event) => event.stopPropagation()}>
      <button type="button" className="animal-detail-close" aria-label={t('admin.close')} onClick={() => setSelectedAnimal(null)}>×</button>{selectedAnimalImage && <img src={selectedAnimalImage} alt={selectedAnimalName} />}
      <div className="animal-detail-copy"><span className="eyebrow">{t('home.meet')}</span><h2 id="animal-detail-title">{selectedAnimalName}</h2>{selectedAnimalInfo?.scientific_name && <em>{selectedAnimalInfo.scientific_name}</em>}<p>{selectedAnimalDescription}</p><AnimalImageCredit src={selectedAnimalImage} />{(selectedCatalogAnimal?.map_available || mapId(selectedFeaturedAnimal || {})) ? <Link className="btn animal-map-link" to={selectedCatalogAnimal ? `/map?poi=${selectedCatalogAnimal.id}` : mapId(selectedFeaturedAnimal) ? `/map?poi=${mapId(selectedFeaturedAnimal)}` : '/map'} onClick={() => setSelectedAnimal(null)}>{t('home.viewMap')} <span>↗</span></Link> : <p>{t('home.mapUnavailable')}</p>}</div>
    </section></div>}
  </div>;
}
