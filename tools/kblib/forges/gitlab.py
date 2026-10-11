"""GitLab (gitlab.com and self-managed). Uses `glab api` when installed, else $GITLAB_TOKEN over HTTPS.

Merge requests are reported as kind 'pr'. GitLab has no review "event": `review` posts a note,
and `approve` additionally approves the MR.
"""
from __future__ import annotations

from urllib.parse import quote

from .base import Forge, login


class GitLab(Forge):
    name = "gitlab"

    @property
    def pid(self) -> str:
        return quote(self.slug, safe="")

    def _item(self, it: dict, kind: str) -> dict:
        return {
            "number": it["iid"],
            "title": it.get("title", ""),
            "url": it.get("web_url", ""),
            "author": login(it.get("author")),
            "state": it.get("state", ""),
            "updated": it.get("updated_at", ""),
            "labels": list(it.get("labels", [])),
            "comments": it.get("user_notes_count", 0),
            "kind": kind,
            "draft": bool(it.get("draft") or it.get("work_in_progress")),
        }

    def list_issues(self, since, limit):
        q = f"projects/{self.pid}/issues?state=opened&order_by=updated_at&per_page={limit}"
        if since:
            q += f"&updated_after={quote(since)}"
        return [self._item(i, "issue") for i in self.t.api("GET", q)]

    def _checks(self, mr: dict) -> str:
        pipe = mr.get("head_pipeline") or mr.get("pipeline") or {}
        status = pipe.get("status", "")
        if not status:
            return "none"
        if status == "success":
            return "success"
        if status in ("failed", "canceled"):
            return "failure"
        return "pending"

    def list_prs(self, since, limit):
        q = f"projects/{self.pid}/merge_requests?state=opened&order_by=updated_at&per_page={limit}"
        if since:
            q += f"&updated_after={quote(since)}"
        out = []
        for m in self.t.api("GET", q):
            item = self._item(m, "pr")
            item.update({
                "head": m.get("source_branch", ""),
                "base": m.get("target_branch", ""),
                "checks": self._checks(m),
                "review": ", ".join(login(r) for r in m.get("reviewers", [])) and
                          "requested: " + ", ".join(login(r) for r in m.get("reviewers", [])),
            })
            out.append(item)
        return out

    def _notes(self, kind: str, number: int) -> list[dict]:
        notes = self.t.api("GET", f"projects/{self.pid}/{kind}/{number}/notes?sort=asc&per_page=100")
        return [{"author": login(n.get("author")), "created": n.get("created_at", ""), "body": n.get("body", "")}
                for n in notes if not n.get("system")]

    def get_issue(self, number):
        it = self.t.api("GET", f"projects/{self.pid}/issues/{number}")
        item = self._item(it, "issue")
        item["body"] = it.get("description") or ""
        item["thread"] = self._notes("issues", number)
        return item

    def get_pr(self, number):
        m = self.t.api("GET", f"projects/{self.pid}/merge_requests/{number}")
        item = self._item(m, "pr")
        try:
            diffs = self.t.api("GET", f"projects/{self.pid}/merge_requests/{number}/diffs?per_page=100")
        except Exception:
            diffs = (self.t.api("GET", f"projects/{self.pid}/merge_requests/{number}/changes") or {}).get("changes", [])
        files = []
        for d in diffs:
            text = d.get("diff", "")
            files.append({
                "path": d.get("new_path", ""),
                "additions": sum(1 for l in text.splitlines() if l.startswith("+") and not l.startswith("+++")),
                "deletions": sum(1 for l in text.splitlines() if l.startswith("-") and not l.startswith("---")),
                "status": "added" if d.get("new_file") else "deleted" if d.get("deleted_file") else "renamed" if d.get("renamed_file") else "modified",
            })
        item.update({
            "body": m.get("description") or "",
            "head": m.get("source_branch", ""),
            "base": m.get("target_branch", ""),
            "checks": self._checks(m),
            "mergeable": m.get("detailed_merge_status", m.get("merge_status", "")),
            "files": files,
            "commits": [
                {"sha": c.get("short_id", ""), "message": c.get("title", "")}
                for c in self.t.api("GET", f"projects/{self.pid}/merge_requests/{number}/commits?per_page=100")
            ],
            "thread": self._notes("merge_requests", number),
            "reviews": [],
            "_diffs": diffs,
        })
        return item

    def get_diff(self, number):
        diffs = self.get_pr(number).get("_diffs", [])
        return "\n".join(f"--- a/{d.get('old_path')}\n+++ b/{d.get('new_path')}\n{d.get('diff', '')}" for d in diffs)

    def _kind(self, is_pr: bool) -> str:
        return "merge_requests" if is_pr else "issues"

    def comment(self, number, body, is_pr):
        self.t.api("POST", f"projects/{self.pid}/{self._kind(is_pr)}/{number}/notes", {"body": body})
        return f"https://{self.repo.get('host', 'gitlab.com')}/{self.slug}/-/{'merge_requests' if is_pr else 'issues'}/{number}"

    def review(self, number, body, event):
        url = self.comment(number, body, True)
        if event == "approve":
            self.t.api("POST", f"projects/{self.pid}/merge_requests/{number}/approve", {})
        return url

    def label(self, number, labels, is_pr):
        self.t.api("PUT", f"projects/{self.pid}/{self._kind(is_pr)}/{number}", {"add_labels": ",".join(labels)})
        return f"https://{self.repo.get('host', 'gitlab.com')}/{self.slug}/-/{'merge_requests' if is_pr else 'issues'}/{number}"

    def open_issue(self, title, body, labels):
        r = self.t.api("POST", f"projects/{self.pid}/issues", {"title": title, "description": body, "labels": ",".join(labels)})
        return r.get("web_url", "")

    def close(self, number, is_pr):
        r = self.t.api("PUT", f"projects/{self.pid}/{self._kind(is_pr)}/{number}", {"state_event": "close"})
        return r.get("web_url", "")

    def merge(self, number):
        r = self.t.api("PUT", f"projects/{self.pid}/merge_requests/{number}/merge", {"squash": True})
        return r.get("web_url", "")
