#!/usr/bin/env python3
"""Offline checks for the Chromium Desktop Railway repository."""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "README.en.md", "Dockerfile", "docker-compose.yml",
    ".env.example", "LICENSE", "NOTICE.md", "SECURITY.md", "CONTRIBUTING.md",
    "LICENSES/GPL-3.0-or-later.txt",
    "services/browser/railway-start.sh",
    "services/browser/patch-image.sh",
    "services/browser/pkg-restore.sh",
    "services/browser/nginx-origin-map.conf",
    "services/browser/nginx-server-hardening.conf",
    "docs/brand.svg", "docs/hero.id.svg", "docs/architecture.svg",
    "docs/DEPLOY-RAILWAY.md", "docs/SOURCES.md",
]
errors: list[str] = []

for relative in REQUIRED:
    if not (ROOT / relative).is_file():
        errors.append(f"Missing required file: {relative}")

if (ROOT / "Dockerfile").exists():
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    if "FROM lscr.io/linuxserver/chromium:7b8e918f-ls63@sha256:" not in dockerfile:
        errors.append("Dockerfile must use the pinned LinuxServer Chromium image.")
    if "ENTRYPOINT [\"/usr/bin/catatonit\", \"--\", \"/usr/local/bin/railway-start\"]" not in dockerfile:
        errors.append("Dockerfile must use the Railway-compatible startup wrapper.")
    if "EXPOSE 3000" not in dockerfile:
        errors.append("Dockerfile must expose port 3000.")
    if "PASSWORD=" in dockerfile:
        errors.append("Do not bake credentials into the Dockerfile.")

for relative in ["docs/brand.svg", "docs/hero.id.svg", "docs/architecture.svg"]:
    path = ROOT / relative
    if path.exists():
        try:
            ET.parse(path)
        except ET.ParseError as exc:
            errors.append(f"Invalid SVG/XML in {relative}: {exc}")

for relative in ["README.md", "README.en.md"]:
    path = ROOT / relative
    if path.exists():
        content = path.read_text(encoding="utf-8")
        for required_text in ["CUSTOM_USER", "PASSWORD", "/config", "docs/architecture.svg", "SECURITY.md", "LICENSES/GPL-3.0-or-later.txt"]:
            if required_text not in content:
                errors.append(f"{relative} is missing reference: {required_text}")
        for forbidden in ["BROWSER_WS_ENDPOINT", "Browserless", "Hermes Agent", "ghcr.io/two-workspaces/chromium:246dc28"]:
            if forbidden in content:
                errors.append(f"{relative} still contains obsolete content: {forbidden}")

if (ROOT / ".env.example").exists():
    env = (ROOT / ".env.example").read_text(encoding="utf-8")
    for key in ["CUSTOM_USER=", "PASSWORD=", "PORT=3000"]:
        if key not in env:
            errors.append(f".env.example is missing {key}")
    if "CHANGE_THIS_TO_A_UNIQUE_PASSWORD" not in env:
        errors.append(".env.example must contain a placeholder password, not a real password.")

if errors:
    print("Repository validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Repository validation passed.")
