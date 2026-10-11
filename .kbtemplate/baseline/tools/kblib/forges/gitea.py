"""Gitea and Forgejo (including Codeberg). HTTPS with $GITEA_TOKEN (Authorization: token ...)."""
from __future__ import annotations

from urllib.parse import quote

from .base import Forge, login


class Gitea(Forge):
    name = "gitea"

    def _item(self, it: dict) -> dict:
        is_pr = bool(it.get("pull_request")) or "head" in it
        return {
            "number": it["number"],
            "title": it.get("title", ""),
            "url": it.get("html_url", ""),
            "author": login(it.get("user")),
            "state": it.get("state", ""),
            "updated": it.get("updated_at", ""),
            "labels": [l.get("name", "") for l in it.get("labels", []) or []],
            "comments": it.get("comments", 0),
            "kind": "pr" if is_pr else "issue",
            "draft": bool(it.get("draft")) or it.get("title", "").lower().startswith(("wip:", "draft:")),
        }

    def list_issues(self, since, limit):
        q = f"repos/{self.slug}/issues?state=open&type=issues&limit={limit}"
        if since:
            q += f"&since={quote(since)}"
        return [self._item(i) for i in self.t.api("GET", q)]

    def _checks(self, sha: str) -> str:
        if not sha:
            return "none"
        try:
            st = self.t.api("GET", f"repos/{self.slug}/commits/{sha}/status")
        except Exception:
            return "unknown"
        state = (st or {}).get("state", "")
        return {"success": "success", "failure": "failure", "error": "failure", "pending": "pending"}.get(state, "none")

    def list_prs(self, since, limit):
        out = []
        for p in self.t.api("GET", f"repos/{self.slug}/pulls?state=open&sort=recentupdate&limit={limit}"):
            if since and p.get("updated_at", "") < since:
                continue
            item = self._item(p)
            item.update({
                "head": p.get("head", {}).get("ref", ""),
                "base": p.get("base", {}).get("ref", ""),
                "checks": self._checks(p.get("head", {}).get("sha", "")),
                "review": ", ".join(login(r) for r in p.get("requested_reviewers", []) or []) and
                          "requested: " + ", ".join(login(r) for r in p.get("requested_reviewers", []) or []),
            })
            out.append(item)
        return out

    def _thread(self, number: int) -> list[dict]:
        return [{"author": login(c.get("user")), "created": c.get("created_at", ""), "body": c.get("body", "")}
                for c in self.t.api("GET", f"repos/{self.slug}/issues/{number}/comments")]

    def get_issue(self, number):
        it = self.t.api("GET", f"repos/{self.slug}/issues/{number}")
        item = self._item(it)
        item["body"] = it.get("body") or ""
        item["thread"] = self._thread(number)
        return item

    def get_pr(self, number):
        p = self.t.api("GET", f"repos/{self.slug}/pulls/{number}")
        item = self._item(p)
        try:
            files = self.t.api("GET", f"repos/{self.slug}/pulls/{number}/files")
        except Exception:
            files = []
        try:
            commits = self.t.api("GET", f"repos/{self.slug}/pulls/{number}/commits")
        except Exception:
            commits = []
        item.update({
            "body": p.get("body") or "",
            "head": p.get("head", {}).get("ref", ""),
            "base": p.get("base", {}).get("ref", ""),
            "checks": self._checks(p.get("head", {}).get("sha", "")),
            "mergeable": "mergeable" if p.get("mergeable") else "not mergeable",
            "files": [{"path": f.get("filename", ""), "additions": f.get("additions", 0),
                       "deletions": f.get("deletions", 0), "status": f.get("status", "")} for f in files],
            "commits": [{"sha": c.get("sha", "")[:7], "message": c.get("commit", {}).get("message", "").splitlines()[0] if c.get("commit") else ""}
                        for c in commits],
            "thread": self._thread(number),
            "reviews": [{"author": login(r.get("user")), "state": r.get("state", ""), "body": r.get("body", "")}
                        for r in self.t.api("GET", f"repos/{self.slug}/pulls/{number}/reviews")],
        })
        return item

    def get_diff(self, number):
        return self.t.api("GET", f"repos/{self.slug}/pulls/{number}.diff", raw=True, accept="text/plain")

    def comment(self, number, body, is_pr):
        return self.t.api("POST", f"repos/{self.slug}/issues/{number}/comments", {"body": body}).get("html_url", "")

    def review(self, number, body, event):
        ev = {"approve": "APPROVED", "request_changes": "REQUEST_CHANGES"}.get(event, "COMMENT")
        r = self.t.api("POST", f"repos/{self.slug}/pulls/{number}/reviews", {"body": body, "event": ev})
        return (r or {}).get("html_url", "")

    def label(self, number, labels, is_pr):
        # Recent Gitea/Forgejo accept label names here; older versions need numeric IDs.
        self.t.api("POST", f"repos/{self.slug}/issues/{number}/labels", {"labels": labels})
        return f"https://{self.repo.get('host', 'codeberg.org')}/{self.slug}/issues/{number}"

    def assign(self, number, users, is_pr):
        r = self.t.api("PATCH", f"repos/{self.slug}/issues/{number}", {"assignees": users})
        return r.get("html_url", "")

    def open_issue(self, title, body, labels):
        return self.t.api("POST", f"repos/{self.slug}/issues", {"title": title, "body": body}).get("html_url", "")

    def close(self, number, is_pr):
        return self.t.api("PATCH", f"repos/{self.slug}/issues/{number}", {"state": "closed"}).get("html_url", "")

    def merge(self, number):
        self.t.api("POST", f"repos/{self.slug}/pulls/{number}/merge", {"Do": "squash"})
        return f"https://{self.repo.get('host', 'codeberg.org')}/{self.slug}/pulls/{number}"
