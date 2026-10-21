import fs from 'node:fs/promises';
import QRCode from '../frontend/node_modules/qrcode/lib/index.js';

const [output, offlinePackageId] = process.argv.slice(2);
if (!output) throw new Error('Usage: node scripts/write_demo_poi_qr_sheet.mjs output.html');
const response = await fetch('http://127.0.0.1:8000/api/pois?language=vi');
if (!response.ok) throw new Error(`Could not load demo POIs (${response.status})`);
const pois = await response.json();
if (pois.length !== 11) throw new Error(`Expected 11 demo POIs, received ${pois.length}`);
const cards = await Promise.all(pois.map(async (poi, index) => {
  const payload = `TCV-POI:${poi.id}`;
  const qr = await QRCode.toDataURL(payload, { errorCorrectionLevel: 'Q', margin: 2, width: 240 });
  const title = String(poi.name).replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
  return `<article class="qr-card"><img src="${qr}" alt="QR ${title}"><h2>${String(index + 1).padStart(2, '0')} · ${title}</h2><code>${payload}</code><p>Quét trong ứng dụng → Khám phá → Bật camera</p></article>`;
}));
if (offlinePackageId) {
  if (!/^[a-f\d]{24}$/i.test(offlinePackageId)) throw new Error('Offline package ID must be a MongoDB ObjectId');
  const payload = `TCV-PACKAGE:${offlinePackageId}`;
  const qr = await QRCode.toDataURL(payload, { errorCorrectionLevel: 'Q', margin: 2, width: 280 });
  cards.unshift(`<article class="qr-card package-card"><img src="${qr}" alt="English offline audio package QR"><h2>Gói audio offline · English</h2><code>${payload}</code><p>Trong app chọn English → Khám phá → Bật camera → quét mã.</p></article>`);
}
const html = `<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Saigon Zoo · Demo POI QR</title><style>*{box-sizing:border-box}body{font:15px/1.45 system-ui,sans-serif;margin:0;padding:24px;color:#23372c;background:#f5f4ee}header{max-width:1000px;margin:0 auto 20px}h1{margin:0 0 5px}header p{margin:0;color:#6a786e}.grid{max-width:1000px;margin:auto;display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.qr-card{padding:14px;background:#fff;border:1px solid #e1e4dc;border-radius:14px;text-align:center;break-inside:avoid}.qr-card img{width:180px;height:180px}.qr-card h2{font-size:16px;margin:4px}.qr-card code{font-size:10px;overflow-wrap:anywhere}.qr-card p{margin:6px 0 0;color:#68766d;font-size:12px}@media(max-width:680px){.grid{grid-template-columns:repeat(2,1fr)}}@media print{body{padding:0;background:white}.grid{grid-template-columns:repeat(3,1fr);gap:8px}.qr-card{border:1px solid #aaa;border-radius:0;padding:6px}.qr-card img{width:145px;height:145px}header{margin-bottom:8px}}}</style><header><h1>Saigon Zoo · Mã QR POI demo</h1><p>Dữ liệu mô phỏng để kiểm chứng luồng đa ngôn ngữ và phát audio. In trang này, sau đó trong app chọn Khám phá và quét từng mã.</p></header><main class="grid">${cards.join('')}</main></html>`;
await fs.writeFile(output, html, 'utf8');
console.log(`Wrote ${pois.length} POI QR codes to ${output}`);
