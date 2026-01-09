/**
 * AutoMetabuilder - Workflow Palette
 */
(() => {
    const state = {
        container: null,
        searchInput: null,
        list: null,
        filter: ''
    };

    const groupOrder = ['core', 'tools', 'utils', 'control', 'other'];
    const groupLabelKeys = {
        core: 'ui.workflow.palette.group.core',
        tools: 'ui.workflow.palette.group.tools',
        utils: 'ui.workflow.palette.group.utils',
        control: 'ui.workflow.palette.group.control',
        other: 'ui.workflow.palette.group.other'
    };

    const getGroupKey = (type) => (type || '').split('.')[0] || 'other';

    const buildEntries = (definitions, t) => Object.entries(definitions || {}).map(([key, def]) => {
        const label = t?.(def.label || '', def.label || key) || key;
        return {
            key,
            label,
            group: getGroupKey(key),
            search: `${key} ${label}`.toLowerCase()
        };
    });

    const render = () => {
        const { t, escapeHtml } = window.AMBWorkflowUtils || {};
        const definitions = window.AMBWorkflowState?.state?.pluginDefinitions || {};
        if (!state.list) return;
        const term = state.filter.toLowerCase();
        const entries = buildEntries(definitions, t).filter(entry => !term || entry.search.includes(term));
        if (!entries.length) {
            state.list.innerHTML = `<p class="text-muted small mb-0">${escapeHtml ? escapeHtml(t?.('ui.workflow.palette.empty', 'No matching nodes.')) : t?.('ui.workflow.palette.empty', 'No matching nodes.')}</p>`;
            return;
        }

        const grouped = entries.reduce((acc, entry) => {
            const group = groupOrder.includes(entry.group) ? entry.group : 'other';
            acc[group] = acc[group] || [];
            acc[group].push(entry);
            return acc;
        }, {});

        const groupsHtml = groupOrder.filter(group => grouped[group]?.length).map(group => {
            const groupLabel = t?.(groupLabelKeys[group], group) || group;
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

        render();
    };

    window.AMBWorkflowPalette = { init, render };
})();
