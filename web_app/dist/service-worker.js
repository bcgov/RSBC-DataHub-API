importScripts("/roadside-forms/precache-manifest.4d5e1c4c501ae83ad5954a10076c99c6.js", "/roadside-forms/workbox-v4.3.1/workbox-sw.js");
workbox.setConfig({modulePathPrefix: "/roadside-forms/workbox-v4.3.1"});
self.__precacheManifest = [].concat(self.__precacheManifest || []);
workbox.precaching.precacheAndRoute(self.__precacheManifest, {
    ignoreURLParametersMatching: [/.*/]
});

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting()
  }
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
    url.pathname.includes('/api/v1/static/impound_lot_operators') ||
    url.pathname.includes('/api/v1/users') ||
    url.pathname.includes('/api/v1/user_roles'),
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


// Cache these API resources for 2 days
workbox.routing.registerRoute(({request, url}) =>
    url.pathname.includes('/api/v1/static/agencies') ||
    url.pathname.includes('/api/v1/static/cities') ||
    url.pathname.includes('/api/v1/static/configuration') ||
    url.pathname.includes('/api/v1/static/countries') ||
    url.pathname.includes('/api/v1/static/jurisdictions') ||
    url.pathname.includes('/api/v1/static/provinces') ||
    url.pathname.includes('/api/v1/static/vehicles') ||
    url.pathname.includes('/api/v1/static/vehicle_styles'),
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


// When the application is offline, queue any forms submitted
// to the API and resubmit when back online.
workbox.routing.registerRoute(({request, url}) =>
    url.pathname.includes('/api/v1/forms/'),
    new workbox.strategies.NetworkOnly({
        plugins: [
            new workbox.backgroundSync.Plugin('roadsafetyQueue', {
              maxRetentionTime: 24 * 60, // Retry for max of 24 Hours (specified in minutes)
            })
        ],
    }), 'PATCH');

