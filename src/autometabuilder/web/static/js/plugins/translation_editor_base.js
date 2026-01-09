/**
 * AutoMetabuilder - Translation Editor Base
 */
(() => {
    const { t, format } = window.AMBContext || {};

    const editor = {
        currentLang: null,
        data: {},
        baseData: {},
        originalData: {},
        filterTerm: '',
        showMissing: true,
        t,
        format,
        escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text ?? '';
            return div.innerHTML;
        }
    };

    window.AMBTranslationEditor = editor;
    window.AMBPlugins?.register('translation_editor', async () => {
        window.TranslationEditor = editor;
    });
})();
