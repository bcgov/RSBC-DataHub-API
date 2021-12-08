importScripts("/precache-manifest.d9d54572567dc99ebe74dcee5b46f3c5.js", "https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js");



self.addEventListener("message", msg => {
    if (msg.data.action === 'SKIP_WAITING') self.skipWaiting();
})


// Remove all service workers
self.addEventListener("activate", function() {
    self.registration.unregister()
        .then(function() {
            return self.clients.matchAll(); })
        .then(function(clients) {
            clients.forEach(client => client.navigate(client.url));
        });
});

