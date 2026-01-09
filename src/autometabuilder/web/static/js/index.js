/**
 * AutoMetabuilder - Index Page Bootstrap
 */
(() => {
    const init = async () => {
        if (window.AMBPlugins?.initAll) {
            await window.AMBPlugins.initAll();
        }
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
