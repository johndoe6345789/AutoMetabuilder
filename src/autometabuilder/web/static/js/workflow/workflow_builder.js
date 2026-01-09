/**
 * AutoMetabuilder - Workflow Builder
 */
(() => {
    const rerender = () => window.AMBWorkflowCanvasRenderer?.render?.();

    const WorkflowBuilder = {
        init(containerId, textareaId, pluginDefinitions) {
            window.AMBWorkflowState?.setElements?.(containerId, textareaId);
            window.AMBWorkflowState?.setPlugins?.(pluginDefinitions);
            window.AMBWorkflowState?.loadFromTextarea?.();
            rerender();
            window.AMBWorkflowPalette?.init?.();
        },

        toggleRaw() {
            const textarea = window.AMBWorkflowState?.state?.textarea;
            if (!textarea) return;

            textarea.classList.toggle('d-none');
            if (!textarea.classList.contains('d-none')) {
                textarea.oninput = () => {
                    try {
                        const parsed = JSON.parse(textarea.value || '{}');
                        window.AMBWorkflowState?.setWorkflow?.(parsed);
                        rerender();
                    } catch (error) {
                        // Ignore invalid JSON while editing
                    }
                };
            } else {
                textarea.oninput = null;
            }
        },

        loadWorkflow(workflow) {
            window.AMBWorkflowState?.setWorkflow?.(workflow);
            rerender();
        },

        get textarea() {
            return window.AMBWorkflowState?.state?.textarea || null;
        },

        get workflow() {
            return window.AMBWorkflowState?.state?.workflow || { nodes: [] };
        }
    };

    window.WorkflowBuilder = WorkflowBuilder;
})();
