# Chromium desktop streamed to the browser through the LinuxServer Selkies UI.
# This Railway-ready community image includes the init and web-login handling
# needed for a single-service Chromium desktop deployment.
FROM ghcr.io/two-workspaces/chromium:246dc28

ENV PORT=3000 \
    PUID=1000 \
    PGID=1000 \
    TZ=Asia/Jakarta \
    HARDEN_DESKTOP=true \
    CHROME_CLI=--disable-dev-shm-usage \
    SELKIES_FILE_TRANSFERS=true \
    SELKIES_UI_SIDEBAR_SHOW_FILES=true

EXPOSE 3000
