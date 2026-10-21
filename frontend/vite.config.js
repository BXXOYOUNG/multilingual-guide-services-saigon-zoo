import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const backendProxy = {
  '/api': { target: 'http://127.0.0.1:8000', changeOrigin: true },
  '/audio': { target: 'http://127.0.0.1:8000', changeOrigin: true },
};

export default defineConfig({
  plugins: [react(), {
    name: 'saigon-zoo-offline-precache',
    configureServer(server) {
      server.middlewares.use('/sw.js', (_request, response) => {
        response.setHeader('Content-Type', 'application/javascript; charset=utf-8');
        response.end(`const CACHE='saigon-zoo-shell-dev-v1';self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(['/','/manifest.json'])).then(()=>self.skipWaiting())));self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET'||new URL(r.url).origin!==location.origin)return;if(r.mode==='navigate'){e.respondWith(fetch(r).catch(async()=>((await caches.match(r))||(await caches.match('/')))));return;}if(['script','style','image','font','worker'].includes(r.destination)||new URL(r.url).pathname.startsWith('/node_modules/'))e.respondWith(caches.match(r).then(c=>c||fetch(r).then(x=>{if(x.ok)caches.open(CACHE).then(cache=>cache.put(r,x.clone()));return x;})));});`);
      });
    },
    generateBundle(_options, bundle) {
      const assets = Object.keys(bundle)
        .filter((file) => /\.(?:js|css|woff2?|ttf|png|jpe?g|svg|webp|ico)$/.test(file))
        .map((file) => `/${file}`);
      this.emitFile({
        type: 'asset',
        fileName: 'sw.js',
        source: `const CACHE='saigon-zoo-shell-v2';\nconst PRECACHE=${JSON.stringify(['/','/index.html','/manifest.json',...assets])};\nself.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(PRECACHE)).then(()=>self.skipWaiting())));\nself.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('saigon-zoo-shell-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));\nself.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET'||new URL(r.url).origin!==location.origin)return;if(r.mode==='navigate'){e.respondWith(fetch(r).catch(async()=>((await caches.match(r))||(await caches.match('/index.html')))));return;}if(r.destination==='script'||r.destination==='style'||r.destination==='image'||r.destination==='font'||r.destination==='worker'||new URL(r.url).pathname.startsWith('/assets/'))e.respondWith(caches.match(r).then(c=>c||fetch(r).then(x=>{if(x.ok){const copy=x.clone();caches.open(CACHE).then(cache=>cache.put(r,copy));}return x;})));});`,
      });
    },
  }],
  server: {
    port: 3000,
    host: '0.0.0.0',
    allowedHosts: ['.trycloudflare.com'],
    proxy: backendProxy,
  },
  preview: {
    host: '0.0.0.0',
    port: 3000,
    allowedHosts: ['.trycloudflare.com'],
    proxy: backendProxy,
  },
});
