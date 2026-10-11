"""Loading kb.config.json and locating the KB root."""
from __future__ import annotations

import json
from pathlib import Path

CONFIG_NAME = "kb.config.json"
DEFAULT_ROOT = Path(__file__).resolve().parent.parent.parent

LEVELS = ("never", "ask", "draft", "auto")


class ConfigError(Exception):
    pass


class Config:
    def __init__(self, root: Path, data: dict):
        self.root = root
        self.data = data

    # -- plain accessors -------------------------------------------------
    def get(self, key: str, default=None):
        return self.data.get(key, default)

    @property
    def initialized(self) -> bool:
        return bool(self.data.get("initialized", False))

    @property
    def project(self) -> dict:
        return self.data.get("project", {})

    @property
    def statuses(self) -> list[str]:
        return list(self.data.get("statuses", []))

    @property
    def required(self) -> list[str]:
        return list(self.data.get("frontmatter_required", ["title", "status", "updated"]))

    @property
    def ids(self) -> dict:
        return self.data.get("ids", {})

    @property
    def non_knowledge(self) -> tuple[str, ...]:
        return tuple(self.data.get("non_knowledge", []))

    @property
    def unindexed(self) -> tuple[str, ...]:
        return tuple(self.data.get("unindexed", []))

    @property
    def skip_dirs(self) -> set[str]:
        return set(self.data.get("skip_dirs", [".git"]))

    @property
    def commit(self) -> dict:
        return self.data.get("commit", {})

    @property
    def privacy(self) -> dict:
        return self.data.get("privacy", {})

    @property
    def repos(self) -> list[dict]:
        return list(self.data.get("repos", []))

    @property
    def forges(self) -> dict:
        return self.data.get("forges", {})

    @property
    def authority(self) -> dict:
        return self.data.get("authority", {})

    @property
    def ops(self) -> dict:
        return self.data.get("ops", {})

    def repo(self, name: str) -> dict:
        for r in self.repos:
            if r.get("name") == name or r.get("slug") == name:
                return r
        raise ConfigError(f"repo '{name}' is not registered in {CONFIG_NAME} (repos[])")

    def level(self, action: str) -> str:
        lvl = self.authority.get(action, "never")
        return lvl if lvl in LEVELS else "never"

    def save(self) -> None:
        path = self.root / CONFIG_NAME
        path.write_text(json.dumps(self.data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load(root: Path | str | None = None) -> Config:
    base = Path(root).resolve() if root else DEFAULT_ROOT
    path = base / CONFIG_NAME
    if not path.exists():
        raise ConfigError(f"no {CONFIG_NAME} in {base}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ConfigError(f"{path}: invalid JSON: {e}") from e
    return Config(base, data)
