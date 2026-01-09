/**
 * AutoMetabuilder - Workflow Node Renderer
 */
(() => {
    const renderNodes = (nodes, container, level) => {
        const pluginDefs = window.AMBWorkflowState?.state?.pluginDefinitions || {};
        const pluginOptions = window.AMBWorkflowPluginOptions?.render;
        const fieldRenderer = window.AMBWorkflowFieldRenderer?.renderNodeFields;
        const template = window.AMBWorkflowNodeTemplate?.build;
        const bindEvents = window.AMBWorkflowNodeEvents?.bind;
        const attachLoop = window.AMBWorkflowLoopRenderer?.attach;
        const rerender = () => window.AMBWorkflowCanvasRenderer?.render?.();

        nodes.forEach((node, nodeIdx) => {
            const nodeCard = document.createElement('div');
            nodeCard.className = 'amb-workflow-node mb-3';
            nodeCard.style.marginLeft = level ? `${level * 24}px` : '0';

            const pluginDef = pluginDefs[node.type] || {};
            nodeCard.innerHTML = template?.({
                node,
                nodeIdx,
                isFirst: nodeIdx === 0,
                isLast: nodeIdx === nodes.length - 1,
                pluginOptionsHtml: pluginOptions ? pluginOptions(node.type) : '',
                fieldHtml: fieldRenderer ? fieldRenderer(pluginDef, node) : ''
            }) || '';

            bindEvents?.({ nodeCard, node, nodes, nodeIdx, pluginDefs, rerender });
            attachLoop?.({ node, nodeCard, level, renderNodes, pluginDefs, rerender });
            container.appendChild(nodeCard);
        });
    };

    window.AMBWorkflowNodeRenderer = { renderNodes };
})();
