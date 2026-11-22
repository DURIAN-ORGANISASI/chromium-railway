# Security Policy

## Login credentials

- `CUSTOM_USER` and `PASSWORD` protect the Chromium web desktop.
- Use a unique password of at least 12 characters; 16+ characters is recommended.
- Store credentials only in Railway service Variables or an untracked local `.env` file.
- Never commit credentials, cookies, browser profiles, downloads, or session data.
- Rotate `PASSWORD` immediately if it is exposed, then redeploy the service.

## Public access

Railway generated domains use HTTPS. Keep the browser behind the login prompt and do not share its URL or credentials. The image's built-in HTTP Basic Authentication is a basic access gate, not an identity provider, multi-user system, or SSO. LinuxServer's own documentation recommends placing the interface behind a stronger reverse-proxy/access layer for internet exposure. For organization-wide access, use a trusted gateway such as Cloudflare Access in front of the domain.

## Browser privileges and profile data

A user who can sign in can control the browser, open websites, access websites signed in to the profile, and interact with files exposed through the desktop. Keep `HARDEN_DESKTOP=true` to disable terminal and sudo access in the desktop session. Avoid untrusted downloads and websites.

The `/config` directory contains sensitive data including browser cookies, saved passwords, history, extensions, settings, and downloads. In the no-Volume deployment, these files live on the container's temporary writable filesystem and are lost when Railway recreates the container. Limit access to the Railway project and do not treat the container filesystem as a backup.

## Deployment recommendations

- Use one replica for one browser session.
- Do not attach a Railway Volume; the browser profile is intentionally temporary in the container filesystem.
- Do not expose additional ports unless required.
- Keep the image tag pinned and review updates before changing it.
- Monitor Railway resource usage; Chromium desktop sessions consume RAM and CPU.

## Reporting

Report vulnerabilities privately to the repository owner. Include the affected deployment version and reproduction steps, but never include live passwords, cookies, session identifiers, or personal data.


## Runtime safeguards

- Nginx Basic Authentication is enabled in the image at build time; it is not optional at runtime.
- The startup wrapper writes a SHA-512 crypt password hash to `/etc/nginx/.htpasswd` and removes the plaintext password from the environment before starting desktop services.
- An Nginx Origin check protects the browser WebSocket from cross-site websites attempting to reuse a cached login.
- `/healthz` is the only unauthenticated HTTP route and returns the internal Selkies health state for Railway probes. It does not expose the browser UI.
- The s6 service tree is started by the Railway-specific wrapper rather than the upstream `/init` PID-1 entry point.
