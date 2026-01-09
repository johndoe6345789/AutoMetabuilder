/**
 * AutoMetabuilder - Main JavaScript
 */
const I18N = window.AMB_I18N || {};
const i18n = (key, fallback = '') => I18N[key] || fallback || key;

/* ==========================================================================
   Theme Manager
   ========================================================================== */
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

        window.matchMedia('(prefers-color-scheme: dark)')
            .addEventListener('change', e => {
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

/* ==========================================================================
   Navigation Manager
   ========================================================================== */
const NavigationManager = {
    _popstateBound: false,

    init() {
        this.bindLinks();

        // Handle initial hash
        const hash = window.location.hash.slice(1);
        if (hash && document.querySelector(`#${hash}`)) {
            this.showSection(hash);
        }

        // Handle browser back/forward
        if (!this._popstateBound) {
            window.addEventListener('popstate', () => {
                const nextHash = window.location.hash.slice(1);
                if (nextHash && document.querySelector(`#${nextHash}`)) {
                    this.showSection(nextHash, false);
                }
            });
            this._popstateBound = true;
        }
    },

    bindLinks() {
        document.querySelectorAll('[data-section]').forEach(link => {
            if (link.dataset.navBound === 'true') return;
            link.dataset.navBound = 'true';
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = link.dataset.section;
                this.showSection(target);
            });
        });
    },

    refresh() {
        this.bindLinks();
        const hash = window.location.hash.slice(1);
        if (hash && document.querySelector(`#${hash}`)) {
            this.showSection(hash, false);
            return;
        }
        const firstLink = document.querySelector('[data-section]');
        if (firstLink) {
            this.showSection(firstLink.dataset.section, false);
        }
    },

    showSection(sectionId, updateHistory = true) {
        // Hide all sections
        document.querySelectorAll('.amb-section').forEach(s => s.classList.remove('active'));

        // Show target section
        const targetSection = document.querySelector(`#${sectionId}`);
        if (targetSection) {
            targetSection.classList.add('active');
        }

        // Update nav active state
        document.querySelectorAll('.amb-nav-link').forEach(n => n.classList.remove('active'));
        const activeLink = document.querySelector(`[data-section="${sectionId}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }

        // Update URL hash
        if (updateHistory) {
            history.pushState(null, '', `#${sectionId}`);
        }
    }
};

/* ==========================================================================
   Choices Manager
   ========================================================================== */
const ChoicesManager = {
    instances: [],

    init() {
        this.initAll();
    },

    initAll() {
        document.querySelectorAll('[data-choices]').forEach(el => {
            // Skip if already initialized
            if (el.classList.contains('choices__input')) return;

            const optionsStr = el.dataset.choicesOptions || '{}';
            let options = {};
            try {
                options = JSON.parse(optionsStr);
            } catch (e) {
                console.warn('Invalid choices options:', optionsStr);
            }

            const instance = new Choices(el, {
                searchEnabled: true,
                shouldSort: false,
                allowHTML: false,
                removeItemButton: options.removeItemButton || false,
                placeholder: true,
                placeholderValue: el.dataset.placeholder || i18n('ui.common.select_placeholder', 'Select...'),
                searchPlaceholderValue: i18n('ui.choices.search_placeholder', 'Type to search...'),
                noResultsText: i18n('ui.choices.no_results', 'No results found'),
                noChoicesText: i18n('ui.choices.no_choices', 'No choices available'),
                ...options
            });
            this.instances.push(instance);
        });
    },

    destroy() {
        this.instances.forEach(instance => {
            try {
                instance.destroy();
            } catch (e) {
                // Ignore errors from already destroyed instances
            }
        });
        this.instances = [];
    },

    refresh() {
        this.destroy();
        this.initAll();
    }
};

/* ==========================================================================
   Workflow Toggle
   ========================================================================== */
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

/* ==========================================================================
   Form Validator
   ========================================================================== */
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

/* ==========================================================================
   Status Poller
   ========================================================================== */
const StatusPoller = {
    logsInterval: null,
    statusInterval: null,

    init() {
        this.refreshLogs();
        this.refreshStatus();
        this.logsInterval = setInterval(() => this.refreshLogs(), 2000);
        this.statusInterval = setInterval(() => this.refreshStatus(), 2000);
    },

    async refreshLogs() {
        try {
            const response = await fetch('/api/logs');
            const data = await response.json();
            const logsPre = document.getElementById('logs');
            if (!logsPre) return;

            const wasAtBottom = logsPre.scrollHeight - logsPre.clientHeight <= logsPre.scrollTop + 1;
            logsPre.textContent = data.logs;
            if (wasAtBottom) {
                logsPre.scrollTop = logsPre.scrollHeight;
            }
        } catch (error) {
            console.error('Error fetching logs:', error);
        }
    },

    async refreshStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();

            // Update status indicator
            const statusIndicator = document.getElementById('status-indicator');
            if (statusIndicator) {
                if (data.is_running) {
                    statusIndicator.className = 'amb-status amb-status-running';
                    statusIndicator.innerHTML = `<span class="amb-status-dot"></span> ${i18n('ui.dashboard.status.running', 'Running')}`;
                } else {
                    statusIndicator.className = 'amb-status amb-status-idle';
                    statusIndicator.innerHTML = `<span class="amb-status-dot"></span> ${i18n('ui.dashboard.status.idle', 'Idle')}`;
                }
            }

            // Update MVP badge
            const mvpBadge = document.getElementById('mvp-badge');
            if (mvpBadge) {
                if (data.mvp_reached) {
                    mvpBadge.className = 'badge bg-primary';
                    mvpBadge.innerHTML = `<i class="bi bi-check-circle-fill"></i> ${i18n('ui.dashboard.status.mvp_reached', 'Reached')}`;
                } else {
                    mvpBadge.className = 'badge bg-secondary';
                    mvpBadge.innerHTML = `<i class="bi bi-hourglass-split"></i> ${i18n('ui.dashboard.status.mvp_progress', 'In Progress')}`;
                }
            }

            // Update run button
            const runBtn = document.getElementById('run-btn');
            if (runBtn) {
                runBtn.disabled = data.is_running;
            }

            // Update progress bar visibility
            const progressBar = document.getElementById('status-progress');
            if (progressBar) {
                progressBar.style.display = data.is_running ? 'block' : 'none';
            }
        } catch (error) {
            console.error('Error fetching status:', error);
        }
    }
};

/* ==========================================================================
   Toast Notifications
   ========================================================================== */
const Toast = {
    show(message, type = 'info') {
        const container = document.getElementById('toast-container') || this.createContainer();
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-bg-${type} border-0 show`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        container.appendChild(toast);

        // Auto remove after 5 seconds
        setTimeout(() => {
            toast.remove();
        }, 5000);

        // Close button
        toast.querySelector('.btn-close').addEventListener('click', () => toast.remove());
    },

    createContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '1100';
        document.body.appendChild(container);
        return container;
    }
};

/* ==========================================================================
   App Initialization
   ========================================================================== */
const App = {
    init() {
        ThemeManager.init();
        NavigationManager.init();
        ChoicesManager.init();
        WorkflowToggle.init();
        FormValidator.init();
        StatusPoller.init();
    }
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => App.init());

// Export for use in other scripts
window.App = App;
window.ThemeManager = ThemeManager;
window.NavigationManager = NavigationManager;
window.ChoicesManager = ChoicesManager;
window.WorkflowToggle = WorkflowToggle;
window.FormValidator = FormValidator;
window.StatusPoller = StatusPoller;
window.Toast = Toast;
