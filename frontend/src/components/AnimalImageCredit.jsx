import React from 'react';
import credits from '../../../data/dataset/demo_image_credits.json';

export default function AnimalImageCredit({ src, linked = true }) {
  const credit = Object.values(credits).find((item) => item.local_path === src);
  if (!credit) return null;
  const author = (credit.artist || credit.artist_html || '').replace(/<[^>]+>/g, '').trim();
  return <small className="animal-image-credit">© {author} · {linked ? <><a href={credit.file_page} target="_blank" rel="noreferrer">Wikimedia Commons</a> · <a href={credit.license_url || credit.file_page} target="_blank" rel="noreferrer">{credit.license}</a></> : credit.license}</small>;
}
