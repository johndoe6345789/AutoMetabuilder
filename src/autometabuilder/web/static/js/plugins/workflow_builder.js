/**
 * AutoMetabuilder - Workflow Builder Loader
 */
(() => {
    const { authHeaders } = window.AMBContext || {};

    const fetchWorkflowPlugins = async () => {
        const response = await fetch('/api/workflow/plugins', {
            credentials: 'include',
            headers: authHeaders || {}
        });
        if (!response.ok) {
            throw new Error(`Plugin fetch failed: ${response.status}`);
        }
        return response.json();
    };

    const init = async () => {
        const container = document.getElementById('workflow-builder');
        const textarea = document.getElementById('workflow-content');
        if (!container || !textarea || !window.WorkflowBuilder) return;
        try {
            const pluginDefinitions = await fetchWorkflowPlugins();
            window.WorkflowBuilder.init('workflow-builder', 'workflow-content', pluginDefinitions);
        } catch (error) {
            console.error('Workflow builder failed to initialize', error);
            window.WorkflowBuilder.init('workflow-builder', 'workflow-content', {});
        }
    };

    window.AMBPlugins?.register('workflow_builder', init);
})();
