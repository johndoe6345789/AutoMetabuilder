(() => {
    const state = {
        container: null,
        searchInput: null,
        list: null,
        filter: '',
        ready: false,
        loading: false
    };
    const getGroupKey = (type) => (type || '').split('.')[0] || 'other';
    const buildEntries = (definitions, t) => Object.entries(definitions || {}).map(([key, def]) => ({ key, label: t?.(def.label || '', def.label || key) || key, group: getGroupKey(key), search: `${key} ${t?.(def.label || '', def.label || key) || key}`.toLowerCase() }));
    const loadDefinitions = async () => {
        if (state.loading) return;
        state.loading = true;
        try {
            const response = await fetch('/api/workflow/plugins', { credentials: 'include', headers: window.AMBContext?.authHeaders || {} });
            if (response.ok) {
                window.AMBWorkflowState?.setPlugins?.(await response.json());
            }
        } catch (error) {
            console.error('Workflow palette fetch failed', error);
        }
        state.loading = false;
        render();
    };
    const render = () => {
        const { t, escapeHtml } = window.AMBWorkflowUtils || {};
        const definitions = window.AMBWorkflowState?.state?.pluginDefinitions || {};
        if (!state.list) return;
        if (!Object.keys(definitions).length) {
            if (!state.loading) {
                loadDefinitions();
            }
            const loadingText = t?.('ui.workflow.palette.loading', 'Loading nodes...');
            state.list.innerHTML = `<p class="text-muted small mb-0">${escapeHtml ? escapeHtml(loadingText) : loadingText}</p>`;
            return;
        }
        const term = state.filter.toLowerCase();
        const entries = buildEntries(definitions, t).filter(entry => !term || entry.search.includes(term));
        if (!entries.length) {
            state.list.innerHTML = `<p class="text-muted small mb-0">${escapeHtml ? escapeHtml(t?.('ui.workflow.palette.empty', 'No matching nodes.')) : t?.('ui.workflow.palette.empty', 'No matching nodes.')}</p>`;
            return;
        }
        const grouped = entries.reduce((acc, entry) => {
            const group = entry.group || 'other';
            acc[group] = acc[group] || [];
            acc[group].push(entry);
            return acc;
        }, {});
        const groupNames = Object.keys(grouped).sort((a, b) => (a === 'other') - (b === 'other') || a.localeCompare(b));
        const groupsHtml = groupNames.map(group => {
            const groupLabelKey = `ui.workflow.palette.group.${group}`;
            const groupLabel = t?.(groupLabelKey, group) || group;
            const items = grouped[group].map(entry => {
                const safeLabel = escapeHtml ? escapeHtml(entry.label) : entry.label;
                const safeKey = escapeHtml ? escapeHtml(entry.key) : entry.key;
                return `
                    <button type="button" class="amb-workflow-palette-item" data-node-type="${safeKey}">
                        <span class="amb-workflow-palette-title">${safeLabel}</span>
                        <span class="amb-workflow-palette-subtitle">${safeKey}</span>
                    </button>
                `;
            }).join('');
            return `
                <div class="amb-workflow-palette-group">
                    <div class="amb-workflow-palette-heading">${escapeHtml ? escapeHtml(groupLabel) : groupLabel}</div>
                    <div class="amb-workflow-palette-items">${items}</div>
                </div>
            `;
        }).join('');
        state.list.innerHTML = groupsHtml;
    };
    const init = () => {
        if (state.ready) {
            render();
            return;
        }
        state.container = document.getElementById('workflow-palette');
        state.searchInput = document.getElementById('workflow-palette-search');
        state.list = document.getElementById('workflow-palette-list');
        if (!state.container || !state.searchInput || !state.list) return;
        state.searchInput.addEventListener('input', (event) => {
            state.filter = event.target.value || '';
            render();
        });
        state.list.addEventListener('click', (event) => {
            const target = event.target.closest('.amb-workflow-palette-item');
            if (!target) return;
            const nodeType = target.dataset.nodeType;
            const workflowState = window.AMBWorkflowState?.state;
            if (!workflowState || !nodeType) return;
            window.AMBWorkflowMutations?.addNode(workflowState.workflow.nodes, workflowState.pluginDefinitions, nodeType);
            window.AMBWorkflowCanvasRenderer?.render?.();
        });
        state.ready = true;
        render();
    };
    window.AMBWorkflowPalette = { init, render };
})();
