import fs from 'node:fs/promises';
import QRCode from '../frontend/node_modules/qrcode/lib/index.js';

const [url, output] = process.argv.slice(2);
if (!url || !output || !/^https:\/\//.test(url)) {
  throw new Error('Usage: node scripts/write_demo_qr.mjs https://demo-url output.svg');
}
await QRCode.toFile(output, url, { errorCorrectionLevel: 'Q', margin: 3, width: 640 });
console.log(output);
