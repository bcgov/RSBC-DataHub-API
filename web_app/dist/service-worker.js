importScripts("/roadside-forms/precache-manifest.04174bb21b67c0ee961c0f77c07242c3.js", "https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js");


// The precaching code provided by Workbox
self.__precacheManifest = [].concat(self.__precacheManifest || []);
workbox.precaching.precacheAndRoute(self.__precacheManifest, {
    ignoreURLParametersMatching: [/.*/]
});

self.addEventListener("message", msg => {
    if (msg.data.action === 'SKIP_WAITING') self.skipWaiting();
})

// Cache CSS, JS, and Web Worker requests with a Stale While Revalidate strategy
workbox.routing.registerRoute(
  // Check to see if the request's destination is style for stylesheets, script for JavaScript, or worker for web worker
  ({ request }) =>
    request.destination === 'style' ||
    request.destination === 'script' ||
    request.destination === 'worker',
  // Use a Stale While Revalidate caching strategy
  new workbox.strategies.StaleWhileRevalidate({
    // Put all cached files in a cache named 'assets'
    cacheName: 'assets',
    plugins: [
      // Ensure that only requests that result in a 200 status are cached
      new workbox.cacheableResponse.Plugin({
        statuses: [200],
      }),
    ],
  }),
);

// Cache frequently changing API resources using "StaleWhileRevalidate" method
workbox.routing.registerRoute(({request, url}) =>
    url.pathname ===  '/roadside-forms/api/v1/impound_lot_operators'  ||
    url.pathname === '/roadside-forms/api/v1/users' ||
    url.pathname === '/roadside-forms/api/v1/user_roles',
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: 'dynamic-api',
    plugins: [
      // Ensure that only requests that result in a 200 status are cached
      new workbox.cacheableResponse.Plugin({
        statuses: [200],
      })
    ],
  }),
);


// Cache static API resources for 2 days
workbox.routing.registerRoute(({request, url}) =>
    url.pathname === '/roadside-forms/api/v1/agencies'  ||
    url.pathname === '/roadside-forms/api/v1/cities'  ||
    url.pathname === '/roadside-forms/api/v1/countries'  ||
    url.pathname === '/roadside-forms/api/v1/jurisdictions'  ||
    url.pathname === '/roadside-forms/api/v1/provinces'  ||
    url.pathname === '/roadside-forms/api/v1/vehicles'  ||
    url.pathname === '/roadside-forms/api/v1/vehicle_styles'  ||
    url.pathname === '/roadside-forms/api/v1/colors',
  new workbox.strategies.CacheFirst({
    cacheName: 'static-api',
    plugins: [
      // Ensure that only requests that result in a 200 status are cached
      new workbox.cacheableResponse.Plugin({
        statuses: [200],
      }),
      new workbox.expiration.Plugin({
        maxAgeSeconds: 60 * 60 * 24 * 2, // 2 Days
      }),
    ],
  }),
);
