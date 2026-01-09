/**
 * AutoMetabuilder - Run Mode Toggle
 */
(() => {
    const updateIterationsGroup = () => {
        const group = document.getElementById('iterations-group');
        if (!group) return;
        const isIterations = document.getElementById('mode-iterations')?.checked;
        group.style.display = isIterations ? 'flex' : 'none';
        const input = group.querySelector('input[name="iterations"]');
        if (input) {
            input.disabled = !isIterations;
        }
    };

    const init = async () => {
        document.querySelectorAll('input[name="mode"]').forEach(radio => {
            radio.addEventListener('change', updateIterationsGroup);
        });
        updateIterationsGroup();
    };

    window.AMBPlugins?.register('run_mode_toggle', init);
})();
