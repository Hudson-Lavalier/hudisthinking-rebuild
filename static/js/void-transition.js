/**
 * HudIsThinking - Swup PJAX Navigation & Black Hole Void Transitions
 * Persistent background canvas, continuous fireflies, zero reload flash.
 */
document.addEventListener('DOMContentLoaded', () => {
  // Verify Swup is available
  if (typeof Swup === 'undefined') {
    return;
  }

  const swup = new Swup({
    containers: ['#swup'],
    animateHistoryBrowsing: true,
    linkSelector: 'a[href^="/"]:not([data-no-swup]):not([download]):not([target="_blank"])',
  });

  // Re-initialization function called on initial load and every PJAX swap
  function initPageFeatures() {
    // 1. Reading Horizon Progress Line
    const progressBar = document.getElementById('reading-progress');
    if (progressBar) {
      const updateScrollProgress = () => {
        const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
        if (scrollHeight > 0) {
          const scrolled = (window.scrollY / scrollHeight) * 100;
          progressBar.style.width = Math.min(100, Math.max(0, scrolled)) + '%';
        }
      };
      window.addEventListener('scroll', updateScrollProgress, { passive: true });
      updateScrollProgress();
    }

    // 2. Dynamic Navigation Link Active Highlighting
    const currentPath = window.location.pathname;
    document.querySelectorAll('.site-nav .nav-link').forEach((link) => {
      const linkHref = link.getAttribute('href');
      if (linkHref === currentPath || (linkHref !== '/' && currentPath.startsWith(linkHref))) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });

    // 3. Instant scroll to top on page swap
    window.scrollTo({ top: 0, behavior: 'instant' });
  }

  // Hook into Swup page replacement
  swup.hooks.on('content:replace', () => {
    initPageFeatures();
  });

  // Initial execution
  initPageFeatures();

  // Gracefully suppress broken image frames
  window.addEventListener('error', (e) => {
    if (e.target && e.target.tagName === 'IMG') {
      e.target.style.display = 'none';
    }
  }, true);
});
