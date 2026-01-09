/**
 * AutoMetabuilder - Workflow Canvas Renderer
 */
(() => {
    const render = () => {
        const state = window.AMBWorkflowState?.state;
        if (!state?.container) return;
        const { t, escapeHtml } = window.AMBWorkflowUtils || {};
        const mutations = window.AMBWorkflowMutations;
        const nodeRenderer = window.AMBWorkflowNodeRenderer?.renderNodes;

        state.container.innerHTML = '';

        if (!state.workflow.nodes.length) {
            state.container.innerHTML = `
                <div class="text-center text-muted py-4">
                    <i class="bi bi-diagram-3" style="font-size: 2.5rem;"></i>
                    <p class="mt-2">${escapeHtml ? escapeHtml(t?.('ui.workflow.empty', 'No tasks yet. Click "Add Node" to create your first workflow node.')) : t?.('ui.workflow.empty', 'No tasks yet. Click "Add Node" to create your first workflow node.')}</p>
                </div>
            `;
        }

        nodeRenderer?.(state.workflow.nodes, state.container, 0);

        const addNodeBtn = document.createElement('button');
        addNodeBtn.className = 'btn btn-primary';
        addNodeBtn.innerHTML = `<i class="bi bi-plus-lg"></i> ${escapeHtml ? escapeHtml(t?.('ui.workflow.add_node', 'Add Node')) : t?.('ui.workflow.add_node', 'Add Node')}`;
        addNodeBtn.onclick = () => {
            mutations?.addNode(state.workflow.nodes, state.pluginDefinitions);
            render();
        };
        state.container.appendChild(addNodeBtn);

        window.AMBWorkflowState?.sync?.();
    };

    window.AMBWorkflowCanvasRenderer = { render };
})();
