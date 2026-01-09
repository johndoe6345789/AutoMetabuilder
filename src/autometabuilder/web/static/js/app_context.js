/**
 * AutoMetabuilder - Shared Context
 */
(() => {
    let translations = {};
    const t = (key, fallback = '') => translations[key] || fallback || key;
    const format = (text, values = {}) => text.replace(/\{(\w+)\}/g, (_, name) => values[name] ?? '');
    const authHeaders = (() => {
        const username = window.location.username || '';
        const password = window.location.password || '';
        if (!username && !password) return {};
        const token = btoa(`${decodeURIComponent(username)}:${decodeURIComponent(password)}`);
        return { Authorization: `Basic ${token}` };
    })();

    const context = {
        t,
        format,
        authHeaders,
        lang: 'en',
        ready: null
    };

    const loadContext = async () => {
        try {
            const response = await fetch('/api/ui-context', {
                credentials: 'include',
                headers: authHeaders || {}
            });
            if (!response.ok) {
                throw new Error(`UI context fetch failed: ${response.status}`);
            }
            const data = await response.json();
            translations = data.messages || {};
            context.lang = data.lang || 'en';
        } catch (error) {
            console.error('Failed to load UI context', error);
        }
    };

    context.ready = loadContext();
    window.AMBContext = context;
})();
