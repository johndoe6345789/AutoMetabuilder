/**
 * AutoMetabuilder - Workflow State
 */
(() => {
    const state = {
        workflow: { nodes: [] },
        pluginDefinitions: {},
        container: null,
        textarea: null
    };

    const setElements = (containerId, textareaId) => {
        state.container = document.getElementById(containerId);
        state.textarea = document.getElementById(textareaId);
    };

    const setPlugins = (pluginDefinitions) => {
        state.pluginDefinitions = pluginDefinitions || {};
    };

    const setWorkflow = (workflow) => {
        if (workflow && Array.isArray(workflow.nodes)) {
            state.workflow = workflow;
        } else {
            state.workflow = { nodes: [] };
        }
    };

    const loadFromTextarea = () => {
        if (!state.textarea) {
            setWorkflow({ nodes: [] });
            return;
        }
        try {
            const parsed = JSON.parse(state.textarea.value || '{}');
            setWorkflow(parsed);
        } catch (error) {
            console.error('Failed to parse workflow JSON', error);
            setWorkflow({ nodes: [] });
        }
    };

    const sync = () => {
        if (state.textarea) {
            state.textarea.value = JSON.stringify(state.workflow, null, 2);
        }
    };

    window.AMBWorkflowState = {
        state,
        setElements,
        setPlugins,
        setWorkflow,
        loadFromTextarea,
        sync
    };
})();
