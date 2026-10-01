/**
 * HudIsThinking - Atmospheric Background Firefly Wisps
 * Monochromatic soft glowing embers drifting organically in the deep black background.
 * Lightweight, non-intrusive, zero dependencies.
 */
(function () {
  const canvas = document.getElementById('wisp-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width, height;
  let wisps = [];
  const WISP_COUNT = 45;

  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  }

  function createWisp() {
    return {
      x: Math.random() * (width || window.innerWidth),
      y: Math.random() * (height || window.innerHeight),
      vx: (Math.random() - 0.5) * 0.45,
      vy: -0.2 - Math.random() * 0.45, // Gentle upward/ambient drift
      radius: 1.2 + Math.random() * 2.2,
      glowRadius: 10 + Math.random() * 20,
      baseAlpha: 0.15 + Math.random() * 0.65,
      pulseSpeed: 0.015 + Math.random() * 0.03,
      pulseOffset: Math.random() * Math.PI * 2,
      wanderAngle: Math.random() * Math.PI * 2,
      wanderSpeed: 0.01 + Math.random() * 0.02,
    };
  }

  function init() {
    resize();
    wisps = [];
    for (let i = 0; i < WISP_COUNT; i++) {
      wisps.push(createWisp());
    }
  }

  let animationFrameId;

  function render(time) {
    ctx.clearRect(0, 0, width, height);

    for (let i = 0; i < wisps.length; i++) {
      const w = wisps[i];

      // Subtle organic wandering
      w.wanderAngle += w.wanderSpeed;
      w.x += w.vx + Math.cos(w.wanderAngle) * 0.25;
      w.y += w.vy + Math.sin(w.wanderAngle) * 0.15;

      // Wrap around screen boundaries seamlessly
      if (w.y < -30) {
        w.y = height + 20;
        w.x = Math.random() * width;
      } else if (w.y > height + 30) {
        w.y = -20;
      }
      if (w.x < -30) {
        w.x = width + 20;
      } else if (w.x > width + 30) {
        w.x = -20;
      }

      // Breathing / pulsating glow
      const currentAlpha = Math.max(
        0.05,
        w.baseAlpha * (0.6 + 0.4 * Math.sin(time * w.pulseSpeed + w.pulseOffset))
      );

      // Radial glow gradient for ethereal wisp effect
      const grad = ctx.createRadialGradient(
        w.x, w.y, 0,
        w.x, w.y, w.glowRadius
      );
      grad.addColorStop(0, `rgba(255, 255, 255, ${currentAlpha})`);
      grad.addColorStop(0.25, `rgba(235, 240, 255, ${currentAlpha * 0.5})`);
      grad.addColorStop(0.65, `rgba(200, 215, 255, ${currentAlpha * 0.15})`);
      grad.addColorStop(1, 'rgba(255, 255, 255, 0)');

      ctx.beginPath();
      ctx.arc(w.x, w.y, w.glowRadius, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();

      // Sharp central spark
      ctx.beginPath();
      ctx.arc(w.x, w.y, w.radius * 0.6, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 255, 255, ${Math.min(1, currentAlpha * 1.5)})`;
      ctx.fill();
    }

    animationFrameId = requestAnimationFrame(render);
  }

  // Handle visibility changes to save resources when tab is inactive
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      cancelAnimationFrame(animationFrameId);
    } else {
      animationFrameId = requestAnimationFrame(render);
    }
  });

  window.addEventListener('resize', resize);
  init();
  animationFrameId = requestAnimationFrame(render);
})();
