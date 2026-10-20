/* 账本 Service Worker —— 页面走网络优先（保证能拿到新版），静态资源走缓存优先 */
const CACHE = 'ledger-2026-10-21';

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(['./index.html', './manifest.json', './icons/icon-192.png']))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

const isHTML = req =>
  req.mode === 'navigate' || (req.headers.get('accept') || '').indexOf('text/html') >= 0;

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;

  if (isHTML(req)) {
    /* 网络优先：更新后立刻生效；断网时回落到缓存 */
    e.respondWith(
      fetch(req).then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {});
        return res;
      }).catch(() => caches.match(req).then(hit => hit || caches.match('./index.html')))
    );
    return;
  }

  /* 其他资源：缓存优先 */
  e.respondWith(
    caches.match(req).then(hit => hit || fetch(req).then(res => {
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {});
      return res;
    }).catch(() => new Response('', { status: 504 })))
  );
});