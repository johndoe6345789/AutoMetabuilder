/**
 * AutoMetabuilder - Navigation Manager
 */
(() => {
    const NavigationManager = {
        _popstateBound: false,

        init() {
            this.bindLinks();
            this.activateFromHash(false);
            if (!this._popstateBound) {
                window.addEventListener('popstate', () => {
                    this.activateFromHash(false);
                });
                this._popstateBound = true;
            }
        },

        bindLinks() {
            document.querySelectorAll('[data-section]').forEach(link => {
                if (link.dataset.navBound === 'true') return;
                link.dataset.navBound = 'true';
                link.addEventListener('click', event => {
                    event.preventDefault();
                    this.showSection(link.dataset.section);
                });
            });
        },

        refresh() {
            this.bindLinks();
            if (!this.activateFromHash(false)) {
                const firstLink = document.querySelector('[data-section]');
                if (firstLink) {
                    this.showSection(firstLink.dataset.section, false);
                }
            }
        },

        activateFromHash(updateHistory) {
            const hash = window.location.hash.slice(1);
            if (!hash || !document.querySelector(`#${hash}`)) return false;
            this.showSection(hash, updateHistory);
            return true;
        },

        showSection(sectionId, updateHistory = true) {
            document.querySelectorAll('.amb-section').forEach(section => {
                section.classList.remove('active');
            });

            const targetSection = document.querySelector(`#${sectionId}`);
            if (targetSection) {
                targetSection.classList.add('active');
            }

            document.querySelectorAll('.amb-nav-link').forEach(link => {
                link.classList.remove('active');
            });
            const activeLink = document.querySelector(`[data-section="${sectionId}"]`);
            if (activeLink) {
                activeLink.classList.add('active');
            }

            if (updateHistory) {
                history.pushState(null, '', `#${sectionId}`);
            }
        }
    };

    window.NavigationManager = NavigationManager;
    window.AMBPlugins?.register('navigation_manager', async () => NavigationManager.init());
})();
