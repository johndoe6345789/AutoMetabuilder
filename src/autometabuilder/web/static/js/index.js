/**
 * AutoMetabuilder - Index Page Scripts
 */
(() => {
    const translations = window.AMB_I18N || {};
    const t = (key, fallback = '') => translations[key] || fallback || key;
    const format = (text, values = {}) => text.replace(/\{(\w+)\}/g, (_, name) => values[name] ?? '');

    const fetchWorkflowPlugins = async () => {
        const response = await fetch('/api/workflow/plugins');
        if (!response.ok) {
            throw new Error(`Plugin fetch failed: ${response.status}`);
        }
        return response.json();
    };

    const initWorkflowBuilder = (pluginDefinitions) => {
        if (!window.WorkflowBuilder) return;
        const container = document.getElementById('workflow-builder');
        const textarea = document.getElementById('workflow-content');
        if (!container || !textarea) return;
        window.WorkflowBuilder.init('workflow-builder', 'workflow-content', pluginDefinitions);
    };

    const updateIterationsGroup = () => {
        const group = document.getElementById('iterations-group');
        if (!group) return;
        const isIterations = document.getElementById('mode-iterations')?.checked;
        group.style.display = isIterations ? 'flex' : 'none';
        const input = group.querySelector('input[name="iterations"]');
        if (input) {
            input.disabled = !isIterations;
        }
    };

    const wireRunModeToggles = () => {
        document.querySelectorAll('input[name="mode"]').forEach(radio => {
            radio.addEventListener('change', updateIterationsGroup);
        });
        updateIterationsGroup();
    };

    const PromptBuilder = {
        append(targetId, snippet) {
            const field = document.getElementById(targetId);
            if (!field) return;
            const current = field.value.trim();
            const spacer = current ? '\n' : '';
            field.value = `${current}${spacer}${snippet}`.trim();
            field.focus();
        }
    };

    const buildPromptYaml = () => {
        const rawPanel = document.getElementById('prompt-raw');
        if (rawPanel && !rawPanel.classList.contains('d-none')) {
            return;
        }

        const systemField = document.getElementById('system-prompt');
        const userField = document.getElementById('user-prompt');
        const modelSelect = document.querySelector('select[name="model"]');
        const outputField = document.getElementById('prompt-yaml');
        if (!systemField || !userField || !modelSelect || !outputField) return;

        const systemContent = systemField.value;
        const userContent = userField.value;
        const model = modelSelect.value;

        const yaml = `messages:
  - role: system
    content: >-
      ${systemContent.split('\n').join('\n      ')}
  - role: user
    content: >-
      ${userContent.split('\n').join('\n      ')}
model: ${model}
`;
        outputField.value = yaml;
    };

    const toggleRawPrompt = () => {
        const rawPanel = document.getElementById('prompt-raw');
        const builder = document.getElementById('prompt-builder');
        if (!rawPanel) return;

        if (rawPanel.classList.contains('d-none')) {
            buildPromptYaml();
            rawPanel.classList.remove('d-none');
            builder?.classList.add('d-none');
        } else {
            rawPanel.classList.add('d-none');
            builder?.classList.remove('d-none');
        }
        const modeInput = document.getElementById('prompt-mode');
        if (modeInput) {
            modeInput.value = rawPanel.classList.contains('d-none') ? 'builder' : 'raw';
        }
    };

    const wirePromptChips = () => {
        document.querySelectorAll('[data-prompt-target]').forEach(button => {
            button.addEventListener('click', () => {
                PromptBuilder.append(button.dataset.promptTarget, button.dataset.promptSnippet || '');
            });
        });

        document.getElementById('prompt-form')?.addEventListener('submit', () => {
            buildPromptYaml();
        });
    };

    const TranslationEditor = {
        currentLang: null,
        data: {},
        baseData: {},
        originalData: {},
        filterTerm: '',
        showMissing: true,

        async load(lang) {
            try {
                const response = await fetch(`/api/translations/${lang}`);
                if (!response.ok) throw new Error(t('ui.translations.errors.load', 'Failed to load translation'));
                const result = await response.json();

                this.currentLang = lang;
                this.data = result.content || {};
                this.originalData = JSON.parse(JSON.stringify(this.data));
                this.filterTerm = '';
                this.showMissing = true;

                if (lang !== 'en') {
                    const baseResponse = await fetch('/api/translations/en');
                    if (baseResponse.ok) {
                        const baseResult = await baseResponse.json();
                        this.baseData = baseResult.content || {};
                    } else {
                        this.baseData = {};
                    }
                } else {
                    this.baseData = result.content || {};
                }

                document.getElementById('editor-title').textContent =
                    `${t('ui.translations.editing_label', 'Editing')}: ${lang.toUpperCase()}`;
                document.getElementById('editor-actions').style.display = 'flex';
                document.getElementById('translation-editor-placeholder').style.display = 'none';
                document.getElementById('translation-editor').style.display = 'block';
                document.getElementById('translation-search').value = '';
                document.getElementById('translation-missing-toggle').checked = true;
                document.getElementById('new-translation-key').value = '';
                document.getElementById('new-translation-value').value = '';

                this.render();

                document.querySelectorAll('.translation-item').forEach(el => el.classList.remove('active'));
                document.querySelector(`.translation-item[data-lang="${lang}"]`)?.classList.add('active');
            } catch (error) {
                alert(`${t('ui.translations.errors.load_prefix', 'Error loading translation: ')}${error.message}`);
            }
        },

        render() {
            const tbody = document.querySelector('#translation-table tbody');
            if (!tbody) return;
            tbody.innerHTML = '';

            const keys = new Set(Object.keys(this.data || {}));
            if (this.showMissing) {
                Object.keys(this.baseData || {}).forEach(key => keys.add(key));
            }

            const sortedKeys = Array.from(keys).sort();
            const missingKeys = Object.keys(this.baseData || {}).filter(key => !(key in this.data));
            const missingCount = missingKeys.length;
            const missingLabel = document.getElementById('missing-count');
            if (missingLabel) {
                const missingText = missingCount
                    ? format(t('ui.translations.missing_count', '{count} missing'), { count: missingCount })
                    : t('ui.translations.all_set', 'All set');
                missingLabel.textContent = missingText;
                missingLabel.classList.toggle('amb-pill-success', missingCount === 0);
                missingLabel.classList.toggle('amb-pill-warning', missingCount > 0);
            }

            sortedKeys.forEach(key => {
                const value = this.data[key] ?? '';
                const baseValue = (this.baseData || {})[key];
                const isMissing = key in (this.baseData || {}) && !(key in this.data);

                const haystack = `${key} ${value} ${baseValue || ''}`.toLowerCase();
                if (this.filterTerm && !haystack.includes(this.filterTerm)) {
                    return;
                }

                const row = document.createElement('tr');
                row.className = isMissing ? 'amb-translation-missing' : '';

                const hintPrefix = t('ui.translations.hint_prefix', 'EN:');
                const hint = isMissing && baseValue
                    ? `<div class="amb-translation-hint">${this.escapeHtml(hintPrefix)} ${this.escapeHtml(baseValue)}</div>`
                    : '';

                row.innerHTML = `
                    <td>
                        <code class="small">${this.escapeHtml(key)}</code>
                        ${isMissing ? `<span class="amb-pill amb-pill-warning ms-2">${this.escapeHtml(t('ui.translations.missing_label', 'Missing'))}</span>` : ''}
                    </td>
                    <td>
                        <div class="amb-translation-field">
                            <input type="text" class="form-control form-control-sm" data-key="${this.escapeHtml(key)}"
                                   value="${this.escapeHtml(value)}" placeholder="${this.escapeHtml(baseValue || '')}">
                            ${hint}
                        </div>
                    </td>
                    <td class="text-end">
                        <button type="button" class="btn btn-sm btn-link text-danger" title="${this.escapeHtml(t('ui.translations.table.delete_title', 'Delete key'))}">
                            <i class="bi bi-trash"></i>
                        </button>
                    </td>
                `;

                const input = row.querySelector('input[data-key]');
                input.addEventListener('input', (event) => this.updateEntry(key, event.target.value));

                const deleteButton = row.querySelector('button');
                deleteButton.addEventListener('click', () => this.deleteEntry(key));

                tbody.appendChild(row);
            });
        },

        updateEntry(key, value) {
            this.data[key] = value;
        },

        addEntry() {
            const keyInput = document.getElementById('new-translation-key');
            const valueInput = document.getElementById('new-translation-value');
            if (!keyInput || !valueInput) return;

            const key = keyInput.value.trim();
            if (!key) {
                alert(t('ui.translations.prompt.enter_key', 'Enter a key name first.'));
                return;
            }

            if (this.data[key] !== undefined) {
                if (!confirm(t('ui.translations.confirm.replace_key', 'This key already exists. Replace it?'))) {
                    return;
                }
            }

            const baseValue = (this.baseData || {})[key] || '';
            const value = valueInput.value.trim() || baseValue;
            this.data[key] = value;

            keyInput.value = '';
            valueInput.value = '';
            this.render();
        },

        prefillNewValue() {
            const keyInput = document.getElementById('new-translation-key');
            const valueInput = document.getElementById('new-translation-value');
            if (!keyInput || !valueInput) return;

            const key = keyInput.value.trim();
            if (!key) {
                alert(t('ui.translations.prompt.enter_key', 'Enter a key name first.'));
                return;
            }

            const baseValue = (this.baseData || {})[key];
            if (!baseValue) {
                alert(t('ui.translations.prompt.no_english', 'No English text found for this key.'));
                return;
            }

            valueInput.value = baseValue;
        },

        deleteEntry(key) {
            if (!confirm(format(t('ui.translations.confirm.delete_key', 'Delete translation key "{key}"?'), { key }))) return;
            delete this.data[key];
            this.render();
        },

        filter(term) {
            this.filterTerm = (term || '').trim().toLowerCase();
            this.render();
        },

        toggleMissing(show) {
            this.showMissing = Boolean(show);
            this.render();
        },

        fillMissing() {
            const baseEntries = Object.entries(this.baseData || {});
            if (!baseEntries.length) return;
            baseEntries.forEach(([key, value]) => {
                if (!(key in this.data)) {
                    this.data[key] = value;
                }
            });
            this.render();
        },

        reset() {
            this.data = JSON.parse(JSON.stringify(this.originalData || {}));
            this.render();
        },

        async save() {
            if (!this.currentLang) return;

            const content = {};
            Object.keys(this.data || {}).sort().forEach(key => {
                content[key] = this.data[key];
            });

            try {
                const response = await fetch(`/api/translations/${this.currentLang}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ content })
                });
                if (!response.ok) throw new Error(t('ui.translations.errors.save', 'Failed to save'));
                this.originalData = JSON.parse(JSON.stringify(this.data));
                Toast.show(format(t('ui.translations.notice.saved', 'Translation "{lang}" saved successfully!'), { lang: this.currentLang }), 'success');
            } catch (error) {
                alert(`${t('ui.translations.errors.save_prefix', 'Error saving translation: ')}${error.message}`);
            }
        },

        async delete(lang) {
            if (!confirm(format(t('ui.translations.confirm.delete_translation', 'Are you sure you want to delete the "{lang}" translation?'), { lang }))) return;

            try {
                const response = await fetch(`/api/translations/${lang}`, { method: 'DELETE' });
                if (!response.ok) throw new Error(t('ui.translations.errors.delete', 'Failed to delete'));
                location.reload();
            } catch (error) {
                alert(`${t('ui.translations.errors.delete_prefix', 'Error deleting translation: ')}${error.message}`);
            }
        },

        escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text ?? '';
            return div.innerHTML;
        }
    };

    const init = async () => {
        let pluginDefinitions = {};
        try {
            pluginDefinitions = await fetchWorkflowPlugins();
        } catch (error) {
            console.error('Workflow plugin fetch failed', error);
        }

        try {
            initWorkflowBuilder(pluginDefinitions);
        } catch (error) {
            console.error('Workflow builder failed to initialize', error);
        }
        wireRunModeToggles();
        wirePromptChips();
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    window.toggleRawPrompt = toggleRawPrompt;
    window.buildPromptYaml = buildPromptYaml;
    window.PromptBuilder = PromptBuilder;
    window.TranslationEditor = TranslationEditor;
})();
