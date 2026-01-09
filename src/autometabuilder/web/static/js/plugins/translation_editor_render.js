/**
 * AutoMetabuilder - Translation Editor Render
 */
(() => {
    const editor = window.AMBTranslationEditor;
    if (!editor) return;

    editor.render = function render() {
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
                ? this.format?.(this.t?.('ui.translations.missing_count', '{count} missing'), { count: missingCount })
                : this.t?.('ui.translations.all_set', 'All set');
            missingLabel.textContent = missingText;
            missingLabel.classList.toggle('amb-pill-success', missingCount === 0);
            missingLabel.classList.toggle('amb-pill-warning', missingCount > 0);
        }

        sortedKeys.forEach(key => {
            const value = this.data[key] ?? '';
            const baseValue = (this.baseData || {})[key];
            const isMissing = key in (this.baseData || {}) && !(key in this.data);

            const haystack = `${key} ${value} ${baseValue || ''}`.toLowerCase();
            if (this.filterTerm && !haystack.includes(this.filterTerm)) return;

            const row = document.createElement('tr');
            row.className = isMissing ? 'amb-translation-missing' : '';
            const hintPrefix = this.t?.('ui.translations.hint_prefix', 'EN:');
            const hint = isMissing && baseValue
                ? `<div class="amb-translation-hint">${this.escapeHtml(hintPrefix)} ${this.escapeHtml(baseValue)}</div>`
                : '';

            row.innerHTML = `
                <td>
                    <code class="small">${this.escapeHtml(key)}</code>
                    ${isMissing ? `<span class="amb-pill amb-pill-warning ms-2">${this.escapeHtml(this.t?.('ui.translations.missing_label', 'Missing'))}</span>` : ''}
                </td>
                <td>
                    <div class="amb-translation-field">
                        <input type="text" class="form-control form-control-sm" data-key="${this.escapeHtml(key)}"
                               value="${this.escapeHtml(value)}" placeholder="${this.escapeHtml(baseValue || '')}">
                        ${hint}
                    </div>
                </td>
                <td class="text-end">
                    <button type="button" class="btn btn-sm btn-link text-danger" title="${this.escapeHtml(this.t?.('ui.translations.table.delete_title', 'Delete key'))}">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            `;

            row.querySelector('input[data-key]')
                .addEventListener('input', (event) => this.updateEntry?.(key, event.target.value));
            row.querySelector('button')
                .addEventListener('click', () => this.deleteEntry?.(key));
            tbody.appendChild(row);
        });
    };
})();
