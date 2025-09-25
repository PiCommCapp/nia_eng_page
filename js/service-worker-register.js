/**
 * NIA Engineering Portal - Service Worker Registration
 *
 * This script registers the service worker for offline capabilities.
 */

// Check if service workers are supported
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/js/service-worker.js')
      .then(registration => {
        console.log('Service worker registered successfully:', registration.scope);

        // Check for updates when page loads
        registration.update();

        // Handle service worker updates
        if (registration.waiting) {
          // If there's a waiting service worker, notify the user
          notifyUpdateAvailable();
        }

        // Listen for new service workers
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;

          // Track state changes
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              // New service worker available
              notifyUpdateAvailable();
            }
          });
        });
      })
      .catch(error => {
        console.error('Service worker registration failed:', error);
      });

    // Detect controller changes (service worker activated)
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      console.log('New service worker activated');
    });
  });
}

/**
 * Notify the user that an update is available
 */
function notifyUpdateAvailable() {
  // For now, just log to console
  // In a production app, we might show a notification to the user
  console.log('New version of the app is available! Refresh to update.');

  // You could add UI notification here:
  // const notification = document.createElement('div');
  // notification.className = 'update-notification';
  // notification.textContent = 'New version available! Refresh to update.';
  // document.body.appendChild(notification);
}

/**
 * Check network status and update UI accordingly
 */
function updateOnlineStatus() {
  const status = document.getElementById('online-status');
  if (status) {
    if (navigator.onLine) {
      status.textContent = 'Online';
      status.className = 'status-online';
    } else {
      status.textContent = 'Offline';
      status.className = 'status-offline';
    }
  }
}

// Listen for online/offline events
window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);

// Check status when page loads
window.addEventListener('load', updateOnlineStatus);
