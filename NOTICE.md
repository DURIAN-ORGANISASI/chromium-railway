# NOTICE — Chromium Railway

This repository combines original project documentation and deployment metadata with GPL-licensed Railway compatibility code and the upstream LinuxServer Chromium image.

## Railway compatibility code

The files under `services/browser/` are based on and adapted from the Chromium Railway implementation published at:

- Source repository: https://github.com/baranberkay96/chromium-browser-railway
- Upstream files: `services/browser/Dockerfile`, `railway-start.sh`, `patch-image.sh`, `nginx-origin-map.conf`, `nginx-server-hardening.conf`, and `pkg-restore.sh`
- License: GNU General Public License v3.0 or later; see [LICENSES/GPL-3.0-or-later.txt](LICENSES/GPL-3.0-or-later.txt)

Changes for this repository: Dockerfile paths are rooted at this repository's top-level directory; the startup and Nginx compatibility logic is integrated with the existing Chromium README and Railway service configuration. The startup wrapper avoids invoking the upstream s6-overlay `/init` as PID 1 because Railway provides its own init process.

## Container image and upstream projects

- Base image: `lscr.io/linuxserver/chromium:7b8e918f-ls63@sha256:ff1b8235e20367c3b660d31892e14428687df75e2d62e274b7d8d40cf5537108`
- LinuxServer Chromium: https://github.com/linuxserver/docker-chromium
- LinuxServer Selkies base image: https://github.com/linuxserver/docker-baseimage-selkies
- Selkies: https://github.com/selkies-project/selkies
- Chromium: https://www.chromium.org/

The LinuxServer image contains Chromium, Selkies, s6-overlay, catatonit, nginx, and operating-system packages. Each upstream component retains its own copyright notices and license. The pinned image digest and source references are provided for reproducibility; consult upstream repositories for corresponding source and package notices.

## License boundaries

- Original repository documentation, SVG artwork, and non-derived supporting material: MIT License, see [LICENSE](LICENSE).
- Railway compatibility scripts and Dockerfile under `services/browser/`, plus the Dockerfile integration: GPL-3.0-or-later, see [LICENSES/GPL-3.0-or-later.txt](LICENSES/GPL-3.0-or-later.txt).
- LinuxServer Chromium image and bundled components: their respective upstream licenses.

This project is independent and is not affiliated with or endorsed by Google, Chromium, LinuxServer.io, Selkies, or Railway.
