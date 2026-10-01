/**
 * HudIsThinking - In-Situ Live Frontend Editor Engine
 * Handles client-side in-place editing, dirty state tracking,
 * and reliable bidirectional sync with Django backend.
 */

(function () {
  'use strict';

  // Check if live editor container exists on page
  const hudContainer = document.getElementById('hit-live-editor-hud');
  if (!hudContainer) return;

  const state = {
    isEditing: false,
    isDirty: false,
    isSaving: false,
    activeModel: null,
    activeId: null,
    modifiedFields: {},
    initialValues: {},
    activeElement: null,
  };

  const statusBadge = document.getElementById('hit-hud-status-badge');
  const toggleBtn = document.getElementById('hit-hud-toggle-btn');
  const saveBtn = document.getElementById('hit-hud-save-btn');
  const mediaBtn = document.getElementById('hit-hud-media-btn');
  const mediaDrawer = document.getElementById('hit-media-drawer');
  const mediaCloseBtn = document.getElementById('hit-drawer-close-btn');
  const mediaGrid = document.getElementById('hit-media-grid');

  // Discover all editable fields on the page
  const editableElements = Array.from(document.querySelectorAll('[data-live-field]'));
  if (editableElements.length === 0) {
    toggleBtn.disabled = true;
    toggleBtn.textContent = '[NO EDITABLE REGIONS]';
    return;
  }

  // Derive model and object ID from first editable element or page container
  const firstElem = editableElements[0];
  state.activeModel = firstElem.getAttribute('data-live-model');
  state.activeId = firstElem.getAttribute('data-live-id');

  // Snapshot initial values
  editableElements.forEach((el) => {
    const field = el.getAttribute('data-live-field');
    const isMarkdown = el.getAttribute('data-live-format') === 'markdown';
    // If raw markdown is provided in a data attribute, prioritize it
    const rawVal = el.getAttribute('data-live-raw') || (isMarkdown ? el.innerText.trim() : el.innerHTML.trim());
    state.initialValues[field] = rawVal;
  });

  function updateStatus(statusType, label) {
    statusBadge.className = 'hit-hud-status is-' + statusType;
    statusBadge.textContent = '[' + label + ']';
  }

  function setEditing(enable) {
    state.isEditing = enable;
    if (enable) {
      document.body.classList.add('hit-editing-active');
      toggleBtn.classList.add('btn-active-toggle');
      toggleBtn.textContent = '[EDIT MODE: ON]';
      editableElements.forEach((el) => {
        el.setAttribute('contenteditable', 'true');
        el.setAttribute('spellcheck', 'false');
      });
      updateStatus(state.isDirty ? 'dirty' : 'synced', state.isDirty ? 'UNSAVED CHANGES' : 'EDITING ACTIVE');
    } else {
      document.body.classList.remove('hit-editing-active');
      toggleBtn.classList.remove('btn-active-toggle');
      toggleBtn.textContent = '[EDIT MODE: OFF]';
      editableElements.forEach((el) => {
        el.removeAttribute('contenteditable');
      });
      updateStatus(state.isDirty ? 'dirty' : 'synced', state.isDirty ? 'UNSAVED CHANGES' : 'STANDBY');
    }
  }

  // Handle user typing and changes
  editableElements.forEach((el) => {
    el.addEventListener('focus', () => {
      state.activeElement = el;
    });

    el.addEventListener('input', () => {
      const field = el.getAttribute('data-live-field');
      const isMarkdown = el.getAttribute('data-live-format') === 'markdown';
      const currentVal = isMarkdown ? el.innerText : el.innerHTML;

      state.modifiedFields[field] = currentVal;
      state.isDirty = true;
      updateStatus('dirty', 'UNSAVED CHANGES');
      saveBtn.style.display = 'inline-flex';
    });
  });

  // Toggle button event
  toggleBtn.addEventListener('click', () => {
    setEditing(!state.isEditing);
  });

  // CSRF token helper
  function getCsrfToken() {
    const cookie = document.cookie.split('; ').find((row) => row.startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
  }

  // Save changes to Django backend
  async function saveChanges() {
    if (!state.isDirty || state.isSaving) return;

    state.isSaving = true;
    updateStatus('saving', 'SAVING...');
    saveBtn.disabled = true;

    const payload = {
      model: state.activeModel,
      id: state.activeId,
      fields: state.modifiedFields,
    };

    try {
      const res = await fetch('/api/live-editor/save/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      if (res.ok && data.status === 'success') {
        state.isDirty = false;
        state.modifiedFields = {};
        updateStatus('synced', 'SYNCED & SAVED');
        saveBtn.disabled = false;
        saveBtn.style.display = 'none';

        // Update rendered previews if server provided formatted markdown back
        if (data.rendered_previews) {
          Object.keys(data.rendered_previews).forEach((field) => {
            const targetEl = document.querySelector(`[data-live-field="${field}"]`);
            if (targetEl && targetEl.getAttribute('data-live-format') === 'markdown') {
              // Update content when user leaves editing mode
              targetEl.setAttribute('data-live-raw', targetEl.innerText);
            }
          });
        }
      } else {
        updateStatus('error', 'SAVE ERROR');
        alert('Live Editor Sync Error: ' + (data.message || 'Unknown error'));
        saveBtn.disabled = false;
      }
    } catch (err) {
      updateStatus('error', 'NETWORK ERROR');
      console.error('In-Situ Save Failed:', err);
      alert('Network failure syncing changes to server.');
      saveBtn.disabled = false;
    } finally {
      state.isSaving = false;
    }
  }

  saveBtn.addEventListener('click', saveChanges);

  // Keyboard shortcut Ctrl+S / Cmd+S
  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
      if (state.isEditing && state.isDirty) {
        e.preventDefault();
        saveChanges();
      }
    }
  });

  // Media Drawer Integration
  if (mediaBtn && mediaDrawer) {
    mediaBtn.addEventListener('click', async () => {
      mediaDrawer.classList.toggle('is-open');
      if (mediaDrawer.classList.contains('is-open')) {
        await loadMediaLibrary();
      }
    });

    mediaCloseBtn.addEventListener('click', () => {
      mediaDrawer.classList.remove('is-open');
    });
  }

  async function loadMediaLibrary() {
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
            <button type="button" class="hit-media-insert-btn" data-embed="${item.markdown_embed.replace(/"/g, '&quot;')}">[INSERT]</button>
          `;
          card.querySelector('.hit-media-insert-btn').addEventListener('click', () => {
            insertAtCursor(item.markdown_embed);
            mediaDrawer.classList.remove('is-open');
          });
          mediaGrid.appendChild(card);
        });
      }
    } catch (e) {
      mediaGrid.innerHTML = '<div style="color: #f33; font-size: 0.8rem;">Error loading media.</div>';
    }
  }

  function insertAtCursor(text) {
    if (state.activeElement && state.isEditing) {
      document.execCommand('insertText', false, text);
    }
  }
})();
