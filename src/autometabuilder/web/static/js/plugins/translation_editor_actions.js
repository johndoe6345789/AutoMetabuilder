/**
 * AutoMetabuilder - Translation Editor Actions
 */
(() => {
    const editor = window.AMBTranslationEditor;
    if (!editor) return;

    editor.updateEntry = (key, value) => {
        editor.data[key] = value;
    };

    editor.deleteEntry = (key) => {
        if (!confirm(editor.format?.(editor.t?.('ui.translations.confirm.delete_key', 'Delete translation key "{key}"?'), { key }))) return;
        delete editor.data[key];
        editor.render?.();
    };

    editor.filter = (term) => {
        editor.filterTerm = (term || '').trim().toLowerCase();
        editor.render?.();
    };

    editor.toggleMissing = (show) => {
        editor.showMissing = Boolean(show);
        editor.render?.();
    };

    editor.fillMissing = () => {
        const baseEntries = Object.entries(editor.baseData || {});
        if (!baseEntries.length) return;
        baseEntries.forEach(([key, value]) => {
            if (!(key in editor.data)) {
                editor.data[key] = value;
            }
        });
        editor.render?.();
    };

    editor.reset = () => {
        editor.data = JSON.parse(JSON.stringify(editor.originalData || {}));
        editor.render?.();
    };

    editor.addEntry = () => {
        const keyInput = document.getElementById('new-translation-key');
        const valueInput = document.getElementById('new-translation-value');
        if (!keyInput || !valueInput) return;
        const key = keyInput.value.trim();
        if (!key) {
            alert(editor.t?.('ui.translations.prompt.enter_key', 'Enter a key name first.'));
            return;
        }
        if (editor.data[key] !== undefined) {
            if (!confirm(editor.t?.('ui.translations.confirm.replace_key', 'This key already exists. Replace it?'))) {
                return;
            }
        }
        const baseValue = (editor.baseData || {})[key] || '';
        editor.data[key] = valueInput.value.trim() || baseValue;
        keyInput.value = '';
        valueInput.value = '';
        editor.render?.();
    };

    editor.prefillNewValue = () => {
        const keyInput = document.getElementById('new-translation-key');
        const valueInput = document.getElementById('new-translation-value');
        if (!keyInput || !valueInput) return;
        const key = keyInput.value.trim();
        if (!key) {
            alert(editor.t?.('ui.translations.prompt.enter_key', 'Enter a key name first.'));
            return;
        }
        const baseValue = (editor.baseData || {})[key];
        if (!baseValue) {
            alert(editor.t?.('ui.translations.prompt.no_english', 'No English text found for this key.'));
            return;
        }
        valueInput.value = baseValue;
    };
})();
