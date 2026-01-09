/**
 * AutoMetabuilder - Workflow Mutations
 */
(() => {
    const buildDefaultFields = (definitions) => {
        const result = {};
        Object.entries(definitions || {}).forEach(([name, def]) => {
            if (def.default !== undefined && def.default !== '') {
                result[name] = def.default;
            }
        });
        return result;
    };

    const updateNodeType = (node, newType, pluginDefinitions) => {
        node.type = newType;
        const def = pluginDefinitions[newType] || {};
        node.inputs = buildDefaultFields(def.inputs);
        node.outputs = buildDefaultFields(def.outputs);
        if (newType === 'control.loop') {
            node.body = Array.isArray(node.body) ? node.body : [];
        } else {
            delete node.body;
        }
    };

    const generateNodeId = (type, nodes) => {
        const base = type ? type.split('.').pop() : 'node';
        const existing = new Set((nodes || []).map(node => node.id));
        let counter = (nodes || []).length + 1;
        let candidate = `${base}_${counter}`;
        while (existing.has(candidate)) {
            counter += 1;
            candidate = `${base}_${counter}`;
        }
        return candidate;
    };

    const addNode = (targetArray, pluginDefinitions) => {
        const types = Object.keys(pluginDefinitions);
        const defaultType = types[0] || '';
        const node = {
            id: generateNodeId(defaultType, targetArray),
            type: defaultType,
            inputs: buildDefaultFields(pluginDefinitions[defaultType]?.inputs),
            outputs: buildDefaultFields(pluginDefinitions[defaultType]?.outputs)
        };
        targetArray.push(node);
    };

    const moveNode = (nodes, idx, dir) => {
        const target = idx + dir;
        if (target < 0 || target >= nodes.length) return;
        [nodes[idx], nodes[target]] = [nodes[target], nodes[idx]];
    };

    const removeNode = (nodes, idx) => {
        nodes.splice(idx, 1);
    };

    window.AMBWorkflowMutations = {
        buildDefaultFields,
        updateNodeType,
        generateNodeId,
        addNode,
        moveNode,
        removeNode
    };
})();
