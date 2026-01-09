/**
 * AutoMetabuilder - Translation Editor Network
 */
(() => {
    const editor = window.AMBTranslationEditor;
    if (!editor) return;

    editor.load = async (lang) => {
        try {
            const response = await fetch(`/api/translations/${lang}`);
            if (!response.ok) throw new Error(editor.t?.('ui.translations.errors.load', 'Failed to load translation'));
            const result = await response.json();

            editor.currentLang = lang;
            editor.data = result.content || {};
            editor.originalData = JSON.parse(JSON.stringify(editor.data));
            editor.filterTerm = '';
            editor.showMissing = true;

            if (lang !== 'en') {
                const baseResponse = await fetch('/api/translations/en');
                if (baseResponse.ok) {
                    const baseResult = await baseResponse.json();
                    editor.baseData = baseResult.content || {};
                } else {
                    editor.baseData = {};
                }
            } else {
                editor.baseData = result.content || {};
            }

            document.getElementById('editor-title').textContent =
                `${editor.t?.('ui.translations.editing_label', 'Editing')}: ${lang.toUpperCase()}`;
            document.getElementById('editor-actions').style.display = 'flex';
            document.getElementById('translation-editor-placeholder').style.display = 'none';
            document.getElementById('translation-editor').style.display = 'block';
            document.getElementById('translation-search').value = '';
            document.getElementById('translation-missing-toggle').checked = true;
            document.getElementById('new-translation-key').value = '';
            document.getElementById('new-translation-value').value = '';

            editor.render?.();
            document.querySelectorAll('.translation-item').forEach(el => el.classList.remove('active'));
            document.querySelector(`.translation-item[data-lang="${lang}"]`)?.classList.add('active');
        } catch (error) {
            alert(`${editor.t?.('ui.translations.errors.load_prefix', 'Error loading translation: ')}${error.message}`);
        }
    };

    editor.save = async () => {
        if (!editor.currentLang) return;
        const content = {};
        Object.keys(editor.data || {}).sort().forEach(key => {
            content[key] = editor.data[key];
        });

        try {
            const response = await fetch(`/api/translations/${editor.currentLang}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content })
            });
            if (!response.ok) throw new Error(editor.t?.('ui.translations.errors.save', 'Failed to save'));
            editor.originalData = JSON.parse(JSON.stringify(editor.data));
            window.Toast?.show(
                editor.format?.(editor.t?.('ui.translations.notice.saved', 'Translation "{lang}" saved successfully!'), {
                    lang: editor.currentLang
                }),
                'success'
            );
        } catch (error) {
            alert(`${editor.t?.('ui.translations.errors.save_prefix', 'Error saving translation: ')}${error.message}`);
        }
    };

    editor.delete = async (lang) => {
        if (!confirm(editor.format?.(editor.t?.('ui.translations.confirm.delete_translation', 'Are you sure you want to delete the "{lang}" translation?'), { lang }))) return;
        try {
            const response = await fetch(`/api/translations/${lang}`, { method: 'DELETE' });
            if (!response.ok) throw new Error(editor.t?.('ui.translations.errors.delete', 'Failed to delete'));
            location.reload();
        } catch (error) {
            alert(`${editor.t?.('ui.translations.errors.delete_prefix', 'Error deleting translation: ')}${error.message}`);
        }
    };
})();
