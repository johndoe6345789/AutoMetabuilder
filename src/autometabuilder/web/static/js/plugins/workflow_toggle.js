/**
 * AutoMetabuilder - Workflow Toggle
 */
(() => {
    const WorkflowToggle = {
        init() {
            document.querySelectorAll('[data-workflow-toggle]').forEach(button => {
                button.addEventListener('click', () => {
                    const builder = window.WorkflowBuilder;
                    if (builder && builder.textarea && typeof builder.toggleRaw === 'function') {
                        builder.toggleRaw();
                        return;
                    }
                    const textarea = document.getElementById('workflow-content');
                    if (textarea) {
                        textarea.classList.toggle('d-none');
                    }
                });
            });
        }
    };

    window.WorkflowToggle = WorkflowToggle;
    window.AMBPlugins?.register('workflow_toggle', async () => WorkflowToggle.init());
})();
