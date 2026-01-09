/**
 * AutoMetabuilder - Plugin Registry
 */
(() => {
    const plugins = [];

    const register = (name, init) => {
        if (!name || typeof init !== 'function') return;
        plugins.push({ name, init });
    };

    const initAll = async () => {
        if (window.AMBContext?.ready) {
            await window.AMBContext.ready;
        }
        for (const plugin of plugins) {
            try {
                await plugin.init();
            } catch (error) {
                console.error(`Plugin init failed: ${plugin.name}`, error);
            }
        }
    };

    window.AMBPlugins = {
        register,
        initAll
    };
})();
