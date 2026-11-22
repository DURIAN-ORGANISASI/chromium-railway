# Sources, Attribution, and Licensing

## Runtime and browser

- [LinuxServer Chromium documentation](https://docs.linuxserver.io/images/docker-chromium/)
- [LinuxServer Docker Chromium source](https://github.com/linuxserver/docker-chromium)
- [LinuxServer Selkies base image](https://github.com/linuxserver/docker-baseimage-selkies)
- [Selkies web desktop](https://github.com/selkies-project/selkies)
- [Chromium project](https://www.chromium.org/)

The Dockerfile pins `lscr.io/linuxserver/chromium:7b8e918f-ls63` by manifest digest. Review upstream tags and security updates before changing that pin.

## Railway compatibility code attribution

The Railway startup workaround, Nginx hardening patch, and package-restore helper in `services/browser/` are based on the public implementation at:

- https://github.com/baranberkay96/chromium-browser-railway

Those files are distributed under GPL-3.0-or-later. The full license is provided in [`LICENSES/GPL-3.0-or-later.txt`](../LICENSES/GPL-3.0-or-later.txt), and file-level attribution/changes are documented in [`NOTICE.md`](../NOTICE.md).

## Railway documentation

- [Railway Dockerfiles](https://docs.railway.com/builds/dockerfiles)
- [Railway Networking](https://docs.railway.com/networking)
- [Railway Volumes](https://docs.railway.com/volumes)
- [Railway Variables](https://docs.railway.com/variables)

## Licensing boundary

Original project documentation, SVG artwork, and supporting material remain under the MIT License in [`LICENSE`](../LICENSE). The adapted Railway compatibility code and integrated Dockerfile are GPL-3.0-or-later. The base image and all bundled programs remain under their respective upstream licenses.

This repository is an independent community deployment and is not affiliated with or endorsed by Google, Chromium, LinuxServer.io, Selkies, or Railway.
