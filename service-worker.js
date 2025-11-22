const CACHE_NAME = 'gkg-v1';
const ASSETS = ['/', '/index.html', '/styles.css', '/script.js'];

self.addEventListener('install', (event) => {
	self.skipWaiting();
	event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)));
});

self.addEventListener('activate', (event) => {
	event.waitUntil(
		caches.keys().then((keys) =>
			Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
		)
	);
});

self.addEventListener('fetch', (event) => {
	const url = new URL(event.request.url);
	if (url.origin === location.origin) {
		event.respondWith(caches.match(event.request).then((cached) => cached || fetch(event.request)));
	}
});

