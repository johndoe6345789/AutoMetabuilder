/**
 * AutoMetabuilder - Workflow Builder (Node-based)
 */

const WorkflowBuilder = {
    workflow: { nodes: [] },
    pluginDefinitions: {},
    container: null,
    textarea: null,

    t(key, fallback = '') {
        const dict = window.AMB_I18N || {};
        return dict[key] || fallback || key;
    },

    format(text, values = {}) {
        return text.replace(/\{(\w+)\}/g, (_, name) => values[name] ?? '');
    },

    init(containerId, textareaId, pluginDefinitions) {
        this.container = document.getElementById(containerId);
        this.textarea = document.getElementById(textareaId);
        this.pluginDefinitions = pluginDefinitions || {};

        try {
            const parsed = JSON.parse(this.textarea.value || '{}');
            this.workflow = parsed && parsed.nodes ? parsed : { nodes: [] };
        } catch (e) {
            console.error('Failed to parse workflow JSON', e);
            this.workflow = { nodes: [] };
        }

        this.render();
    },

    render() {
        if (!this.container) return;

        this.container.innerHTML = '';

        if (!this.workflow.nodes.length) {
            this.container.innerHTML = `
                <div class="text-center text-muted py-4">
                    <i class="bi bi-diagram-3" style="font-size: 2.5rem;"></i>
                    <p class="mt-2">${this.escapeHtml(this.t('ui.workflow.empty', 'No tasks yet. Click "Add Node" to create your first workflow node.'))}</p>
                </div>
            `;
        }

        this.renderNodes(this.workflow.nodes, this.container, 0);

        const addNodeBtn = document.createElement('button');
        addNodeBtn.className = 'btn btn-primary';
        addNodeBtn.innerHTML = `<i class="bi bi-plus-lg"></i> ${this.escapeHtml(this.t('ui.workflow.add_node', 'Add Node'))}`;
        addNodeBtn.onclick = () => this.addNode(this.workflow.nodes);
        this.container.appendChild(addNodeBtn);

        this.sync();
    },

    renderNodes(nodes, container, level) {
        nodes.forEach((node, nodeIdx) => {
            const nodeCard = document.createElement('div');
            nodeCard.className = 'amb-workflow-node mb-3';
            nodeCard.style.marginLeft = level ? `${level * 24}px` : '0';

            const pluginDef = this.pluginDefinitions[node.type] || {};
            const nodeLabel = this.format(
                this.t('ui.workflow.node_label', 'Node {number}'),
                { number: nodeIdx + 1 }
            );

            nodeCard.innerHTML = `
                <div class="amb-workflow-node-header">
                    <div class="amb-workflow-node-main">
                        <span class="amb-workflow-node-badge">${this.escapeHtml(nodeLabel)}</span>
                        <input type="text" class="form-control form-control-sm amb-workflow-node-id"
                               value="${this.escapeHtml(node.id || '')}"
                               placeholder="${this.escapeHtml(this.t('ui.workflow.node_id_label', 'Node ID'))}">
                        <select class="form-select form-select-sm amb-workflow-node-type">
                            ${this.renderPluginOptions(node.type)}
                        </select>
                    </div>
                    <div class="amb-workflow-node-actions">
                        <button class="btn btn-sm btn-outline-secondary amb-icon-btn" data-action="move-up"
                                ${nodeIdx === 0 ? 'disabled' : ''} title="${this.escapeHtml(this.t('ui.workflow.move_up', 'Move up'))}">
                            <i class="bi bi-chevron-up"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-secondary amb-icon-btn" data-action="move-down"
                                ${nodeIdx === nodes.length - 1 ? 'disabled' : ''} title="${this.escapeHtml(this.t('ui.workflow.move_down', 'Move down'))}">
                            <i class="bi bi-chevron-down"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger amb-icon-btn" data-action="remove"
                                title="${this.escapeHtml(this.t('ui.workflow.delete_node', 'Delete node'))}">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </div>
                <div class="amb-workflow-node-meta">
                    <label class="form-label small text-muted mb-1">${this.escapeHtml(this.t('ui.workflow.run_when_label', 'Run when'))}</label>
                    <input type="text" class="form-control form-control-sm amb-workflow-node-when"
                           value="${this.escapeHtml(node.when || '')}"
                           placeholder="${this.escapeHtml(this.t('ui.workflow.run_when_placeholder', '$flag_key'))}">
                </div>
                <div class="amb-workflow-node-body">
                    ${this.renderNodeFields(pluginDef, node)}
                </div>
            `;

            const idInput = nodeCard.querySelector('.amb-workflow-node-id');
            idInput.addEventListener('input', (event) => {
                node.id = event.target.value;
                this.sync();
            });

            const typeSelect = nodeCard.querySelector('.amb-workflow-node-type');
            typeSelect.addEventListener('change', (event) => {
                this.updateNodeType(node, event.target.value);
                this.render();
            });

            nodeCard.querySelector('[data-action="move-up"]').addEventListener('click', () => {
                this.moveNode(nodes, nodeIdx, -1);
            });
            nodeCard.querySelector('[data-action="move-down"]').addEventListener('click', () => {
                this.moveNode(nodes, nodeIdx, 1);
            });
            nodeCard.querySelector('[data-action="remove"]').addEventListener('click', () => {
                this.removeNode(nodes, nodeIdx);
            });

            const whenInput = nodeCard.querySelector('.amb-workflow-node-when');
            whenInput.addEventListener('input', (event) => {
                node.when = event.target.value;
                if (!node.when) {
                    delete node.when;
                }
                this.sync();
            });

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
                    this.sync();
                };

                if (fieldType === 'checkbox') {
                    fieldEl.addEventListener('change', updateValue);
                } else {
                    fieldEl.addEventListener('input', updateValue);
                }
            });

            if (node.type === 'control.loop') {
                const bodyContainer = document.createElement('div');
                bodyContainer.className = 'amb-workflow-node-nested';
                bodyContainer.innerHTML = `
                    <div class="amb-workflow-node-nested-header">
                        <strong>${this.escapeHtml(this.t('ui.workflow.loop_body_label', 'Loop Body'))}</strong>
                    </div>
                `;

                const bodyNodes = Array.isArray(node.body) ? node.body : [];
                node.body = bodyNodes;
                this.renderNodes(bodyNodes, bodyContainer, level + 1);

                const addNestedBtn = document.createElement('button');
                addNestedBtn.className = 'btn btn-sm btn-outline-primary';
                addNestedBtn.innerHTML = `<i class="bi bi-plus-lg"></i> ${this.escapeHtml(this.t('ui.workflow.add_loop_node', 'Add Node to Loop'))}`;
                addNestedBtn.onclick = () => this.addNode(bodyNodes);
                bodyContainer.appendChild(addNestedBtn);

                nodeCard.appendChild(bodyContainer);
            }

            container.appendChild(nodeCard);
        });
    },

    renderPluginOptions(selectedType) {
        const entries = Object.entries(this.pluginDefinitions);
        return entries.map(([type, def]) => {
            const label = this.t(def.label || '', def.label || type);
            return `<option value="${this.escapeHtml(type)}" ${type === selectedType ? 'selected' : ''}>${this.escapeHtml(label)}</option>`;
        }).join('');
    },

    renderNodeFields(pluginDef, node) {
        const inputs = pluginDef.inputs || {};
        const outputs = pluginDef.outputs || {};
        const inputFields = this.renderFieldGroup(inputs, node.inputs || {}, 'inputs');
        const outputFields = this.renderFieldGroup(outputs, node.outputs || {}, 'outputs');

        return `
            <div class="amb-workflow-node-section">
                <h6>${this.escapeHtml(this.t('ui.workflow.inputs_label', 'Inputs'))}</h6>
                ${inputFields || `<p class="text-muted small mb-0">${this.escapeHtml(this.t('ui.workflow.no_inputs', 'No inputs'))}</p>`}
            </div>
            <div class="amb-workflow-node-section">
                <h6>${this.escapeHtml(this.t('ui.workflow.outputs_label', 'Outputs'))}</h6>
                ${outputFields || `<p class="text-muted small mb-0">${this.escapeHtml(this.t('ui.workflow.no_outputs', 'No outputs'))}</p>`}
            </div>
        `;
    },

    renderFieldGroup(definitions, values, group) {
        const fields = Object.entries(definitions || {});
        if (!fields.length) return '';

        return fields.map(([name, def]) => {
            const value = values[name] !== undefined ? values[name] : def.default ?? '';
            const labelText = this.t(def.label || '', def.label || name);
            const type = def.type || 'text';
            const optionLabels = def.option_labels || [];
            const inputId = `node-${name}-${Math.random().toString(36).slice(2)}`;

            let inputHtml = '';
            if (type === 'checkbox') {
                inputHtml = `
                    <div class="form-check">
                        <input type="checkbox" class="form-check-input" id="${inputId}"
                               data-field-name="${this.escapeHtml(name)}" data-field-type="${type}" data-field-group="${group}"
                               ${value ? 'checked' : ''}>
                    </div>
                `;
            } else if (type === 'select') {
                inputHtml = `
                    <select class="form-select form-select-sm" id="${inputId}"
                            data-field-name="${this.escapeHtml(name)}" data-field-type="${type}" data-field-group="${group}">
                        ${def.options.map((option, idx) => {
                            const label = optionLabels[idx]
                                ? this.t(optionLabels[idx], optionLabels[idx])
                                : option;
                            return `<option value="${this.escapeHtml(option)}" ${value === option ? 'selected' : ''}>${this.escapeHtml(label)}</option>`;
                        }).join('')}
                    </select>
                `;
            } else if (type === 'textarea') {
                inputHtml = `
                    <textarea class="form-control form-control-sm" rows="3" id="${inputId}"
                              data-field-name="${this.escapeHtml(name)}" data-field-type="${type}" data-field-group="${group}">${this.escapeHtml(value)}</textarea>
                `;
            } else if (type === 'number') {
                inputHtml = `
                    <input type="number" class="form-control form-control-sm" id="${inputId}"
                           data-field-name="${this.escapeHtml(name)}" data-field-type="${type}" data-field-group="${group}"
                           value="${this.escapeHtml(value)}">
                `;
            } else {
                inputHtml = `
                    <input type="text" class="form-control form-control-sm" id="${inputId}"
                           data-field-name="${this.escapeHtml(name)}" data-field-type="${type}" data-field-group="${group}"
                           value="${this.escapeHtml(value)}">
                `;
            }

            return `
                <div class="amb-workflow-field">
                    <label class="form-label small text-muted mb-1" for="${inputId}">${this.escapeHtml(labelText)}</label>
                    ${inputHtml}
                </div>
            `;
        }).join('');
    },

    updateNodeType(node, newType) {
        node.type = newType;
        const def = this.pluginDefinitions[newType] || {};
        node.inputs = this.buildDefaultFields(def.inputs);
        node.outputs = this.buildDefaultFields(def.outputs);

        if (newType === 'control.loop') {
            node.body = Array.isArray(node.body) ? node.body : [];
        } else {
            delete node.body;
        }
    },

    buildDefaultFields(definitions) {
        const result = {};
        Object.entries(definitions || {}).forEach(([name, def]) => {
            if (def.default !== undefined && def.default !== '') {
                result[name] = def.default;
            }
        });
        return result;
    },

    addNode(targetArray) {
        const types = Object.keys(this.pluginDefinitions);
        const defaultType = types[0] || '';
        const node = {
            id: this.generateNodeId(defaultType, targetArray),
            type: defaultType,
            inputs: this.buildDefaultFields(this.pluginDefinitions[defaultType]?.inputs),
            outputs: this.buildDefaultFields(this.pluginDefinitions[defaultType]?.outputs)
        };
        targetArray.push(node);
        this.render();
    },

    moveNode(nodes, idx, dir) {
        const target = idx + dir;
        if (target < 0 || target >= nodes.length) return;
        [nodes[idx], nodes[target]] = [nodes[target], nodes[idx]];
        this.render();
    },

    removeNode(nodes, idx) {
        nodes.splice(idx, 1);
        this.render();
    },

    generateNodeId(type, nodes) {
        const base = type ? type.split('.').pop() : 'node';
        const existing = new Set((nodes || []).map(node => node.id));
        let counter = nodes.length + 1;
        let candidate = `${base}_${counter}`;
        while (existing.has(candidate)) {
            counter += 1;
            candidate = `${base}_${counter}`;
        }
        return candidate;
    },

    sync() {
        if (this.textarea) {
            this.textarea.value = JSON.stringify(this.workflow, null, 2);
        }
    },

    toggleRaw() {
        if (!this.textarea) return;

        this.textarea.classList.toggle('d-none');
        if (!this.textarea.classList.contains('d-none')) {
            this.textarea.oninput = () => {
                try {
                    const parsed = JSON.parse(this.textarea.value || '{}');
                    this.workflow = parsed && parsed.nodes ? parsed : { nodes: [] };
                    this.render();
                } catch (e) {
                    // Ignore invalid JSON while editing
                }
            };
        }
    },

    loadWorkflow(workflow) {
        if (!workflow || !Array.isArray(workflow.nodes)) {
            this.workflow = { nodes: [] };
        } else {
            this.workflow = workflow;
        }
        this.render();
    },

    escapeHtml(text) {
        if (text === null || text === undefined) return '';
        const div = document.createElement('div');
        div.textContent = String(text);
        return div.innerHTML;
    }
};

window.WorkflowBuilder = WorkflowBuilder;
