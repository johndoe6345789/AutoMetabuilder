/**
 * AutoMetabuilder - Workflow Builder
 */

const WorkflowBuilder = {
    workflow: [],
    stepDefinitions: {},
    allSuggestions: new Set(),
    container: null,
    textarea: null,

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

        this.workflow.forEach((task, taskIdx) => {
            const taskCard = document.createElement('div');
            taskCard.className = 'amb-workflow-task';
            taskCard.innerHTML = `
                <div class="amb-workflow-task-header">
                    <div class="d-flex align-items-center gap-2 flex-grow-1">
                        <input type="text" class="form-control form-control-sm" style="max-width: 200px;"
                               value="${this.escapeHtml(task.name || '')}"
                               data-choices data-placeholder="Task name"
                               onchange="WorkflowBuilder.updateTask(${taskIdx}, 'name', this.value)"
                               placeholder="Task Name">
                        <select class="form-select form-select-sm" style="max-width: 160px;"
                                onchange="WorkflowBuilder.updateTask(${taskIdx}, 'type', this.value)">
                            <option value="" ${!task.type ? 'selected' : ''}>Standard</option>
                            <option value="loop" ${task.type === 'loop' ? 'selected' : ''}>Loop</option>
                        </select>
                        ${task.type === 'loop' ? `
                            <input type="number" class="form-control form-control-sm" style="max-width: 80px;"
                                   value="${task.max_iterations || 1}"
                                   onchange="WorkflowBuilder.updateTask(${taskIdx}, 'max_iterations', parseInt(this.value))"
                                   title="Max Iterations" min="1">
                        ` : ''}
                    </div>
                    <div class="d-flex align-items-center gap-1">
                        <button class="btn btn-sm btn-light" onclick="WorkflowBuilder.moveTask(${taskIdx}, -1)"
                                ${taskIdx === 0 ? 'disabled' : ''} title="Move up">
                            <i class="bi bi-arrow-up"></i>
                        </button>
                        <button class="btn btn-sm btn-light" onclick="WorkflowBuilder.moveTask(${taskIdx}, 1)"
                                ${taskIdx === this.workflow.length - 1 ? 'disabled' : ''} title="Move down">
                            <i class="bi bi-arrow-down"></i>
                        </button>
                        <button class="btn btn-sm btn-danger ms-1" onclick="WorkflowBuilder.removeTask(${taskIdx})"
                                title="Remove task">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </div>
                <div class="amb-workflow-task-body">
                    <div class="steps-container" id="steps-${taskIdx}"></div>
                    <button class="btn btn-sm btn-outline-primary mt-2" onclick="WorkflowBuilder.addStep(${taskIdx})">
                        <i class="bi bi-plus-lg"></i> Add Step
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
        addTaskBtn.innerHTML = '<i class="bi bi-plus-lg"></i> Add Task';
        addTaskBtn.onclick = () => this.addTask();
        this.container.appendChild(addTaskBtn);

        this.sync();

        // Reinitialize Choices.js for new elements
        if (window.ChoicesManager) {
            window.ChoicesManager.refresh();
        }
    },

    createStepElement(task, taskIdx, step, stepIdx) {
        const stepDiv = document.createElement('div');
        stepDiv.className = 'amb-workflow-step';

        let fieldsHtml = `
            <select class="form-select form-select-sm mb-2" data-choices
                    onchange="WorkflowBuilder.updateStepType(${taskIdx}, ${stepIdx}, this.value)">
                <option value="">Select action type...</option>
                ${Object.entries(this.stepDefinitions).map(([type, def]) =>
                    `<option value="${type}" ${step.type === type ? 'selected' : ''}>${this.escapeHtml(def.label)}</option>`
                ).join('')}
            </select>
        `;

        if (step.type && this.stepDefinitions[step.type]) {
            fieldsHtml += '<div class="row g-2 mt-2">';
            const def = this.stepDefinitions[step.type];
            Object.entries(def.fields || {}).forEach(([field, fieldDef]) => {
                const val = step[field] !== undefined ? step[field] : '';
                const isCheckbox = fieldDef.type === 'checkbox';
                const suggestions = fieldDef.suggestions || Array.from(this.allSuggestions);

                fieldsHtml += `
                    <div class="col-md-6">
                        <label class="form-label small fw-semibold">${this.escapeHtml(fieldDef.label)}</label>
                        ${isCheckbox ? `
                            <div class="form-check">
                                <input type="checkbox" class="form-check-input"
                                       ${step[field] ? 'checked' : ''}
                                       onchange="WorkflowBuilder.updateStepField(${taskIdx}, ${stepIdx}, '${field}', this.checked)">
                            </div>
                        ` : `
                            <select class="form-select form-select-sm" data-choices
                                    onchange="WorkflowBuilder.updateStepField(${taskIdx}, ${stepIdx}, '${field}', this.value)">
                                <option value="">${this.escapeHtml(fieldDef.default || 'Select...')}</option>
                                ${suggestions.map(s =>
                                    `<option value="${this.escapeHtml(s)}" ${val === s ? 'selected' : ''}>${this.escapeHtml(s)}</option>`
                                ).join('')}
                            </select>
                        `}
                    </div>
                `;
            });
            fieldsHtml += '</div>';
        }

        stepDiv.innerHTML = `
            <div class="amb-workflow-step-header">
                <span class="badge bg-secondary">Step ${stepIdx + 1}</span>
                <div class="d-flex align-items-center gap-1">
                    <button class="btn btn-sm btn-link p-0" onclick="WorkflowBuilder.moveStep(${taskIdx}, ${stepIdx}, -1)"
                            ${stepIdx === 0 ? 'disabled' : ''} title="Move up">
                        <i class="bi bi-arrow-up"></i>
                    </button>
                    <button class="btn btn-sm btn-link p-0" onclick="WorkflowBuilder.moveStep(${taskIdx}, ${stepIdx}, 1)"
                            ${stepIdx === (task.steps || []).length - 1 ? 'disabled' : ''} title="Move down">
                        <i class="bi bi-arrow-down"></i>
                    </button>
                    <button class="btn btn-sm btn-link p-0 text-danger" onclick="WorkflowBuilder.removeStep(${taskIdx}, ${stepIdx})"
                            title="Remove step">
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
        this.workflow.push({ name: 'New Task', steps: [] });
        this.render();
    },

    removeTask(idx) {
        if (confirm('Remove this task?')) {
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
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

// Export globally
window.WorkflowBuilder = WorkflowBuilder;
