/**
 * AutoMetabuilder - Workflow Utils
 */
(() => {
    const t = (key, fallback = '') => window.AMBContext?.t?.(key, fallback) || fallback || key;
    const format = (text, values = {}) => text.replace(/\{(\w+)\}/g, (_, name) => values[name] ?? '');

    const escapeHtml = (text) => {
        if (text === null || text === undefined) return '';
        const div = document.createElement('div');
        div.textContent = String(text);
        return div.innerHTML;
    };

    window.AMBWorkflowUtils = {
        t,
        format,
        escapeHtml
    };
})();
