/**
 * AutoMetabuilder - Workflow Builder
 */

const WorkflowBuilder = {
    workflow: [],
    stepDefinitions: {},
    allSuggestions: new Set(),
    container: null,
    textarea: null,

    t(key, fallback = '') {
        const dict = window.AMB_I18N || {};
        return dict[key] || fallback || key;
    },

    format(text, values = {}) {
        return text.replace(/\{(\w+)\}/g, (_, name) => values[name] ?? '');
    },

    init(containerId, textareaId, stepDefinitions) {
        this.container = document.getElementById(containerId);
        this.textarea = document.getElementById(textareaId);
        this.stepDefinitions = stepDefinitions || {};

        // Build all suggestions set
        Object.values(this.stepDefinitions).forEach(def => {
            Object.values(def.fields || {}).forEach(f => {
                if (f.suggestions) {
                    f.suggestions.forEach(s => this.allSuggestions.add(s));
                }
            });
        });

        // Parse initial workflow
        try {
            this.workflow = JSON.parse(this.textarea.value || '[]');
        } catch (e) {
            console.error('Failed to parse workflow JSON', e);
            this.workflow = [];
        }

        this.render();
    },

    render() {
        if (!this.container) return;

        this.container.innerHTML = '';

        if (this.workflow.length === 0) {
            this.container.innerHTML = `
                <div class="text-center text-muted py-4">
                    <i class="bi bi-diagram-3" style="font-size: 2.5rem;"></i>
                    <p class="mt-2">${this.escapeHtml(this.t('ui.workflow.empty', 'No tasks yet. Click \"Add Task\" to create your first workflow task.'))}</p>
                </div>
            `;
        }

        this.workflow.forEach((task, taskIdx) => {
            const taskCard = document.createElement('div');
            taskCard.className = 'amb-workflow-task mb-4';
            taskCard.innerHTML = `
                <div class="amb-workflow-task-header">
                    <div class="amb-workflow-task-main">
                        <span class="amb-workflow-badge">${this.escapeHtml(this.format(this.t('ui.workflow.task_label', 'Task {number}'), { number: taskIdx + 1 }))}</span>
                        <input type="text" class="form-control form-control-sm amb-workflow-input amb-workflow-title"
                               value="${this.escapeHtml(task.name || this.t('ui.workflow.untitled_task', 'Untitled Task'))}"
                               onchange="WorkflowBuilder.updateTask(${taskIdx}, 'name', this.value)"
                               placeholder="${this.escapeHtml(this.t('ui.workflow.task_name_placeholder', 'Task Name'))}">
                        <select class="form-select form-select-sm amb-workflow-input amb-workflow-type"
                                onchange="WorkflowBuilder.updateTask(${taskIdx}, 'type', this.value)">
                            <option value="" ${!task.type ? 'selected' : ''}>${this.escapeHtml(this.t('ui.workflow.type.standard', 'Standard'))}</option>
                            <option value="loop" ${task.type === 'loop' ? 'selected' : ''}>${this.escapeHtml(this.t('ui.workflow.type.loop', 'Loop'))}</option>
                        </select>
                        ${task.type === 'loop' ? `
                            <div class="amb-workflow-inline">
                                <span class="amb-workflow-meta">${this.escapeHtml(this.t('ui.workflow.max_label', 'Max'))}</span>
                                <input type="number" class="form-control form-control-sm amb-workflow-input"
                                       value="${task.max_iterations || 10}" min="1"
                                       onchange="WorkflowBuilder.updateTask(${taskIdx}, 'max_iterations', parseInt(this.value))">
                            </div>
                        ` : ''}
                    </div>
                    <div class="amb-workflow-task-actions">
                        <button class="btn btn-sm btn-outline-secondary amb-icon-btn" onclick="WorkflowBuilder.moveTask(${taskIdx}, -1)"
                                ${taskIdx === 0 ? 'disabled' : ''} title="${this.escapeHtml(this.t('ui.workflow.move_up', 'Move up'))}">
                            <i class="bi bi-chevron-up"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-secondary amb-icon-btn" onclick="WorkflowBuilder.moveTask(${taskIdx}, 1)"
                                ${taskIdx === this.workflow.length - 1 ? 'disabled' : ''} title="${this.escapeHtml(this.t('ui.workflow.move_down', 'Move down'))}">
                            <i class="bi bi-chevron-down"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger amb-icon-btn" onclick="WorkflowBuilder.removeTask(${taskIdx})"
                                title="${this.escapeHtml(this.t('ui.workflow.delete_task', 'Delete task'))}">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </div>
                <div class="amb-workflow-task-body">
                    <div class="steps-container" id="steps-${taskIdx}"></div>
                    <button class="btn btn-sm btn-outline-primary" onclick="WorkflowBuilder.addStep(${taskIdx})">
                        <i class="bi bi-plus-lg"></i> ${this.escapeHtml(this.t('ui.workflow.add_step', 'Add Step'))}
                    </button>
                </div>
            `;
            this.container.appendChild(taskCard);

            const stepsContainer = taskCard.querySelector(`#steps-${taskIdx}`);
            (task.steps || []).forEach((step, stepIdx) => {
                const stepDiv = this.createStepElement(task, taskIdx, step, stepIdx);
                stepsContainer.appendChild(stepDiv);
            });
        });

        // Add task button
        const addTaskBtn = document.createElement('button');
        addTaskBtn.className = 'btn btn-primary';
        addTaskBtn.innerHTML = `<i class="bi bi-plus-lg"></i> ${this.escapeHtml(this.t('ui.workflow.add_task', 'Add Task'))}`;
        addTaskBtn.onclick = () => this.addTask();
        this.container.appendChild(addTaskBtn);

        this.sync();
    },

    createStepElement(task, taskIdx, step, stepIdx) {
        const stepDiv = document.createElement('div');
        stepDiv.className = 'amb-workflow-step';

        const stepDef = this.stepDefinitions[step.type];
        const stepLabel = stepDef
            ? this.t(stepDef.label || '', stepDef.label || '')
            : this.t('ui.workflow.select_action', 'Select action...');

        let fieldsHtml = '';
        if (step.type && stepDef) {
            fieldsHtml = '<div class="row g-2 mt-2">';
            Object.entries(stepDef.fields || {}).forEach(([field, fieldDef]) => {
                const val = step[field] !== undefined ? step[field] : fieldDef.default || '';
                const fieldType = fieldDef.type || 'text';
                const suggestions = fieldDef.suggestions || Array.from(this.allSuggestions);
                const options = fieldDef.options || suggestions;
                const optionLabels = fieldDef.option_labels || [];
                const selectLabel = fieldDef.placeholder
                    ? this.t(fieldDef.placeholder, fieldDef.placeholder)
                    : this.t('ui.common.select_placeholder', 'Select...');
                const fieldId = `workflow-${taskIdx}-${stepIdx}-${field}`;
                const labelValue = fieldDef.label ? this.t(fieldDef.label, fieldDef.label) : field;
                const labelText = this.escapeHtml(labelValue);
                const placeholder = fieldDef.placeholder
                    ? this.escapeHtml(this.t(fieldDef.placeholder, fieldDef.placeholder))
                    : '';

                let inputHtml = '';
                if (fieldType === 'checkbox') {
                    inputHtml = `
                        <div class="form-check">
                            <input type="checkbox" class="form-check-input"
                                   ${step[field] ? 'checked' : ''}
                                   onchange="WorkflowBuilder.updateStepField(${taskIdx}, ${stepIdx}, '${field}', this.checked)">
                            <label class="form-check-label small">${this.escapeHtml(this.t('ui.workflow.field.enable', 'Enable'))}</label>
                        </div>
                    `;
                } else if (fieldType === 'select') {
                    inputHtml = `
                        <select class="form-select form-select-sm"
                                onchange="WorkflowBuilder.updateStepField(${taskIdx}, ${stepIdx}, '${field}', this.value)">
                            <option value="">${this.escapeHtml(selectLabel)}</option>
                            ${options.map((option, idx) => {
                                const label = optionLabels[idx]
                                    ? this.t(optionLabels[idx], optionLabels[idx])
                                    : option;
                                return `<option value="${this.escapeHtml(option)}" ${val === option ? 'selected' : ''}>${this.escapeHtml(label)}</option>`;
                            }).join('')}
                        </select>
                    `;
                } else if (fieldType === 'number') {
                    const min = fieldDef.min !== undefined ? `min="${fieldDef.min}"` : '';
                    const max = fieldDef.max !== undefined ? `max="${fieldDef.max}"` : '';
                    const stepAttr = fieldDef.step !== undefined ? `step="${fieldDef.step}"` : '';
                    inputHtml = `
                        <input type="number" class="form-control form-control-sm"
                               value="${this.escapeHtml(val)}" ${min} ${max} ${stepAttr}
                               placeholder="${placeholder}"
                               onchange="WorkflowBuilder.updateStepField(${taskIdx}, ${stepIdx}, '${field}', parseFloat(this.value))">
                    `;
                } else if (fieldType === 'textarea') {
                    inputHtml = `
                        <textarea class="form-control form-control-sm" rows="3"
                                  placeholder="${placeholder}"
                                  oninput="WorkflowBuilder.updateStepField(${taskIdx}, ${stepIdx}, '${field}', this.value)">${this.escapeHtml(val)}</textarea>
                    `;
                } else {
                    const listId = suggestions.length ? `list="${fieldId}-list"` : '';
                    const listHtml = suggestions.length
                        ? `<datalist id="${fieldId}-list">${suggestions.map(s =>
                            `<option value="${this.escapeHtml(s)}"></option>`
                        ).join('')}</datalist>`
                        : '';
                    inputHtml = `
                        <input type="text" class="form-control form-control-sm"
                               value="${this.escapeHtml(val)}" ${listId}
                               placeholder="${placeholder}"
                               oninput="WorkflowBuilder.updateStepField(${taskIdx}, ${stepIdx}, '${field}', this.value)">
                        ${listHtml}
                    `;
                }

                fieldsHtml += `
                    <div class="col-md-6 amb-workflow-field">
                        <label class="form-label small text-muted mb-1">${labelText}</label>
                        ${inputHtml}
                    </div>
                `;
            });
            fieldsHtml += '</div>';
        }

        stepDiv.innerHTML = `
            <div class="amb-workflow-step-header">
                <div class="amb-workflow-step-main">
                    <span class="amb-workflow-step-badge">${stepIdx + 1}</span>
                    <select class="form-select form-select-sm amb-workflow-step-select"
                            onchange="WorkflowBuilder.updateStepType(${taskIdx}, ${stepIdx}, this.value)">
                        <option value="">${this.escapeHtml(this.t('ui.workflow.step_type_placeholder', 'Select action type...'))}</option>
                        ${Object.entries(this.stepDefinitions).map(([type, def]) => {
                            const label = this.t(def.label || '', def.label || '');
                            return `<option value="${type}" ${step.type === type ? 'selected' : ''}>${this.escapeHtml(label)}</option>`;
                        }).join('')}
                    </select>
                    ${step.type ? `<span class="amb-workflow-step-hint"><i class="bi bi-arrow-right"></i></span>` : ''}
                </div>
                <div class="amb-workflow-step-actions">
                    <button class="btn btn-sm btn-outline-secondary amb-icon-btn" onclick="WorkflowBuilder.moveStep(${taskIdx}, ${stepIdx}, -1)"
                            ${stepIdx === 0 ? 'disabled' : ''} title="${this.escapeHtml(this.t('ui.workflow.move_up', 'Move up'))}">
                        <i class="bi bi-chevron-up"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-secondary amb-icon-btn" onclick="WorkflowBuilder.moveStep(${taskIdx}, ${stepIdx}, 1)"
                            ${stepIdx === (task.steps || []).length - 1 ? 'disabled' : ''} title="${this.escapeHtml(this.t('ui.workflow.move_down', 'Move down'))}">
                        <i class="bi bi-chevron-down"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger amb-icon-btn" onclick="WorkflowBuilder.removeStep(${taskIdx}, ${stepIdx})"
                            title="${this.escapeHtml(this.t('ui.workflow.remove_step', 'Remove step'))}">
                        <i class="bi bi-x-lg"></i>
                    </button>
                </div>
            </div>
            ${fieldsHtml}
        `;

        return stepDiv;
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
                    this.workflow = JSON.parse(this.textarea.value);
                    this.render();
                } catch (e) {
                    // Invalid JSON, ignore
                }
            };
        }
    },

    updateTask(idx, field, value) {
        this.workflow[idx][field] = value;
        if (field === 'type' && value !== 'loop') {
            delete this.workflow[idx].max_iterations;
        } else if (field === 'type' && value === 'loop' && !this.workflow[idx].max_iterations) {
            this.workflow[idx].max_iterations = 10;
        }
        this.render();
    },

    addTask() {
        this.workflow.push({ name: this.t('ui.workflow.new_task', 'New Task'), steps: [] });
        this.render();
    },

    removeTask(idx) {
        if (confirm(this.t('ui.workflow.delete_task_confirm', 'Remove this task and all its steps?'))) {
            this.workflow.splice(idx, 1);
            this.render();
        }
    },

    moveTask(idx, dir) {
        const target = idx + dir;
        if (target >= 0 && target < this.workflow.length) {
            [this.workflow[idx], this.workflow[target]] = [this.workflow[target], this.workflow[idx]];
            this.render();
        }
    },

    updateStepType(taskIdx, stepIdx, type) {
        const newStep = { type: type };
        if (this.stepDefinitions[type]) {
            Object.entries(this.stepDefinitions[type].fields || {}).forEach(([field, fieldDef]) => {
                newStep[field] = fieldDef.default;
            });
        }
        this.workflow[taskIdx].steps[stepIdx] = newStep;
        this.render();
    },

    updateStepField(taskIdx, stepIdx, field, value) {
        this.workflow[taskIdx].steps[stepIdx][field] = value;
        this.sync();
    },

    addStep(taskIdx) {
        if (!this.workflow[taskIdx].steps) {
            this.workflow[taskIdx].steps = [];
        }
        this.workflow[taskIdx].steps.push({ type: '' });
        this.render();
    },

    removeStep(taskIdx, stepIdx) {
        this.workflow[taskIdx].steps.splice(stepIdx, 1);
        this.render();
    },

    moveStep(taskIdx, stepIdx, dir) {
        const target = stepIdx + dir;
        const steps = this.workflow[taskIdx].steps;
        if (target >= 0 && target < steps.length) {
            [steps[stepIdx], steps[target]] = [steps[target], steps[stepIdx]];
            this.render();
        }
    },

    escapeHtml(text) {
        if (text === null || text === undefined) return '';
        const div = document.createElement('div');
        div.textContent = String(text);
        return div.innerHTML;
    }
};

// Export globally
window.WorkflowBuilder = WorkflowBuilder;
