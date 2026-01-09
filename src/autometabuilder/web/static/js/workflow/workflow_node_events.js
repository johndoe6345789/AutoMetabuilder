/**
 * AutoMetabuilder - Workflow Node Events
 */
(() => {
    const bindFieldUpdates = (nodeCard, node) => {
        nodeCard.querySelectorAll('[data-field-name]').forEach(fieldEl => {
            const fieldName = fieldEl.dataset.fieldName;
            const fieldType = fieldEl.dataset.fieldType || 'text';
            const fieldGroup = fieldEl.dataset.fieldGroup || 'inputs';
            const target = fieldGroup === 'outputs' ? 'outputs' : 'inputs';

            const updateValue = () => {
                let newValue = fieldEl.value;
                if (fieldType === 'checkbox') {
                    newValue = fieldEl.checked;
                } else if (fieldType === 'number') {
                    newValue = fieldEl.value === '' ? '' : Number(fieldEl.value);
                }

                if (!node[target]) node[target] = {};
                node[target][fieldName] = newValue;
                if (newValue === '' || newValue === null) {
                    delete node[target][fieldName];
                }
                window.AMBWorkflowState?.sync?.();
            };

            if (fieldType === 'checkbox') {
                fieldEl.addEventListener('change', updateValue);
            } else {
                fieldEl.addEventListener('input', updateValue);
            }
        });
    };

    const bind = ({ nodeCard, node, nodes, nodeIdx, pluginDefs, rerender }) => {
        const mutations = window.AMBWorkflowMutations;

        nodeCard.querySelector('.amb-workflow-node-id').addEventListener('input', event => {
            node.id = event.target.value;
            window.AMBWorkflowState?.sync?.();
        });

        nodeCard.querySelector('.amb-workflow-node-type').addEventListener('change', event => {
            mutations?.updateNodeType(node, event.target.value, pluginDefs);
            rerender();
        });

        nodeCard.querySelector('[data-action="move-up"]').addEventListener('click', () => {
            mutations?.moveNode(nodes, nodeIdx, -1);
            rerender();
        });
        nodeCard.querySelector('[data-action="move-down"]').addEventListener('click', () => {
            mutations?.moveNode(nodes, nodeIdx, 1);
            rerender();
        });
        nodeCard.querySelector('[data-action="remove"]').addEventListener('click', () => {
            mutations?.removeNode(nodes, nodeIdx);
            rerender();
        });

        nodeCard.querySelector('.amb-workflow-node-when').addEventListener('input', event => {
            node.when = event.target.value;
            if (!node.when) {
                delete node.when;
            }
            window.AMBWorkflowState?.sync?.();
        });

        bindFieldUpdates(nodeCard, node);
    };

    window.AMBWorkflowNodeEvents = { bind };
})();
