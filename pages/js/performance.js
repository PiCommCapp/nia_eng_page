// Performance Monitoring for NIA Engineering Portal
// Tracks Core Web Vitals and other performance metrics

(function () {
  'use strict';

  // Performance monitoring configuration
  const config = {
    enabled: true,
    logToConsole: false,
    sendToAnalytics: false, // Set to true if you have analytics
    thresholds: {
      fcp: 1800, // First Contentful Paint (ms)
      lcp: 2500, // Largest Contentful Paint (ms)
      fid: 100, // First Input Delay (ms)
      cls: 0.1, // Cumulative Layout Shift
    },
  };

  // Performance data storage
  let performanceData = {
    fcp: null,
    lcp: null,
    fid: null,
    cls: null,
    loadTime: null,
    domContentLoaded: null,
  };

  // Initialize performance monitoring
  function initPerformanceMonitoring() {
    if (!config.enabled || !window.performance) return;

    // Track page load time
    trackPageLoadTime();

    // Track Core Web Vitals
    trackFirstContentfulPaint();
    trackLargestContentfulPaint();
    trackFirstInputDelay();
    trackCumulativeLayoutShift();

    // Track DOM content loaded
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function () {
        performanceData.domContentLoaded = performance.now();
        logPerformance('DOM Content Loaded', performanceData.domContentLoaded);
      });
    } else {
      performanceData.domContentLoaded = performance.now();
    }
  }

  // Track page load time
  function trackPageLoadTime() {
    window.addEventListener('load', function () {
      const loadTime = performance.now();
      performanceData.loadTime = loadTime;
      logPerformance('Page Load Time', loadTime);

      // Check if load time exceeds threshold
      if (loadTime > 3000) {
        logPerformance('WARNING: Slow page load', loadTime);
      }
    });
  }

  // Track First Contentful Paint
  function trackFirstContentfulPaint() {
    if ('PerformanceObserver' in window) {
      const observer = new PerformanceObserver(function (list) {
        const entries = list.getEntries();
        entries.forEach(function (entry) {
          if (entry.name === 'first-contentful-paint') {
            performanceData.fcp = entry.startTime;
            logPerformance('First Contentful Paint', entry.startTime);

            if (entry.startTime > config.thresholds.fcp) {
              logPerformance('WARNING: Slow FCP', entry.startTime);
            }
          }
        });
      });

      observer.observe({ entryTypes: ['paint'] });
    }
  }

  // Track Largest Contentful Paint
  function trackLargestContentfulPaint() {
    if ('PerformanceObserver' in window) {
      const observer = new PerformanceObserver(function (list) {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        performanceData.lcp = lastEntry.startTime;
        logPerformance('Largest Contentful Paint', lastEntry.startTime);

        if (lastEntry.startTime > config.thresholds.lcp) {
          logPerformance('WARNING: Slow LCP', lastEntry.startTime);
        }
      });

      observer.observe({ entryTypes: ['largest-contentful-paint'] });
    }
  }

  // Track First Input Delay
  function trackFirstInputDelay() {
    if ('PerformanceObserver' in window) {
      const observer = new PerformanceObserver(function (list) {
        const entries = list.getEntries();
        entries.forEach(function (entry) {
          performanceData.fid = entry.processingStart - entry.startTime;
          logPerformance('First Input Delay', performanceData.fid);

          if (performanceData.fid > config.thresholds.fid) {
            logPerformance('WARNING: High FID', performanceData.fid);
          }
        });
      });

      observer.observe({ entryTypes: ['first-input'] });
    }
  }

  // Track Cumulative Layout Shift
  function trackCumulativeLayoutShift() {
    if ('PerformanceObserver' in window) {
      let clsValue = 0;
      const observer = new PerformanceObserver(function (list) {
        const entries = list.getEntries();
        entries.forEach(function (entry) {
          if (!entry.hadRecentInput) {
            clsValue += entry.value;
          }
        });
        performanceData.cls = clsValue;
        logPerformance('Cumulative Layout Shift', clsValue);

        if (clsValue > config.thresholds.cls) {
          logPerformance('WARNING: High CLS', clsValue);
        }
      });

      observer.observe({ entryTypes: ['layout-shift'] });
    }
  }

  // Log performance metrics
  function logPerformance(metric, value) {
    if (config.logToConsole) {
      console.log(`[Performance] ${metric}: ${value}ms`);
    }

    // Send to analytics if configured
    if (config.sendToAnalytics && window.gtag) {
      gtag('event', 'performance_metric', {
        metric_name: metric,
        metric_value: value,
        page_location: window.location.href,
      });
    }
  }

  // Get performance summary
  function getPerformanceSummary() {
    return {
      ...performanceData,
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      connection: navigator.connection
        ? {
            effectiveType: navigator.connection.effectiveType,
            downlink: navigator.connection.downlink,
          }
        : null,
    };
  }

  // Export performance data to window for debugging
  window.getPerformanceData = getPerformanceSummary;

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPerformanceMonitoring);
  } else {
    initPerformanceMonitoring();
  }

  // Log performance summary after 5 seconds
  setTimeout(function () {
    const summary = getPerformanceSummary();
    if (config.logToConsole) {
      console.log('[Performance Summary]', summary);
    }
  }, 5000);
})();
