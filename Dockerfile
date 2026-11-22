# SPDX-License-Identifier: GPL-3.0-or-later
# Chromium Desktop streamed through LinuxServer Selkies, adapted for Railway.
# Railway provides its own PID 1, so railway-start supervises the upstream s6
# service tree without calling the upstream /init wrapper.
FROM lscr.io/linuxserver/chromium:7b8e918f-ls63@sha256:ff1b8235e20367c3b660d31892e14428687df75e2d62e274b7d8d40cf5537108

ENV PUID=1000 \
    PGID=1000 \
    START_DOCKER=false \
    SELKIES_ALLOWED_ORIGINS="" \
    SELKIES_ENABLE_BASIC_AUTH=false \
    TITLE="Chromium" \
    CUSTOM_USER=chromium \
    PORT=3000 \
    TZ=Asia/Jakarta \
    HARDEN_DESKTOP=true \
    SELKIES_FILE_TRANSFERS=upload,download \
    SELKIES_UI_SIDEBAR_SHOW_FILES=true

COPY services/browser/patch-image.sh /tmp/railway-desktop/patch-image.sh
COPY services/browser/nginx-origin-map.conf services/browser/nginx-server-hardening.conf /tmp/railway-desktop/
COPY services/browser/railway-start.sh /usr/local/bin/railway-start
COPY services/browser/pkg-restore.sh /usr/local/bin/railway-pkg-restore

RUN bash /tmp/railway-desktop/patch-image.sh \
 && rm -rf /tmp/railway-desktop \
 && chmod 0755 /usr/local/bin/railway-start /usr/local/bin/railway-pkg-restore

EXPOSE 3000

ENTRYPOINT ["/usr/bin/catatonit", "--", "/usr/local/bin/railway-start"]
