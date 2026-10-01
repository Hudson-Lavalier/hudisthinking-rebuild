/**
 * HudIsThinking - Universal Django Admin Offcanvas Popup Drawer Engine
 * Completely isolates Swup PJAX and delivers 100% native Django Admin editing
 * Strict zero-emoji compliance.
 */

(function () {
  'use strict';

  const drawer = document.getElementById('hit-admin-drawer');
  const iframe = document.getElementById('hit-admin-iframe');
  const backdrop = document.getElementById('hit-drawer-backdrop');
  const closeBtn = document.getElementById('hit-drawer-close');
  const toggleBtn = document.getElementById('hit-hud-toggle-btn');
  const statusBadge = document.getElementById('hit-hud-status-badge');
  const collapseBtn = document.getElementById('hit-hud-collapse-btn');
  const expandBtn = document.getElementById('hit-hud-expand-btn');
  const hud = document.getElementById('hit-live-editor-hud');

  let isEditMode = localStorage.getItem('hit_edit_mode') === 'true';

  function applyEditMode(enabled) {
    isEditMode = enabled;
    localStorage.setItem('hit_edit_mode', enabled ? 'true' : 'false');
    document.body.classList.toggle('hit-editing-active', enabled);

    if (toggleBtn) {
      toggleBtn.textContent = enabled ? '[EDIT MODE: ON]' : '[EDIT MODE: OFF]';
      toggleBtn.classList.toggle('btn-active-toggle', enabled);
    }
    if (statusBadge) {
      statusBadge.textContent = enabled ? '[EDITING ACTIVE]' : '[VIEWER MODE]';
      statusBadge.className = 'hit-hud-status ' + (enabled ? 'is-active' : 'is-synced');
    }
  }

  function openEditDrawer(adminUrl, title) {
    if (!drawer || !iframe) return;
    const popupUrl = adminUrl.includes('?') ? (adminUrl + '&_popup=1') : (adminUrl + '?_popup=1');
    iframe.src = popupUrl;
    if (title && document.getElementById('hit-drawer-title')) {
      document.getElementById('hit-drawer-title').textContent = title;
    }
    drawer.classList.add('is-open');
    if (backdrop) backdrop.classList.add('is-open');
    drawer.setAttribute('aria-hidden', 'false');
  }

  function closeEditDrawer() {
    if (!drawer || !iframe) return;
    drawer.classList.remove('is-open');
    if (backdrop) backdrop.classList.remove('is-open');
    drawer.setAttribute('aria-hidden', 'true');
    iframe.src = 'about:blank';
  }

  // Intercept trigger clicks at document level (immune to Swup DOM swaps)
  document.addEventListener('click', function (e) {
    const trigger = e.target.closest('[data-admin-edit]');
    if (trigger && isEditMode) {
      e.preventDefault();
      e.stopPropagation();
      openEditDrawer(
        trigger.getAttribute('data-admin-edit'),
        trigger.getAttribute('data-admin-title') || 'Django Model Editor'
      );
    }
  });

  if (closeBtn) closeBtn.addEventListener('click', closeEditDrawer);
  if (backdrop) backdrop.addEventListener('click', closeEditDrawer);

  window.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && drawer && drawer.classList.contains('is-open')) {
      closeEditDrawer();
    }
  });

  // Handle Django Admin popup save completion via postMessage
  window.addEventListener('message', function (e) {
    if (e.data && e.data.action === 'saved') {
      closeEditDrawer();

      // Clear Swup Cache prior to re-fetch so fresh HTML is retrieved
      if (window.swup && window.swup.cache) {
        window.swup.cache.clear();
      }

      // Re-render current page dynamically via Swup or browser reload
      if (window.swup) {
        window.swup.navigate(window.location.pathname + window.location.search);
      } else {
        window.location.reload();
      }
    }
  });

  // Collapse & Expand Bottom HUD Bar
  if (collapseBtn && expandBtn && hud) {
    collapseBtn.addEventListener('click', function () {
      hud.classList.add('is-collapsed');
      document.body.classList.remove('hit-staff-active');
      expandBtn.style.display = 'block';
      localStorage.setItem('hit_hud_minimized', 'true');
    });

    expandBtn.addEventListener('click', function () {
      hud.classList.remove('is-collapsed');
      document.body.classList.add('hit-staff-active');
      expandBtn.style.display = 'none';
      localStorage.removeItem('hit_hud_minimized');
    });

    if (localStorage.getItem('hit_hud_minimized') === 'true') {
      hud.classList.add('is-collapsed');
      document.body.classList.remove('hit-staff-active');
      expandBtn.style.display = 'block';
    } else {
      document.body.classList.add('hit-staff-active');
    }
  }

  if (toggleBtn) {
    toggleBtn.addEventListener('click', function () {
      applyEditMode(!isEditMode);
    });
  }

  applyEditMode(isEditMode);
})();
