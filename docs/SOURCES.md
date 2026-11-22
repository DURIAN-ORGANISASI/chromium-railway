# Sources, Attribution, and Licensing

## Browser image and desktop stack

- [Chromium project](https://www.chromium.org/)
- [LinuxServer Chromium documentation](https://docs.linuxserver.io/images/docker-chromium/)
- [LinuxServer Docker Chromium source](https://github.com/linuxserver/docker-chromium)
- [LinuxServer Selkies base image](https://github.com/linuxserver/docker-baseimage-selkies)
- [Selkies web desktop](https://github.com/selkies-project/selkies)
- Community Railway image used by this repository: [`ghcr.io/two-workspaces/chromium:246dc28`](https://railway.com/deploy/chromium-your-browser-in-the-cloud--chromium)

## Railway documentation

- [Railway Dockerfiles](https://docs.railway.com/builds/dockerfiles)
- [Railway Networking](https://docs.railway.com/networking)
- [Railway Volumes](https://docs.railway.com/volumes)
- [Railway Variables](https://docs.railway.com/variables)

## Licensing boundary

The repository's original documentation, deployment files, and assets are distributed under the MIT License; see [`../LICENSE`](../LICENSE).

The Dockerfile uses the community-published image `ghcr.io/two-workspaces/chromium:246dc28`. This image is built on the LinuxServer Chromium/Selkies stack. Chromium, LinuxServer, Selkies, and bundled packages carry their own licenses and notices. The repository license does not relicense the upstream image or its dependencies. Review the publisher's and upstream projects' current terms before redistributing or offering the image to others.

Product names and trademarks belong to their respective owners.

## Independence

This is an independent deployment repository. It is not affiliated with or endorsed by Google, the Chromium project, LinuxServer.io, Selkies, Two Workspaces, or Railway.
