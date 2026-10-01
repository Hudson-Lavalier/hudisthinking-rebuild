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

  // --- Shadow Confetti Falling Particle Burst ---
  function spawnShadowConfetti() {
    const confettiContainer = document.getElementById('shadow-confetti');
    if (!confettiContainer) return;

    // Clear any previous confetti elements
    confettiContainer.innerHTML = '';

    const particleCount = 42;
    for (let i = 0; i < particleCount; i++) {
      const p = document.createElement('div');
      p.className = 'shadow-flake';

      // Random starting coordinates around the vortex center and screen
      const startX = 50 + (Math.random() - 0.5) * 60; // 20% to 80% screen width
      const startY = 35 + (Math.random() - 0.5) * 40; // 15% to 55% screen height
      
      // Fall trajectory offsets
      const driftX = (Math.random() - 0.5) * 220; // -110px to +110px horizontal drift
      const fallY = 160 + Math.random() * 320;     // falls 160px - 480px down
      const rotation = (Math.random() - 0.5) * 720;
      
      // Particle physical dimensions (irregular dark shards / ash confetti)
      const sizeW = 3 + Math.random() * 8;
      const sizeH = 4 + Math.random() * 12;
      const opacity = 0.55 + Math.random() * 0.45;
      const animDuration = 0.35 + Math.random() * 0.35; // 0.35s - 0.7s
      const delay = Math.random() * 0.08;

      p.style.cssText = `
        left: ${startX}vw;
        top: ${startY}vh;
        width: ${sizeW}px;
        height: ${sizeH}px;
        --drift-x: ${driftX}px;
        --fall-y: ${fallY}px;
        --rot: ${rotation}deg;
        --target-opacity: ${opacity};
        animation-duration: ${animDuration}s;
        animation-delay: ${delay}s;
      `;

      confettiContainer.appendChild(p);
    }

    // Clean up particles after animation completes
    setTimeout(() => {
      if (confettiContainer) confettiContainer.innerHTML = '';
    }, 800);
  }

  // Hook into Swup transition start
  swup.hooks.on('visit:start', () => {
    spawnShadowConfetti();
  });

  // Hook into Swup page replacement
  swup.hooks.on('content:replace', () => {
    initPageFeatures();
  });

  // Initial execution
  initPageFeatures();
});
