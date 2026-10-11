"""Forge adapter interface and transports.

A transport sends `api(method, path, body)` to a forge. Two kinds:
  * CliTransport: the forge's own CLI (`gh api`, `glab api`), which handles auth for you.
  * HttpTransport: plain HTTPS with a token from an environment variable (stdlib urllib).

Adapters map normalized operations (list issues, get PR, post comment, ...) onto a forge's REST API.
Every adapter returns plain dicts so the rest of the tool never sees forge-specific shapes.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
from typing import Any


class ForgeError(Exception):
    pass


class Unsupported(ForgeError):
    pass


class CliTransport:
    """`gh api` / `glab api` style CLIs: `<cli> api [-X METHOD] [--hostname H] PATH [--input FILE]`."""

    def __init__(self, cli: str, host: str | None = None, host_flag: str = "--hostname"):
        self.cli = cli
        self.host = host
        self.host_flag = host_flag

    def available(self) -> tuple[bool, str]:
        if not shutil.which(self.cli):
            return False, f"`{self.cli}` not installed"
        return True, f"via `{self.cli}`"

    def api(self, method: str, path: str, body: dict | None = None, raw: bool = False,
            accept: str | None = None) -> Any:
        cmd = [self.cli, "api", "-X", method, path.lstrip("/")]
        if self.host:
            cmd += [self.host_flag, self.host]
        if accept:
            cmd += ["-H", f"Accept: {accept}"]
        tmp = None
        try:
            if body is not None:
                tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
                json.dump(body, tmp)
                tmp.close()
                cmd += ["--input", tmp.name]
            res = subprocess.run(cmd, capture_output=True, text=True)
        finally:
            if tmp:
                os.unlink(tmp.name)
        if res.returncode != 0:
            raise ForgeError(f"{self.cli} api {method} {path}: {res.stderr.strip() or res.stdout.strip()}")
        if raw:
            return res.stdout
        return json.loads(res.stdout) if res.stdout.strip() else None


class HttpTransport:
    def __init__(self, base_url: str, token_env: str, auth_scheme: str = "Bearer", token_header: str = "Authorization"):
        self.base_url = base_url.rstrip("/")
        self.token_env = token_env
        self.auth_scheme = auth_scheme
        self.token_header = token_header
        self.static_token = ""  # set when a CLI login (e.g. `tea login`) supplies the token

    def _token(self) -> str:
        return self.static_token or os.environ.get(self.token_env, "")

    def available(self) -> tuple[bool, str]:
        if self.static_token:
            return True, f"via HTTPS ({self.base_url}) with the CLI's stored login"
        if not os.environ.get(self.token_env):
            return False, f"HTTPS fallback enabled but ${self.token_env} is not set"
        return True, f"via HTTPS fallback ({self.base_url}, ${self.token_env})"

    def api(self, method: str, path: str, body: dict | None = None, raw: bool = False,
            accept: str | None = None) -> Any:
        token = self._token()
        url = path if path.startswith("http") else f"{self.base_url}/{path.lstrip('/')}"
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        if token:
            value = f"{self.auth_scheme} {token}".strip() if self.auth_scheme else token
            req.add_header(self.token_header, value)
        req.add_header("Accept", accept or "application/json")
        req.add_header("User-Agent", "kb-ops")
        if data is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                text = resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            raise ForgeError(f"{method} {url}: HTTP {e.code} {e.read().decode('utf-8', 'replace')[:300]}") from e
        except urllib.error.URLError as e:
            raise ForgeError(f"{method} {url}: {e.reason}") from e
        if raw:
            return text
        return json.loads(text) if text.strip() else None


class Forge:
    """Normalized operations. Items are dicts with at least:
    number, title, url, author, state, updated, labels (list), kind ('issue' | 'pr').
    PRs add: draft, head, base, checks ('success' | 'failure' | 'pending' | 'none'), review (str).
    """

    name = "forge"

    def __init__(self, transport, repo: dict):
        self.t = transport
        self.repo = repo
        self.slug = repo.get("slug", "")

    def available(self) -> tuple[bool, str]:
        return self.t.available()

    # reads
    def list_issues(self, since: str | None, limit: int) -> list[dict]:
        raise Unsupported(f"{self.name}: list_issues")

    def list_prs(self, since: str | None, limit: int) -> list[dict]:
        raise Unsupported(f"{self.name}: list_prs")

    def get_issue(self, number: int) -> dict:
        raise Unsupported(f"{self.name}: get_issue")

    def get_pr(self, number: int) -> dict:
        raise Unsupported(f"{self.name}: get_pr")

    def get_diff(self, number: int) -> str:
        raise Unsupported(f"{self.name}: get_diff")

    # writes
    def comment(self, number: int, body: str, is_pr: bool) -> str:
        raise Unsupported(f"{self.name}: comment")

    def review(self, number: int, body: str, event: str) -> str:
        raise Unsupported(f"{self.name}: review")

    def label(self, number: int, labels: list[str], is_pr: bool) -> str:
        raise Unsupported(f"{self.name}: label")

    def assign(self, number: int, users: list[str], is_pr: bool) -> str:
        raise Unsupported(f"{self.name}: assign")

    def open_issue(self, title: str, body: str, labels: list[str]) -> str:
        raise Unsupported(f"{self.name}: open_issue")

    def close(self, number: int, is_pr: bool) -> str:
        raise Unsupported(f"{self.name}: close")

    def merge(self, number: int) -> str:
        raise Unsupported(f"{self.name}: merge")


def login(user: Any) -> str:
    if isinstance(user, dict):
        return user.get("login") or user.get("username") or user.get("nickname") or user.get("display_name") or ""
    return str(user or "")
