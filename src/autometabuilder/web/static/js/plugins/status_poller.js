/**
 * AutoMetabuilder - Status Poller
 */
(() => {
    const t = (key, fallback = '') => window.AMBContext?.t?.(key, fallback) || fallback || key;
    const headers = () => window.AMBContext?.authHeaders || {};

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
                const response = await fetch('/api/logs', {
                    credentials: 'include',
                    headers: headers()
                });
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
                const response = await fetch('/api/status', {
                    credentials: 'include',
                    headers: headers()
                });
                const data = await response.json();

                const statusIndicator = document.getElementById('status-indicator');
                if (statusIndicator) {
                    if (data.is_running) {
                        statusIndicator.className = 'amb-status amb-status-running';
                        statusIndicator.innerHTML = `<span class="amb-status-dot"></span> ${t('ui.dashboard.status.running', 'Running')}`;
                    } else {
                        statusIndicator.className = 'amb-status amb-status-idle';
                        statusIndicator.innerHTML = `<span class="amb-status-dot"></span> ${t('ui.dashboard.status.idle', 'Idle')}`;
                    }
                }

                const mvpBadge = document.getElementById('mvp-badge');
                if (mvpBadge) {
                    if (data.mvp_reached) {
                        mvpBadge.className = 'badge bg-primary';
                        mvpBadge.innerHTML = `<i class="bi bi-check-circle-fill"></i> ${t('ui.dashboard.status.mvp_reached', 'Reached')}`;
                    } else {
                        mvpBadge.className = 'badge bg-secondary';
                        mvpBadge.innerHTML = `<i class="bi bi-hourglass-split"></i> ${t('ui.dashboard.status.mvp_progress', 'In Progress')}`;
                    }
                }

                const runBtn = document.getElementById('run-btn');
                if (runBtn) {
                    runBtn.disabled = data.is_running;
                }

                const progressBar = document.getElementById('status-progress');
                if (progressBar) {
                    progressBar.style.display = data.is_running ? 'block' : 'none';
                }
            } catch (error) {
                console.error('Error fetching status:', error);
            }
        }
    };

    window.StatusPoller = StatusPoller;
    window.AMBPlugins?.register('status_poller', async () => StatusPoller.init());
})();
