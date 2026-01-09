/**
 * AutoMetabuilder - Workflow Templates
 */
(() => {
    const { t, authHeaders } = window.AMBContext || {};
    const fetchPackages = async () => {
        const response = await fetch('/api/workflow/packages', {
            credentials: 'include',
            headers: authHeaders || {}
        });
        if (!response.ok) {
            throw new Error(`Package fetch failed: ${response.status}`);
        }
        return response.json();
    };
    const fetchPackage = async (packageId) => {
        const response = await fetch(`/api/workflow/packages/${packageId}`, {
            credentials: 'include',
            headers: authHeaders || {}
        });
        if (!response.ok) {
            throw new Error(`Template fetch failed: ${response.status}`);
        }
        return response.json();
    };
    const init = async () => {
        const selectEl = document.getElementById('workflow-template-select');
        const descEl = document.getElementById('workflow-template-description');
        const applyBtn = document.getElementById('workflow-template-apply');
        if (!selectEl || !descEl || !applyBtn) return;
        let packages = [];
        try {
            const data = await fetchPackages();
            packages = data.packages || [];
        } catch (error) {
            console.error('Workflow template fetch failed', error);
            descEl.textContent = t?.('ui.workflow.templates.error', 'Unable to load templates.');
            return;
        }
        selectEl.innerHTML = '';
        const placeholder = document.createElement('option');
        placeholder.value = '';
        placeholder.textContent = t?.('ui.workflow.templates.select_placeholder', 'Select a template...');
        placeholder.disabled = true;
        placeholder.selected = true;
        selectEl.appendChild(placeholder);
        packages.forEach(pkg => {
            const option = document.createElement('option');
            option.value = pkg.id;
            option.textContent = t?.(pkg.label || pkg.id, pkg.label || pkg.id);
            selectEl.appendChild(option);
        });
        const updateDescription = () => {
            const selected = packages.find(pkg => pkg.id === selectEl.value);
            applyBtn.disabled = !selected;
            if (!selected) {
                descEl.textContent = t?.(
                    'ui.workflow.templates.description_placeholder',
                    'Choose a template to preview what it does.'
                );
                return;
            }
            descEl.textContent = t?.(selected.description || '', selected.description || '');
        };
        selectEl.addEventListener('change', updateDescription);
        updateDescription();
        applyBtn.addEventListener('click', async () => {
            const selected = packages.find(pkg => pkg.id === selectEl.value);
            if (!selected) return;
            const confirmText = t?.(
                'ui.workflow.templates.confirm_apply',
                'Replace the current workflow with this template?'
            );
            if (!confirm(confirmText)) return;

            try {
                const data = await fetchPackage(selected.id);
                const workflow = data.workflow || data;
                if (window.WorkflowBuilder?.loadWorkflow) {
                    window.WorkflowBuilder.loadWorkflow(workflow);
                }
                window.Toast?.show(t?.('ui.workflow.templates.loaded', 'Template loaded.'), 'success');
            } catch (error) {
                console.error('Workflow template load failed', error);
                alert(t?.('ui.workflow.templates.error_load', 'Unable to load the selected template.'));
            }
        });
    };
    window.AMBPlugins?.register('workflow_templates', init);
})();
