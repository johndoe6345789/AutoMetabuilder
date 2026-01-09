/**
 * AutoMetabuilder - Choices Manager
 */
(() => {
    const i18n = (key, fallback = '') => window.AMBContext?.t?.(key, fallback) || fallback || key;

    const ChoicesManager = {
        instances: [],

        init() {
            this.initAll();
        },

        initAll() {
            document.querySelectorAll('[data-choices]').forEach(el => {
                if (el.dataset.choicesInit === 'true') return;

                const optionsStr = el.dataset.choicesOptions || '{}';
                let options = {};
                try {
                    options = JSON.parse(optionsStr);
                } catch (error) {
                    console.warn('Invalid choices options:', optionsStr);
                }

                const instance = new Choices(el, {
                    searchEnabled: true,
                    shouldSort: false,
                    allowHTML: false,
                    removeItemButton: options.removeItemButton || false,
                    placeholder: true,
                    placeholderValue: el.dataset.placeholder || i18n('ui.common.select_placeholder', 'Select...'),
                    searchPlaceholderValue: i18n('ui.choices.search_placeholder', 'Type to search...'),
                    noResultsText: i18n('ui.choices.no_results', 'No results found'),
                    noChoicesText: i18n('ui.choices.no_choices', 'No choices available'),
                    ...options
                });
                el.dataset.choicesInit = 'true';
                this.instances.push(instance);
            });
        },

        destroy() {
            this.instances.forEach(instance => {
                try {
                    const element = instance.passedElement?.element;
                    if (element) {
                        element.dataset.choicesInit = 'false';
                    }
                    instance.destroy();
                } catch (error) {
                    // Ignore errors from already destroyed instances
                }
            });
            this.instances = [];
        },

        refresh() {
            this.destroy();
            this.initAll();
        }
    };

    window.ChoicesManager = ChoicesManager;
    window.AMBPlugins?.register('choices_manager', async () => ChoicesManager.init());
})();
