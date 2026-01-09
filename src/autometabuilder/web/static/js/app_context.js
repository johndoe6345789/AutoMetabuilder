/**
 * AutoMetabuilder - Shared Context
 */
(() => {
    const translations = window.AMB_I18N || {};
    const t = (key, fallback = '') => translations[key] || fallback || key;
    const format = (text, values = {}) => text.replace(/\{(\w+)\}/g, (_, name) => values[name] ?? '');
    const authHeaders = (() => {
        const username = window.location.username || '';
        const password = window.location.password || '';
        if (!username && !password) return {};
        const token = btoa(`${decodeURIComponent(username)}:${decodeURIComponent(password)}`);
        return { Authorization: `Basic ${token}` };
    })();

    window.AMBContext = {
        t,
        format,
        authHeaders
    };
})();
