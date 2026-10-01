/**
 * HudIsThinking - Black Hole Void Navigation & Atmospheric Interactions
 * Gravitational singularity collapse on exit, event horizon bloom on entry.
 * Pure vanilla JavaScript. Zero framework overhead.
 */
(function () {
  'use strict';

  // 1. Create or ensure Void Portal Overlay exists
  let voidPortal = document.getElementById('void-portal');
  if (!voidPortal) {
    voidPortal = document.createElement('div');
    voidPortal.id = 'void-portal';
    voidPortal.className = 'void-portal-idle';
    document.body.appendChild(voidPortal);
  }

  // Handle page entry bloom
  function enterPageBloom() {
    voidPortal.className = 'void-portal-entering';
    setTimeout(() => {
      voidPortal.className = 'void-portal-idle';
    }, 280);
  }

  // Handle browser back-forward cache (bfcache)
  window.addEventListener('pageshow', (event) => {
    if (event.persisted) {
      voidPortal.className = 'void-portal-idle';
    } else {
      enterPageBloom();
    }
  });

  // 2. Intercept Internal Navigation Clicks
  document.addEventListener('click', (e) => {
    // Find closest anchor tag
    const link = e.target.closest('a');
    if (!link) return;

    const href = link.getAttribute('href');
    if (!href) return;

    // Ignore anchors, external links, javascript, downloads, new tabs, modifier keys
    if (
      href.startsWith('#') ||
      href.startsWith('javascript:') ||
      href.startsWith('mailto:') ||
      href.startsWith('tel:') ||
      link.hasAttribute('download') ||
      link.target === '_blank' ||
      e.ctrlKey ||
      e.metaKey ||
      e.shiftKey ||
      e.which === 2 // Middle click
    ) {
      return;
    }

    // Check same origin
    const targetUrl = new URL(link.href, window.location.href);
    if (targetUrl.origin !== window.location.origin) return;
    if (targetUrl.pathname === window.location.pathname && targetUrl.search === window.location.search) return;

    // Trigger Gravitational Singularity Collapse (~280ms)
    e.preventDefault();
    voidPortal.className = 'void-portal-collapsing';

    setTimeout(() => {
      window.location.href = link.href;
    }, 280);
  });

  // 3. Reading Horizon Progress Line
  const progressBar = document.getElementById('reading-progress');
  if (progressBar) {
    function updateScrollProgress() {
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (scrollHeight > 0) {
        const scrolled = (window.scrollY / scrollHeight) * 100;
        progressBar.style.width = Math.min(100, Math.max(0, scrolled)) + '%';
      }
    }
    window.addEventListener('scroll', updateScrollProgress, { passive: true });
    updateScrollProgress();
  }

  // 4. Terminal Typewriter Entrance for Headers
  const typewriterHeaders = document.querySelectorAll('.typewriter-entrance');
  typewriterHeaders.forEach((el) => {
    const originalText = el.innerText;
    el.style.opacity = '1';
    el.classList.add('typewriter-active');
  });

})();
