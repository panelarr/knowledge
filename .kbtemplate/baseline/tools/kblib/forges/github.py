"""GitHub (github.com and GitHub Enterprise). Uses `gh api` when installed, else $GITHUB_TOKEN over HTTPS."""
from __future__ import annotations

from urllib.parse import quote

from .base import Forge, login


class GitHub(Forge):
    name = "github"

    def _item(self, it: dict) -> dict:
        is_pr = "pull_request" in it or "head" in it
        return {
            "number": it["number"],
            "title": it.get("title", ""),
            "url": it.get("html_url", ""),
            "author": login(it.get("user")),
            "state": it.get("state", ""),
            "updated": it.get("updated_at", ""),
            "labels": [l.get("name", "") for l in it.get("labels", [])],
            "comments": it.get("comments", 0),
            "kind": "pr" if is_pr else "issue",
            "draft": bool(it.get("draft")),
        }

    def list_issues(self, since, limit):
        q = f"repos/{self.slug}/issues?state=open&sort=updated&per_page={limit}"
        if since:
            q += f"&since={quote(since)}"
        return [self._item(i) for i in self.t.api("GET", q) if "pull_request" not in i]

    def _checks(self, sha: str) -> str:
        try:
            runs = self.t.api("GET", f"repos/{self.slug}/commits/{sha}/check-runs?per_page=100").get("check_runs", [])
        except Exception:
            return "unknown"
        if not runs:
            return "none"
        concl = {r.get("conclusion") for r in runs}
        if any(r.get("status") != "completed" for r in runs):
            return "pending"
        if concl & {"failure", "timed_out", "cancelled", "action_required"}:
            return "failure"
        return "success"

    def list_prs(self, since, limit):
        prs = self.t.api("GET", f"repos/{self.slug}/pulls?state=open&sort=updated&direction=desc&per_page={limit}")
        out = []
        for p in prs:
            if since and p.get("updated_at", "") < since:
                continue
            item = self._item(p)
            item.update({
                "head": p.get("head", {}).get("ref", ""),
                "base": p.get("base", {}).get("ref", ""),
                "checks": self._checks(p.get("head", {}).get("sha", "")),
                "review": ", ".join(login(r) for r in p.get("requested_reviewers", [])) and
                          "requested: " + ", ".join(login(r) for r in p.get("requested_reviewers", [])),
            })
            out.append(item)
        return out

    def get_issue(self, number):
        it = self.t.api("GET", f"repos/{self.slug}/issues/{number}")
        item = self._item(it)
        item["body"] = it.get("body") or ""
        item["thread"] = [
            {"author": login(c.get("user")), "created": c.get("created_at", ""), "body": c.get("body", "")}
            for c in self.t.api("GET", f"repos/{self.slug}/issues/{number}/comments?per_page=100")
        ]
        return item

    def get_pr(self, number):
        p = self.t.api("GET", f"repos/{self.slug}/pulls/{number}")
        item = self._item(p)
        item.update({
            "body": p.get("body") or "",
            "head": p.get("head", {}).get("ref", ""),
            "base": p.get("base", {}).get("ref", ""),
            "checks": self._checks(p.get("head", {}).get("sha", "")),
            "mergeable": p.get("mergeable_state", ""),
            "files": [
                {"path": f["filename"], "additions": f.get("additions", 0), "deletions": f.get("deletions", 0), "status": f.get("status", "")}
                for f in self.t.api("GET", f"repos/{self.slug}/pulls/{number}/files?per_page=100")
            ],
            "commits": [
                {"sha": c["sha"][:7], "message": c.get("commit", {}).get("message", "").splitlines()[0]}
                for c in self.t.api("GET", f"repos/{self.slug}/pulls/{number}/commits?per_page=100")
            ],
            "thread": [
                {"author": login(c.get("user")), "created": c.get("created_at", ""), "body": c.get("body", "")}
                for c in self.t.api("GET", f"repos/{self.slug}/issues/{number}/comments?per_page=100")
            ],
            "reviews": [
                {"author": login(r.get("user")), "state": r.get("state", ""), "body": r.get("body", "")}
                for r in self.t.api("GET", f"repos/{self.slug}/pulls/{number}/reviews?per_page=100")
            ],
        })
        return item

    def get_diff(self, number):
        return self.t.api("GET", f"repos/{self.slug}/pulls/{number}", raw=True, accept="application/vnd.github.v3.diff")

    def comment(self, number, body, is_pr):
        return self.t.api("POST", f"repos/{self.slug}/issues/{number}/comments", {"body": body}).get("html_url", "")

    def review(self, number, body, event):
        ev = {"approve": "APPROVE", "request_changes": "REQUEST_CHANGES"}.get(event, "COMMENT")
        r = self.t.api("POST", f"repos/{self.slug}/pulls/{number}/reviews", {"body": body, "event": ev})
        return r.get("html_url", "")

    def label(self, number, labels, is_pr):
        self.t.api("POST", f"repos/{self.slug}/issues/{number}/labels", {"labels": labels})
        return f"https://{self.repo.get('host', 'github.com')}/{self.slug}/issues/{number}"

    def assign(self, number, users, is_pr):
        self.t.api("POST", f"repos/{self.slug}/issues/{number}/assignees", {"assignees": users})
        return f"https://{self.repo.get('host', 'github.com')}/{self.slug}/issues/{number}"

    def open_issue(self, title, body, labels):
        return self.t.api("POST", f"repos/{self.slug}/issues", {"title": title, "body": body, "labels": labels}).get("html_url", "")

    def close(self, number, is_pr):
        return self.t.api("PATCH", f"repos/{self.slug}/issues/{number}", {"state": "closed"}).get("html_url", "")

    def merge(self, number):
        self.t.api("PUT", f"repos/{self.slug}/pulls/{number}/merge", {"merge_method": "squash"})
        return f"https://{self.repo.get('host', 'github.com')}/{self.slug}/pull/{number}"
