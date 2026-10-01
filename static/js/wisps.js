/**
 * HudIsThinking - Atmospheric Background Firefly Wisps
 * Monochromatic soft glowing embers drifting organically in the deep black background
 * with Gravitational Cursor Lensing physics.
 * Lightweight, non-intrusive, zero dependencies.
 */
(function () {
  const canvas = document.getElementById('wisp-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width, height;
  let wisps = [];

  // Dynamic configuration from backend SiteConfiguration
  const countAttr = parseInt(canvas.getAttribute('data-count'), 10);
  const speedAttr = parseFloat(canvas.getAttribute('data-speed'));
  const WISP_COUNT = (!isNaN(countAttr) && countAttr > 0) ? countAttr : 16;
  const SPEED_SCALE = (!isNaN(speedAttr) && speedAttr > 0) ? (speedAttr / 0.08) : 1.0;

  // Mouse tracking for Gravitational Cursor Lensing
  let mouseX = -1000;
  let mouseY = -1000;
  let mouseActive = false;

  window.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    mouseActive = true;
  }, { passive: true });

  window.addEventListener('mouseleave', () => {
    mouseActive = false;
    mouseX = -1000;
    mouseY = -1000;
  });

  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  }

  function createWisp() {
    return {
      x: Math.random() * (width || window.innerWidth),
      y: Math.random() * (height || window.innerHeight),
      vx: ((Math.random() - 0.5) * 0.08) * SPEED_SCALE, // Scale horizontal drift
      vy: (-0.03 - Math.random() * 0.07) * SPEED_SCALE, // Scale upward drift
      radius: 1.0 + Math.random() * 1.8,
      glowRadius: 10 + Math.random() * 18,
      baseAlpha: 0.12 + Math.random() * 0.48,
      pulseSpeed: 0.003 + Math.random() * 0.005, // Slow, hypnotic breathing
      pulseOffset: Math.random() * Math.PI * 2,
      wanderAngle: Math.random() * Math.PI * 2,
      wanderSpeed: (0.002 + Math.random() * 0.004) * SPEED_SCALE,
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

      // Very gentle, slow organic wandering
      w.wanderAngle += w.wanderSpeed;
      w.x += w.vx + Math.cos(w.wanderAngle) * 0.08;
      w.y += w.vy + Math.sin(w.wanderAngle) * 0.05;

      // Gravitational Cursor Lensing (wisps curve gently around cursor mass)
      if (mouseActive) {
        const dx = mouseX - w.x;
        const dy = mouseY - w.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        const GRAVITY_RADIUS = 160;
        if (dist < GRAVITY_RADIUS && dist > 5) {
          const force = (1 - dist / GRAVITY_RADIUS) * 0.5;
          w.x += (dx / dist) * force * 0.45;
          w.y += (dy / dist) * force * 0.45;
          w.wanderAngle += 0.03 * force;
        }
      }

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
