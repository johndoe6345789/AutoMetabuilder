/**
 * AutoMetabuilder - Form Validator
 */
(() => {
    const FormValidator = {
        init() {
            document.querySelectorAll('form[data-validate]').forEach(form => {
                form.addEventListener('submit', event => {
                    if (!form.checkValidity()) {
                        event.preventDefault();
                        event.stopPropagation();
                    }
                    form.classList.add('was-validated');
                });
            });
        }
    };

    window.FormValidator = FormValidator;
    window.AMBPlugins?.register('form_validator', async () => FormValidator.init());
})();
