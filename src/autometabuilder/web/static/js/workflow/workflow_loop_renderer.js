/**
 * AutoMetabuilder - Workflow Loop Renderer
 */
(() => {
    const attach = ({ node, nodeCard, level, renderNodes, pluginDefs, rerender }) => {
        if (node.type !== 'control.loop') return;
        const { t, escapeHtml } = window.AMBWorkflowUtils || {};
        const mutations = window.AMBWorkflowMutations;

        const bodyContainer = document.createElement('div');
        bodyContainer.className = 'amb-workflow-node-nested';
        bodyContainer.innerHTML = `
            <div class="amb-workflow-node-nested-header">
                <strong>${escapeHtml ? escapeHtml(t?.('ui.workflow.loop_body_label', 'Loop Body')) : t?.('ui.workflow.loop_body_label', 'Loop Body')}</strong>
            </div>
        `;

        const bodyNodes = Array.isArray(node.body) ? node.body : [];
        node.body = bodyNodes;
        renderNodes(bodyNodes, bodyContainer, level + 1);

        const addNestedBtn = document.createElement('button');
        addNestedBtn.className = 'btn btn-sm btn-outline-primary';
        addNestedBtn.innerHTML = `<i class="bi bi-plus-lg"></i> ${escapeHtml ? escapeHtml(t?.('ui.workflow.add_loop_node', 'Add Node to Loop')) : t?.('ui.workflow.add_loop_node', 'Add Node to Loop')}`;
        addNestedBtn.onclick = () => {
            mutations?.addNode(bodyNodes, pluginDefs);
            rerender();
        };
        bodyContainer.appendChild(addNestedBtn);

        nodeCard.appendChild(bodyContainer);
    };

    window.AMBWorkflowLoopRenderer = { attach };
})();
