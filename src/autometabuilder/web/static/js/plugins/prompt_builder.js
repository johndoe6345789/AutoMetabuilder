/**
 * AutoMetabuilder - Prompt Builder
 */
(() => {
    const buildPromptYaml = () => {
        const rawPanel = document.getElementById('prompt-raw');
        if (rawPanel && !rawPanel.classList.contains('d-none')) {
            return;
        }

        const systemField = document.getElementById('system-prompt');
        const userField = document.getElementById('user-prompt');
        const modelSelect = document.querySelector('select[name="model"]');
        const outputField = document.getElementById('prompt-yaml');
        if (!systemField || !userField || !modelSelect || !outputField) return;

        const systemContent = systemField.value;
        const userContent = userField.value;
        const model = modelSelect.value;

        const yaml = `messages:
  - role: system
    content: >-
      ${systemContent.split('\n').join('\n      ')}
  - role: user
    content: >-
      ${userContent.split('\n').join('\n      ')}
model: ${model}
`;
        outputField.value = yaml;
    };

    const toggleRawPrompt = () => {
        const rawPanel = document.getElementById('prompt-raw');
        const builder = document.getElementById('prompt-builder');
        if (!rawPanel) return;

        if (rawPanel.classList.contains('d-none')) {
            buildPromptYaml();
            rawPanel.classList.remove('d-none');
            builder?.classList.add('d-none');
        } else {
            rawPanel.classList.add('d-none');
            builder?.classList.remove('d-none');
        }
        const modeInput = document.getElementById('prompt-mode');
        if (modeInput) {
            modeInput.value = rawPanel.classList.contains('d-none') ? 'builder' : 'raw';
        }
    };

    const init = async () => {
        document.querySelectorAll('[data-prompt-target]').forEach(button => {
            button.addEventListener('click', () => {
                const field = document.getElementById(button.dataset.promptTarget);
                if (!field) return;
                const current = field.value.trim();
                const spacer = current ? '\n' : '';
                field.value = `${current}${spacer}${button.dataset.promptSnippet || ''}`.trim();
                field.focus();
            });
        });

        document.getElementById('prompt-form')?.addEventListener('submit', () => {
            buildPromptYaml();
        });
    };

    window.buildPromptYaml = buildPromptYaml;
    window.toggleRawPrompt = toggleRawPrompt;
    window.AMBPlugins?.register('prompt_builder', init);
})();
