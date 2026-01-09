/**
 * AutoMetabuilder - Workflow Palette Plugin
 */
(() => {
    const init = async () => {
        window.AMBWorkflowPalette?.init?.();
    };

    window.AMBPlugins?.register('workflow_palette', init);
})();
