

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
