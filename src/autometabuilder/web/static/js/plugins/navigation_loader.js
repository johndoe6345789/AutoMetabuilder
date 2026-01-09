/**
 * AutoMetabuilder - Navigation Loader
 */
(() => {
    const { t, authHeaders } = window.AMBContext || {};
    const defaults = [
        { section: 'dashboard', icon: 'speedometer2', label_key: 'ui.nav.dashboard', default_label: 'Dashboard' },
        { section: 'workflow', icon: 'diagram-3', label_key: 'ui.nav.workflow', default_label: 'Workflow' },
        { section: 'prompt', icon: 'file-text', label_key: 'ui.nav.prompt', default_label: 'Prompt' },
        { section: 'settings', icon: 'gear', label_key: 'ui.nav.settings', default_label: 'Settings' },
        { section: 'translations', icon: 'translate', label_key: 'ui.nav.translations', default_label: 'Translations' }
    ];

    const fetchNavigation = async () => {
        const response = await fetch('/api/navigation', {
            credentials: 'include',
            headers: authHeaders || {}
        });
        if (!response.ok) {
            throw new Error(`Navigation fetch failed: ${response.status}`);
        }
        return response.json();
    };

    const render = (container, items) => {
        container.innerHTML = '';
        items.forEach(item => {
            const link = document.createElement('a');
            link.className = 'amb-nav-link';
            link.href = `#${item.section}`;
            link.dataset.section = item.section;

            const icon = document.createElement('i');
            icon.className = `bi bi-${item.icon || 'circle'}`;

            const label = document.createTextNode(
                ` ${t?.(item.label_key || '', item.default_label || item.label_key || item.section)}`
            );

            link.appendChild(icon);
            link.appendChild(label);
            container.appendChild(link);
        });
    };

    const init = async () => {
        const container = document.getElementById('amb-nav');
        if (!container) return;
        let items = [];
        try {
            const data = await fetchNavigation();
            items = data.items || [];
        } catch (error) {
            console.error('Navigation fetch failed', error);
        }
        if (!items.length) {
            items = defaults;
        }
        render(container, items);
        if (window.NavigationManager?.refresh) {
            window.NavigationManager.refresh();
        }
    };

    window.AMBPlugins?.register('navigation', init);
})();
