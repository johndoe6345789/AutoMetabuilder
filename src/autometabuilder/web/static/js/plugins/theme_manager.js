/**
 * AutoMetabuilder - Theme Manager
 */
(() => {
    const ThemeManager = {
        STORAGE_KEY: 'amb-theme',

        init() {
            const saved = localStorage.getItem(this.STORAGE_KEY);
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            const theme = saved || (prefersDark ? 'dark' : 'light');
            this.setTheme(theme);

            document.querySelectorAll('[data-theme-toggle]').forEach(btn => {
                btn.addEventListener('click', () => this.toggle());
            });

            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
                if (!localStorage.getItem(this.STORAGE_KEY)) {
                    this.setTheme(e.matches ? 'dark' : 'light');
                }
            });
        },

        setTheme(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem(this.STORAGE_KEY, theme);
            this.updateToggleIcon(theme);
        },

        toggle() {
            const current = document.documentElement.getAttribute('data-theme');
            this.setTheme(current === 'dark' ? 'light' : 'dark');
        },

        updateToggleIcon(theme) {
            document.querySelectorAll('[data-theme-toggle] i').forEach(icon => {
                icon.className = theme === 'dark' ? 'bi bi-moon-fill' : 'bi bi-sun-fill';
            });
        }
    };

    window.ThemeManager = ThemeManager;
    window.AMBPlugins?.register('theme_manager', async () => ThemeManager.init());
})();
