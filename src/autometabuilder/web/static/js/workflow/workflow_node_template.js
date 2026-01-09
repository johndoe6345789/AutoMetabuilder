/**
 * AutoMetabuilder - Workflow Node Template
 */
(() => {
    const build = ({ node, nodeIdx, isFirst, isLast, pluginOptionsHtml, fieldHtml }) => {
        const { t, format, escapeHtml } = window.AMBWorkflowUtils || {};
        const nodeLabel = format?.(t?.('ui.workflow.node_label', 'Node {number}'), { number: nodeIdx + 1 });
        const safeNodeLabel = escapeHtml ? escapeHtml(nodeLabel) : nodeLabel;
        const safeId = escapeHtml ? escapeHtml(node.id || '') : (node.id || '');
        const safeWhen = escapeHtml ? escapeHtml(node.when || '') : (node.when || '');
        const nodeIdLabel = t?.('ui.workflow.node_id_label', 'Node ID');
        const runWhenLabel = t?.('ui.workflow.run_when_label', 'Run when');
        const runWhenPlaceholder = t?.('ui.workflow.run_when_placeholder', '$flag_key');
        const moveUpLabel = t?.('ui.workflow.move_up', 'Move up');
        const moveDownLabel = t?.('ui.workflow.move_down', 'Move down');
        const deleteLabel = t?.('ui.workflow.delete_node', 'Delete node');

        return `
            <div class="amb-workflow-node-header">
                <div class="amb-workflow-node-main">
                    <span class="amb-workflow-node-badge">${safeNodeLabel}</span>
                    <input type="text" class="form-control form-control-sm amb-workflow-node-id"
                           value="${safeId}"
                           placeholder="${escapeHtml ? escapeHtml(nodeIdLabel) : nodeIdLabel}">
                    <select class="form-select form-select-sm amb-workflow-node-type">
                        ${pluginOptionsHtml}
                    </select>
                </div>
                <div class="amb-workflow-node-actions">
                    <button class="btn btn-sm btn-outline-secondary amb-icon-btn" data-action="move-up"
                            ${isFirst ? 'disabled' : ''} title="${escapeHtml ? escapeHtml(moveUpLabel) : moveUpLabel}">
                        <i class="bi bi-chevron-up"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-secondary amb-icon-btn" data-action="move-down"
                            ${isLast ? 'disabled' : ''} title="${escapeHtml ? escapeHtml(moveDownLabel) : moveDownLabel}">
                        <i class="bi bi-chevron-down"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger amb-icon-btn" data-action="remove"
                            title="${escapeHtml ? escapeHtml(deleteLabel) : deleteLabel}">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </div>
            <div class="amb-workflow-node-meta">
                <label class="form-label small text-muted mb-1">${escapeHtml ? escapeHtml(runWhenLabel) : runWhenLabel}</label>
                <input type="text" class="form-control form-control-sm amb-workflow-node-when"
                       value="${safeWhen}"
                       placeholder="${escapeHtml ? escapeHtml(runWhenPlaceholder) : runWhenPlaceholder}">
            </div>
            <div class="amb-workflow-node-body">
                ${fieldHtml}
            </div>
        `;
    };

    window.AMBWorkflowNodeTemplate = { build };
})();
