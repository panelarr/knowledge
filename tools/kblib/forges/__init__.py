"""Forge adapters. `for_repo(cfg, repo)` picks the adapter and its transport.

CLI first. The forge's official CLI handles login, tokens and SSO for you, so kb.py uses it
whenever it can. If the CLI is missing, kb.py stops and tells you how to install it. The raw
HTTPS + token fallback is used only when you opt in with `"transport": "http"` for that forge
in kb.config.json.

| forge          | default (transport: cli)              | opt-in (transport: http)                      |
|----------------|---------------------------------------|-----------------------------------------------|
| github         | `gh api` (gh auth login)              | $GITHUB_TOKEN -> api.github.com / <host>/api/v3 |
| gitlab         | `glab api` (glab auth login)          | $GITLAB_TOKEN -> <host>/api/v4 (PRIVATE-TOKEN)  |
| gitea/forgejo  | token from `tea login add`            | $GITEA_TOKEN  -> <host>/api/v1                  |
| bitbucket      | no official CLI: opt in to http       | $BITBUCKET_TOKEN -> api.bitbucket.org/2.0       |

Adding a forge: subclass `base.Forge`, implement the operations you can, register it below.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

from .base import CliTransport, Forge, ForgeError, HttpTransport, Unsupported
from .bitbucket import Bitbucket
from .gitea import Gitea
from .github import GitHub
from .gitlab import GitLab

ADAPTERS = {"github": GitHub, "gitlab": GitLab, "gitea": Gitea, "forgejo": Gitea, "codeberg": Gitea, "bitbucket": Bitbucket}

INSTALL = {
    "github": (
        "Install the GitHub CLI, then log in:\n"
        "    macOS: brew install gh   ·   Windows: winget install GitHub.cli   ·   Linux: https://github.com/cli/cli#installation\n"
        "    gh auth login{host_flag}"
    ),
    "gitlab": (
        "Install the GitLab CLI, then log in:\n"
        "    macOS: brew install glab   ·   Windows: winget install glab.glab   ·   Linux: https://gitlab.com/gitlab-org/cli#installation\n"
        "    glab auth login{host_flag}"
    ),
    "gitea": (
        "Install the Gitea/Forgejo CLI `tea`, then log in to your server:\n"
        "    macOS: brew install tea   ·   any OS: go install code.gitea.io/tea@latest   ·   binaries: https://gitea.com/gitea/tea/releases\n"
        "    tea login add --url https://{host} --token <personal access token>"
    ),
    "bitbucket": (
        "Bitbucket has no official CLI. To use it, opt in to the HTTPS fallback:\n"
        "    set \"transport\": \"http\" under forges.bitbucket in kb.config.json and export BITBUCKET_TOKEN\n"
        "    (a repository or workspace access token with pull request + issue scopes)"
    ),
}

HTTP_OPT_IN = ("\n  Last resort: set \"transport\": \"http\" under forges.{kind} in kb.config.json and export ${token_env}.\n"
               "  The CLI is recommended: it keeps tokens out of your shell environment and handles SSO and refresh.")

__all__ = ["for_repo", "ForgeError", "ForgeSetupError", "Unsupported", "Forge", "ADAPTERS"]


class ForgeSetupError(ForgeError):
    """The forge cannot be reached as configured; the message says how to fix it."""


class MissingTransport:
    """Placeholder transport that explains what to install instead of failing obscurely."""

    def __init__(self, message: str):
        self.message = message

    def available(self) -> tuple[bool, str]:
        return False, self.message

    def api(self, *a, **k):
        raise ForgeSetupError(self.message)


def _tea_token(host: str) -> str | None:
    """Read the token `tea login add` stored for `host` (tea's config.yml)."""
    candidates = [
        Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "tea" / "config.yml",
        Path.home() / "Library" / "Application Support" / "tea" / "config.yml",
        Path(os.environ.get("APPDATA", Path.home())) / "tea" / "config.yml",
    ]
    for path in candidates:
        if not path.exists():
            continue
        url, token = "", ""
        for raw in path.read_text(encoding="utf-8").splitlines() + ["- end"]:
            line = raw.strip()
            if line.startswith("- "):
                if url and token and host in url:
                    return token
                url, token = "", ""
                line = line[2:]
            if line.startswith("url:"):
                url = line[4:].strip().strip("'\"")
            elif line.startswith("token:"):
                token = line[6:].strip().strip("'\"")
    return None


def _host_flag(kind: str, host: str) -> str:
    default = {"github": "github.com", "gitlab": "gitlab.com"}.get(kind)
    return f" --hostname {host}" if host and host != default else ""


def _setup_message(kind: str, host: str, token_env: str, reason: str) -> str:
    base = "gitea" if kind in ("forgejo", "codeberg") else kind
    msg = f"{reason}\n  " + INSTALL[base].format(host=host or "codeberg.org", host_flag=_host_flag(base, host)).replace("\n", "\n  ")
    if base != "bitbucket":
        msg += HTTP_OPT_IN.format(kind=base, token_env=token_env)
    return msg


def _transport(kind: str, settings: dict):
    host = settings.get("host", "")
    cli = settings.get("cli")
    token_env = settings.get("token_env", "")
    # KB_FORGE_TRANSPORT=http is an explicit opt-in for CI runners where no CLI is logged in.
    mode = os.environ.get("KB_FORGE_TRANSPORT") or settings.get("transport", "cli")
    base = "gitea" if kind in ("forgejo", "codeberg") else kind

    if mode == "http":
        if base == "github":
            url = "https://api.github.com" if host in ("", "github.com") else f"https://{host}/api/v3"
            return HttpTransport(url, token_env or "GITHUB_TOKEN")
        if base == "gitlab":
            return HttpTransport(f"https://{host or 'gitlab.com'}/api/v4", token_env or "GITLAB_TOKEN",
                                 auth_scheme="", token_header="PRIVATE-TOKEN")
        if base == "gitea":
            return HttpTransport(f"https://{host or 'codeberg.org'}/api/v1", token_env or "GITEA_TOKEN", auth_scheme="token")
        if base == "bitbucket":
            return HttpTransport("https://api.bitbucket.org/2.0", token_env or "BITBUCKET_TOKEN")
        raise ForgeError(f"unknown forge '{kind}'")

    if base in ("github", "gitlab"):
        cli = cli or ("gh" if base == "github" else "glab")
        if shutil.which(cli):
            default = "github.com" if base == "github" else "gitlab.com"
            return CliTransport(cli, None if host in ("", default) else host)
        return MissingTransport(_setup_message(kind, host, token_env, f"`{cli}` is not installed."))
    if base == "gitea":
        if not shutil.which("tea"):
            return MissingTransport(_setup_message(kind, host, token_env or "GITEA_TOKEN", "`tea` is not installed."))
        token = _tea_token(host or "codeberg.org")
        if not token:
            return MissingTransport(_setup_message(kind, host, token_env or "GITEA_TOKEN",
                                                   f"`tea` has no login for {host or 'codeberg.org'}."))
        t = HttpTransport(f"https://{host or 'codeberg.org'}/api/v1", "", auth_scheme="token")
        t.static_token = token
        return t
    if base == "bitbucket":
        return MissingTransport(_setup_message(kind, host, token_env, "Bitbucket is not set up."))
    raise ForgeError(f"unknown forge '{kind}'")


def for_repo(cfg, repo: dict, transport=None) -> Forge:
    kind = repo.get("forge") or cfg.get("forge", "github")
    if kind not in ADAPTERS:
        raise ForgeError(f"unknown forge '{kind}' for repo '{repo.get('name')}' (known: {', '.join(ADAPTERS)})")
    base = "gitea" if kind in ("forgejo", "codeberg") else kind
    settings = dict(cfg.forges.get(kind) or cfg.forges.get(base) or {})
    if repo.get("host"):
        settings["host"] = repo["host"]
    repo = dict(repo, host=settings.get("host", ""))
    return ADAPTERS[kind](transport or _transport(kind, settings), repo)
