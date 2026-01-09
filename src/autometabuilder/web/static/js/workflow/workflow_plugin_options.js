/**
 * AutoMetabuilder - Workflow Plugin Options
 */
(() => {
    const render = (selectedType) => {
        const { t, escapeHtml } = window.AMBWorkflowUtils || {};
        const definitions = window.AMBWorkflowState?.state?.pluginDefinitions || {};
        return Object.entries(definitions).map(([type, def]) => {
            const label = t?.(def.label || '', def.label || type);
            const safeLabel = escapeHtml ? escapeHtml(label) : label;
            const safeType = escapeHtml ? escapeHtml(type) : type;
            const selected = type === selectedType ? 'selected' : '';
            return `<option value="${safeType}" ${selected}>${safeLabel}</option>`;
        }).join('');
    };

    window.AMBWorkflowPluginOptions = { render };
})();
