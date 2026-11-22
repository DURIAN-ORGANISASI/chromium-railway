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

The `/config` Volume contains sensitive data including browser cookies, saved passwords, history, extensions, settings, and downloads. Limit access to the Railway project and its Volumes.

## Deployment recommendations

- Use one replica for a single persistent browser profile.
- Attach a Railway Volume at `/config`.
- Do not expose additional ports unless required.
- Keep the image tag pinned and review updates before changing it.
- Monitor Railway resource usage; Chromium desktop sessions consume RAM and CPU.

## Reporting

Report vulnerabilities privately to the repository owner. Include the affected deployment version and reproduction steps, but never include live passwords, cookies, session identifiers, or personal data.
