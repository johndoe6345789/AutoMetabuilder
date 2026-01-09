/**
 * AutoMetabuilder - Workflow Field Renderer
 */
(() => {
    const renderFieldGroup = (definitions, values, group) => {
        const { t, escapeHtml } = window.AMBWorkflowUtils || {};
        const fields = Object.entries(definitions || {});
        if (!fields.length) return '';

        return fields.map(([name, def]) => {
            const value = values[name] !== undefined ? values[name] : def.default ?? '';
            const labelText = t?.(def.label || '', def.label || name);
            const type = def.type || 'text';
            const optionLabels = def.option_labels || [];
            const inputId = `node-${name}-${Math.random().toString(36).slice(2)}`;
            const safeName = escapeHtml ? escapeHtml(name) : name;
            const safeLabel = escapeHtml ? escapeHtml(labelText) : labelText;

            let inputHtml = '';
            if (type === 'checkbox') {
                inputHtml = `
                    <div class="form-check">
                        <input type="checkbox" class="form-check-input" id="${inputId}"
                               data-field-name="${safeName}" data-field-type="${type}" data-field-group="${group}"
                               ${value ? 'checked' : ''}>
                    </div>
                `;
            } else if (type === 'select') {
                const optionsHtml = (def.options || []).map((option, idx) => {
                    const label = optionLabels[idx]
                        ? t?.(optionLabels[idx], optionLabels[idx])
                        : option;
                    const safeOption = escapeHtml ? escapeHtml(option) : option;
                    const safeOptionLabel = escapeHtml ? escapeHtml(label) : label;
                    return `<option value="${safeOption}" ${value === option ? 'selected' : ''}>${safeOptionLabel}</option>`;
                }).join('');
                inputHtml = `
                    <select class="form-select form-select-sm" id="${inputId}"
                            data-field-name="${safeName}" data-field-type="${type}" data-field-group="${group}">
                        ${optionsHtml}
                    </select>
                `;
            } else if (type === 'textarea') {
                inputHtml = `
                    <textarea class="form-control form-control-sm" rows="3" id="${inputId}"
                              data-field-name="${safeName}" data-field-type="${type}" data-field-group="${group}">${escapeHtml ? escapeHtml(value) : value}</textarea>
                `;
            } else if (type === 'number') {
                inputHtml = `
                    <input type="number" class="form-control form-control-sm" id="${inputId}"
                           data-field-name="${safeName}" data-field-type="${type}" data-field-group="${group}"
                           value="${escapeHtml ? escapeHtml(value) : value}">
                `;
            } else {
                inputHtml = `
                    <input type="text" class="form-control form-control-sm" id="${inputId}"
                           data-field-name="${safeName}" data-field-type="${type}" data-field-group="${group}"
                           value="${escapeHtml ? escapeHtml(value) : value}">
                `;
            }

            return `
                <div class="amb-workflow-field">
                    <label class="form-label small text-muted mb-1" for="${inputId}">${safeLabel}</label>
                    ${inputHtml}
                </div>
            `;
        }).join('');
    };

    const renderNodeFields = (pluginDef, node) => {
        const { t, escapeHtml } = window.AMBWorkflowUtils || {};
        const inputs = pluginDef.inputs || {};
        const outputs = pluginDef.outputs || {};
        const inputFields = renderFieldGroup(inputs, node.inputs || {}, 'inputs');
        const outputFields = renderFieldGroup(outputs, node.outputs || {}, 'outputs');

        return `
            <div class="amb-workflow-node-section">
                <h6>${escapeHtml ? escapeHtml(t?.('ui.workflow.inputs_label', 'Inputs')) : t?.('ui.workflow.inputs_label', 'Inputs')}</h6>
                ${inputFields || `<p class="text-muted small mb-0">${escapeHtml ? escapeHtml(t?.('ui.workflow.no_inputs', 'No inputs')) : t?.('ui.workflow.no_inputs', 'No inputs')}</p>`}
            </div>
            <div class="amb-workflow-node-section">
                <h6>${escapeHtml ? escapeHtml(t?.('ui.workflow.outputs_label', 'Outputs')) : t?.('ui.workflow.outputs_label', 'Outputs')}</h6>
                ${outputFields || `<p class="text-muted small mb-0">${escapeHtml ? escapeHtml(t?.('ui.workflow.no_outputs', 'No outputs')) : t?.('ui.workflow.no_outputs', 'No outputs')}</p>`}
            </div>
        `;
    };

    window.AMBWorkflowFieldRenderer = {
        renderFieldGroup,
        renderNodeFields
    };
})();
