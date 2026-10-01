/**
 * HudIsThinking - In-Situ Live Frontend Editor Engine
 * Handles client-side in-place editing, dirty state tracking,
 * and reliable bidirectional sync with Django backend.
 * Works seamlessly with Swup page transitions.
 */

(function () {
  'use strict';

  let state = {
    isEditing: false,
    isDirty: false,
    isSaving: false,
    modifiedFields: {}, // Map of key `${model}:${id}:${field}` -> { model, id, field, value }
    activeElement: null,
  };

  function getHudElements() {
    return {
      hud: document.getElementById('hit-live-editor-hud'),
      statusBadge: document.getElementById('hit-hud-status-badge'),
      toggleBtn: document.getElementById('hit-hud-toggle-btn'),
      saveBtn: document.getElementById('hit-hud-save-btn'),
      mediaBtn: document.getElementById('hit-hud-media-btn'),
      mediaDrawer: document.getElementById('hit-media-drawer'),
      mediaCloseBtn: document.getElementById('hit-drawer-close-btn'),
      mediaGrid: document.getElementById('hit-media-grid'),
    };
  }

  function updateStatus(statusType, label) {
    const { statusBadge } = getHudElements();
    if (!statusBadge) return;
    statusBadge.className = 'hit-hud-status is-' + statusType;
    statusBadge.textContent = '[' + label + ']';
  }

  function setEditing(enable) {
    state.isEditing = enable;
    localStorage.setItem('hit_edit_mode', enable ? 'true' : 'false');
    const { toggleBtn } = getHudElements();
    const editableElements = Array.from(document.querySelectorAll('[data-live-field]'));

    if (enable) {
      document.body.classList.add('hit-editing-active');
      if (toggleBtn) {
        toggleBtn.classList.add('btn-active-toggle');
        toggleBtn.textContent = '[EDIT MODE: ON]';
      }
      editableElements.forEach((el) => {
        el.setAttribute('contenteditable', 'true');
        el.setAttribute('spellcheck', 'false');
      });
      updateStatus(state.isDirty ? 'dirty' : 'synced', state.isDirty ? 'UNSAVED CHANGES' : 'EDITING ACTIVE');
    } else {
      document.body.classList.remove('hit-editing-active');
      if (toggleBtn) {
        toggleBtn.classList.remove('btn-active-toggle');
        toggleBtn.textContent = '[EDIT MODE: OFF]';
      }
      editableElements.forEach((el) => {
        el.removeAttribute('contenteditable');
      });
      updateStatus(state.isDirty ? 'dirty' : 'synced', state.isDirty ? 'UNSAVED CHANGES' : 'STANDBY');
    }
  }

  function getCsrfToken() {
    const cookie = document.cookie.split('; ').find((row) => row.startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
  }

  async function saveChanges() {
    if (!state.isDirty || state.isSaving) return;

    const { saveBtn } = getHudElements();
    state.isSaving = true;
    updateStatus('saving', 'SAVING...');
    if (saveBtn) saveBtn.disabled = true;

    // Group modified fields by model and object ID
    const grouped = {};
    Object.values(state.modifiedFields).forEach((item) => {
      const groupKey = `${item.model}::${item.id}`;
      if (!grouped[groupKey]) {
        grouped[groupKey] = { model: item.model, id: item.id, fields: {} };
      }
      grouped[groupKey].fields[item.field] = item.value;
    });

    try {
      const savePromises = Object.values(grouped).map(async (group) => {
        const payload = {
          model: group.model,
          id: group.id,
          fields: group.fields,
        };
        const res = await fetch('/api/live-editor/save/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
          },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok || data.status !== 'success') {
          throw new Error(data.message || 'Save failed');
        }
        return data;
      });

      await Promise.all(savePromises);

      state.isDirty = false;
      state.modifiedFields = {};
      updateStatus('synced', 'SYNCED & SAVED');
      if (saveBtn) {
        saveBtn.disabled = false;
        saveBtn.style.display = 'none';
      }
    } catch (err) {
      updateStatus('error', 'SAVE ERROR');
      console.error('In-Situ Save Failed:', err);
      alert('Live Editor Sync Error: ' + err.message);
      if (saveBtn) saveBtn.disabled = false;
    } finally {
      state.isSaving = false;
    }
  }

  function initPage() {
    const { hud, toggleBtn, saveBtn, mediaBtn, mediaDrawer, mediaCloseBtn } = getHudElements();
    if (!hud) return;

    const collapseBtn = document.getElementById('hit-hud-collapse-btn');
    const expandBtn = document.getElementById('hit-hud-expand-btn');

    // 1. Collapse & Expand Controls (Always wired up)
    if (collapseBtn && !collapseBtn._hasLiveEditorListener) {
      collapseBtn.addEventListener('click', () => {
        hud.classList.add('is-collapsed');
        document.body.classList.remove('hit-staff-active');
        if (expandBtn) expandBtn.style.display = 'block';
        localStorage.setItem('hit_hud_minimized', 'true');
      });
      collapseBtn._hasLiveEditorListener = true;
    }

    if (expandBtn && !expandBtn._hasLiveEditorListener) {
      expandBtn.addEventListener('click', () => {
        hud.classList.remove('is-collapsed');
        document.body.classList.add('hit-staff-active');
        expandBtn.style.display = 'none';
        localStorage.removeItem('hit_hud_minimized');
      });
      expandBtn._hasLiveEditorListener = true;
    }

    // Apply saved collapse state
    if (localStorage.getItem('hit_hud_minimized') === 'true') {
      hud.classList.add('is-collapsed');
      document.body.classList.remove('hit-staff-active');
      if (expandBtn) expandBtn.style.display = 'block';
    } else {
      hud.classList.remove('is-collapsed');
      document.body.classList.add('hit-staff-active');
      if (expandBtn) expandBtn.style.display = 'none';
    }

    // 2. Media Drawer Controls (Always wired up)
    if (mediaBtn && mediaDrawer && !mediaBtn._hasLiveEditorListener) {
      mediaBtn.addEventListener('click', async () => {
        mediaDrawer.classList.toggle('is-open');
        if (mediaDrawer.classList.contains('is-open')) {
          await loadMediaLibrary();
        }
      });
      mediaBtn._hasLiveEditorListener = true;
    }

    if (mediaCloseBtn && mediaDrawer && !mediaCloseBtn._hasLiveEditorListener) {
      mediaCloseBtn.addEventListener('click', () => {
        mediaDrawer.classList.remove('is-open');
      });
      mediaCloseBtn._hasLiveEditorListener = true;
    }

    // 3. Save Button (Always wired up)
    if (saveBtn && !saveBtn._hasLiveEditorListener) {
      saveBtn.addEventListener('click', saveChanges);
      saveBtn._hasLiveEditorListener = true;
    }

    // 4. Toggle Button (Always wired up)
    if (toggleBtn && !toggleBtn._hasLiveEditorListener) {
      toggleBtn.addEventListener('click', () => {
        setEditing(!state.isEditing);
      });
      toggleBtn._hasLiveEditorListener = true;
    }

    // 5. Restore saved edit mode
    const savedEditMode = localStorage.getItem('hit_edit_mode') === 'true';
    state.isEditing = savedEditMode;

    // 6. Handle Editable Regions
    const editableElements = Array.from(document.querySelectorAll('[data-live-field]'));

    if (editableElements.length === 0) {
      if (toggleBtn) {
        toggleBtn.disabled = true;
        toggleBtn.textContent = '[NO EDITABLE REGIONS]';
        toggleBtn.classList.remove('btn-active-toggle');
      }
      updateStatus('synced', 'STANDBY');
      return;
    }

    if (toggleBtn) {
      toggleBtn.disabled = false;
      if (state.isEditing) {
        toggleBtn.classList.add('btn-active-toggle');
        toggleBtn.textContent = '[EDIT MODE: ON]';
      } else {
        toggleBtn.classList.remove('btn-active-toggle');
        toggleBtn.textContent = '[EDIT MODE: OFF]';
      }
    }

    if (state.isEditing) {
      document.body.classList.add('hit-editing-active');
      updateStatus(state.isDirty ? 'dirty' : 'synced', state.isDirty ? 'UNSAVED CHANGES' : 'EDITING ACTIVE');
    } else {
      document.body.classList.remove('hit-editing-active');
      updateStatus(state.isDirty ? 'dirty' : 'synced', state.isDirty ? 'UNSAVED CHANGES' : 'STANDBY');
    }

    editableElements.forEach((el) => {
      const field = el.getAttribute('data-live-field');
      const model = el.getAttribute('data-live-model');
      const id = el.getAttribute('data-live-id');

      if (state.isEditing) {
        el.setAttribute('contenteditable', 'true');
        el.setAttribute('spellcheck', 'false');
      } else {
        el.removeAttribute('contenteditable');
      }

      if (!el._hasLiveEditorListener) {
        el.addEventListener('click', (e) => {
          if (state.isEditing && (el.tagName === 'A' || el.closest('a'))) {
            e.preventDefault();
          }
        });

        el.addEventListener('focus', () => {
          state.activeElement = el;
        });

        el.addEventListener('input', () => {
          const isMarkdown = el.getAttribute('data-live-format') === 'markdown';
          const currentVal = isMarkdown ? el.innerText : el.innerHTML;
          const key = `${model}:${id}:${field}`;

          state.modifiedFields[key] = {
            model: model,
            id: id,
            field: field,
            value: currentVal,
          };
          state.isDirty = true;
          updateStatus('dirty', 'UNSAVED CHANGES');
          if (saveBtn) saveBtn.style.display = 'inline-flex';
        });

        el._hasLiveEditorListener = true;
      }
    });
  }

  async function loadMediaLibrary() {
    const { mediaGrid, mediaDrawer } = getHudElements();
    if (!mediaGrid) return;
    mediaGrid.innerHTML = '<div style="color: #666; font-size: 0.8rem;">Loading Media Library...</div>';
    try {
      const res = await fetch('/api/live-editor/media/');
      const data = await res.json();
      if (res.ok && data.status === 'success') {
        mediaGrid.innerHTML = '';
        data.items.forEach((item) => {
          const card = document.createElement('div');
          card.className = 'hit-media-card';
          card.innerHTML = `
            ${item.url && item.media_type === 'image' ? `<img src="${item.url}" class="hit-media-thumb" alt="${item.title}">` : `<div style="height: 100px; display:flex; align-items:center; justify-content:center; background:#111; color:#777; font-size:0.7rem;">[${item.media_type.toUpperCase()}]</div>`}
            <div class="hit-media-name" title="${item.title}">${item.title}</div>
            <button type="button" class="hit-media-insert-btn">[INSERT]</button>
          `;
          card.querySelector('.hit-media-insert-btn').addEventListener('click', () => {
            if (state.activeElement && state.isEditing) {
              document.execCommand('insertText', false, item.markdown_embed);
            }
            if (mediaDrawer) mediaDrawer.classList.remove('is-open');
          });
          mediaGrid.appendChild(card);
        });
      }
    } catch (e) {
      mediaGrid.innerHTML = '<div style="color: #f33; font-size: 0.8rem;">Error loading media.</div>';
    }
  }

  // Keyboard shortcut Ctrl+S / Cmd+S
  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
      if (state.isEditing && state.isDirty) {
        e.preventDefault();
        saveChanges();
      }
    }
  });

  // Run on initial page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPage);
  } else {
    initPage();
  }

  // Hook into Swup page transitions if Swup is active
  document.addEventListener('swup:contentReplaced', initPage);
  document.addEventListener('swup:pageView', initPage);
})();
