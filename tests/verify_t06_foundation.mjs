import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');

console.log('--- Verifying Task T06: PWA / Service Worker / IndexedDB Foundation ---');

// 1. Verify files exist
const requiredFiles = [
  'frontend/public/sw.js',
  'frontend/public/manifest.json',
  'frontend/src/sw/registerServiceWorker.js',
  'frontend/src/db/indexedDB.js',
  'frontend/src/services/cacheStorage.js',
  'frontend/src/services/networkStatus.js',
];

let allFilesExist = true;
for (const relPath of requiredFiles) {
  const fullPath = path.join(projectRoot, relPath);
  if (fs.existsSync(fullPath)) {
    console.log(`[PASS] File exists: ${relPath}`);
  } else {
    console.error(`[FAIL] Missing file: ${relPath}`);
    allFilesExist = false;
  }
}

if (!allFilesExist) {
  process.exit(1);
}

// 2. Verify Service Worker content
const swContent = fs.readFileSync(path.join(projectRoot, 'frontend/public/sw.js'), 'utf8');
const swChecks = [
  { desc: 'Install listener', pattern: /addEventListener\(\s*['"]install['"]/ },
  { desc: 'Activate listener', pattern: /addEventListener\(\s*['"]activate['"]/ },
  { desc: 'Fetch listener', pattern: /addEventListener\(\s*['"]fetch['"]/ },
  { desc: 'Precache URLs', pattern: /['"]\/index\.html['"]/ },
  { desc: 'SPA Navigation fallback', pattern: /mode\s*===\s*['"]navigate['"]/ },
];

for (const check of swChecks) {
  if (check.pattern.test(swContent)) {
    console.log(`[PASS] Service Worker: ${check.desc}`);
  } else {
    console.error(`[FAIL] Service Worker missing: ${check.desc}`);
    process.exit(1);
  }
}

// 3. Verify module exports
async function verifyExports() {
  const dbModule = await import('../frontend/src/db/indexedDB.js');
  if (typeof dbModule.openDatabase === 'function' &&
      typeof dbModule.getItem === 'function' &&
      typeof dbModule.setItem === 'function' &&
      typeof dbModule.deleteItem === 'function' &&
      typeof dbModule.getAllItems === 'function' &&
      typeof dbModule.clearStore === 'function' &&
      typeof dbModule.verifyIndexedDB === 'function' &&
      dbModule.STORES && dbModule.STORES.POIS) {
    console.log('[PASS] IndexedDB module exports all required CRUD and store definitions.');
  } else {
    console.error('[FAIL] IndexedDB module exports incomplete.');
    process.exit(1);
  }

  const cacheModule = await import('../frontend/src/services/cacheStorage.js');
  if (typeof cacheModule.putInCache === 'function' &&
      typeof cacheModule.getFromCache === 'function' &&
      typeof cacheModule.removeFromCache === 'function' &&
      typeof cacheModule.clearCache === 'function' &&
      typeof cacheModule.verifyCacheStorage === 'function' &&
      cacheModule.CACHE_NAMES && cacheModule.CACHE_NAMES.AUDIO) {
    console.log('[PASS] CacheStorage module exports all required helper functions and cache names.');
  } else {
    console.error('[FAIL] CacheStorage module exports incomplete.');
    process.exit(1);
  }

  const swModule = await import('../frontend/src/sw/registerServiceWorker.js');
  if (typeof swModule.registerServiceWorker === 'function' &&
      typeof swModule.unregisterServiceWorker === 'function') {
    console.log('[PASS] Service Worker registration module exports properly.');
  } else {
    console.error('[FAIL] Service Worker registration module exports incomplete.');
    process.exit(1);
  }

  const netModule = await import('../frontend/src/services/networkStatus.js');
  if (typeof netModule.isOnline === 'function' &&
      typeof netModule.subscribeNetworkStatus === 'function') {
    console.log('[PASS] Network status module exports properly.');
  } else {
    console.error('[FAIL] Network status module exports incomplete.');
    process.exit(1);
  }
}

await verifyExports();
console.log('--- All T06 Foundation checks PASSED successfully! ---');

