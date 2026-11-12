/* ==========================================================================
   Service Worker for Esco AV Interview Simulation (PWA)
   - Fast cross-platform caching (App Shell, CDNs, Fonts, Data)
   - Stale-While-Revalidate for core assets
   - Network-First with offline fallback for navigation
   - HTTP Range (206) support for offline audio/video playback
   ========================================================================== */

const CACHE_NAME = 'esco-av-pwa-v1';

// App Shell & Static Assets to Precache
const PRECACHE_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon.svg',
  './icon-192.png',
  './icon-512.png',
  './interview_data.json',
  './interview_script.json',
  // Essential CDN dependencies
  'https://cdn.tailwindcss.com',
  'https://unpkg.com/lucide@latest',
  'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&family=JetBrains+Mono:wght@400;500;600;700&display=swap'
];

// Install: precache critical assets safely
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      // Use allSettled so individual external failures don't block install
      return Promise.allSettled(
        PRECACHE_ASSETS.map((url) =>
          cache.add(url).catch((err) => {
            console.warn('[SW] Precache item failed:', url, err);
          })
        )
      );
    }).then(() => self.skipWaiting())
  );
});

// Activate: clean obsolete caches and take immediate control
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

// Helper: Handle HTTP Range requests for offline media (audio/video)
async function handleRangeRequest(request) {
  try {
    const networkResponse = await fetch(request);
    // If online and request was 200 (or if media was requested without range), cache full response
    if (networkResponse.ok && networkResponse.status === 200) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request.url, networkResponse.clone());
    }
    return networkResponse;
  } catch (err) {
    // Offline fallback for Range requests from cached full media
    const cache = await caches.open(CACHE_NAME);
    const cachedResponse = await cache.match(request.url);
    if (!cachedResponse) {
      return new Response('Media offline unavailable', { status: 503, statusText: 'Service Unavailable' });
    }
    const rangeHeader = request.headers.get('range');
    if (!rangeHeader) {
      return cachedResponse;
    }
    const arrayBuffer = await cachedResponse.arrayBuffer();
    const bytesMatch = rangeHeader.match(/bytes=(\d+)-(\d+)?/);
    if (!bytesMatch) {
      return cachedResponse;
    }
    const total = arrayBuffer.byteLength;
    const start = parseInt(bytesMatch[1], 10);
    const end = bytesMatch[2] ? parseInt(bytesMatch[2], 10) : total - 1;
    const sliced = arrayBuffer.slice(start, end + 1);

    return new Response(sliced, {
      status: 206,
      statusText: 'Partial Content',
      headers: {
        'Content-Type': cachedResponse.headers.get('Content-Type') || 'audio/mpeg',
        'Content-Range': `bytes ${start}-${end}/${total}`,
        'Content-Length': sliced.byteLength,
        'Accept-Ranges': 'bytes'
      }
    });
  }
}

// Fetch router
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // 1. Media handling (mp3, mp4, or range header)
  const isMedia = request.headers.has('range') ||
                  request.destination === 'audio' ||
                  request.destination === 'video' ||
                  url.pathname.endsWith('.mp3') ||
                  url.pathname.endsWith('.mp4');

  if (isMedia) {
    event.respondWith(handleRangeRequest(request));
    return;
  }

  // 2. Navigation requests (HTML pages) -> Network-First with Cache Fallback
  if (request.mode === 'navigate' || request.destination === 'document') {
    event.respondWith(
      fetch(request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.ok) {
            const clone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
          }
          return networkResponse;
        })
        .catch(async () => {
          const cached = await caches.match(request);
          if (cached) return cached;
          return caches.match('./index.html');
        })
    );
    return;
  }

  // 3. Static assets, fonts, CDNs, JSON -> Stale-While-Revalidate
  event.respondWith(
    caches.match(request).then((cachedResponse) => {
      const fetchPromise = fetch(request).then((networkResponse) => {
        if (networkResponse && (networkResponse.ok || networkResponse.type === 'opaque')) {
          const clone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
        }
        return networkResponse;
      }).catch((err) => {
        // Network failed; if we have cached response it will be used
        return cachedResponse;
      });

      return cachedResponse || fetchPromise;
    })
  );
});

// Immediate skip waiting on message
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
