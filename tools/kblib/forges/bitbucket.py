"""Bitbucket Cloud. HTTPS with $BITBUCKET_TOKEN (a repository/workspace access token, Bearer).

Bitbucket has no labels; `label` raises Unsupported. Issues exist only if the repo's issue tracker is on.
"""
from __future__ import annotations

from .base import Forge, Unsupported, login


class Bitbucket(Forge):
    name = "bitbucket"

    def _pr(self, p: dict) -> dict:
        return {
            "number": p["id"],
            "title": p.get("title", ""),
            "url": p.get("links", {}).get("html", {}).get("href", ""),
            "author": login(p.get("author")),
            "state": p.get("state", "").lower(),
            "updated": p.get("updated_on", ""),
            "labels": [],
            "comments": p.get("comment_count", 0),
            "kind": "pr",
            "draft": bool(p.get("draft")),
            "head": p.get("source", {}).get("branch", {}).get("name", ""),
            "base": p.get("destination", {}).get("branch", {}).get("name", ""),
        }

    def _issue(self, i: dict) -> dict:
        return {
            "number": i["id"],
            "title": i.get("title", ""),
            "url": i.get("links", {}).get("html", {}).get("href", ""),
            "author": login(i.get("reporter")),
            "state": i.get("state", ""),
            "updated": i.get("updated_on", ""),
            "labels": [x for x in (i.get("kind"), i.get("priority")) if x],
            "comments": 0,
            "kind": "issue",
            "draft": False,
        }

    def list_issues(self, since, limit):
        q = f'repositories/{self.slug}/issues?pagelen={min(limit, 50)}&sort=-updated_on&q=(state="new" OR state="open")'
        if since:
            q = q[:-1] + f' AND updated_on>{since[:19]})'
        try:
            return [self._issue(i) for i in self.t.api("GET", q.replace(" ", "%20").replace('"', "%22")).get("values", [])]
        except Exception as e:
            if "404" in str(e):
                return []
            raise

    def _checks(self, number: int) -> str:
        try:
            st = self.t.api("GET", f"repositories/{self.slug}/pullrequests/{number}/statuses").get("values", [])
        except Exception:
            return "unknown"
        states = {s.get("state") for s in st}
        if not states:
            return "none"
        if states & {"FAILED", "STOPPED"}:
            return "failure"
        if "INPROGRESS" in states:
            return "pending"
        return "success"

    def list_prs(self, since, limit):
        out = []
        for p in self.t.api("GET", f"repositories/{self.slug}/pullrequests?state=OPEN&pagelen={min(limit, 50)}").get("values", []):
            if since and p.get("updated_on", "") < since:
                continue
            item = self._pr(p)
            item["checks"] = self._checks(p["id"])
            item["review"] = ""
            out.append(item)
        return out

    def _thread(self, kind: str, number: int) -> list[dict]:
        vals = self.t.api("GET", f"repositories/{self.slug}/{kind}/{number}/comments?pagelen=100").get("values", [])
        return [{"author": login(c.get("user")), "created": c.get("created_on", ""),
                 "body": c.get("content", {}).get("raw", "")} for c in vals if not c.get("deleted")]

    def get_issue(self, number):
        i = self.t.api("GET", f"repositories/{self.slug}/issues/{number}")
        item = self._issue(i)
        item["body"] = i.get("content", {}).get("raw", "")
        item["thread"] = self._thread("issues", number)
        return item

    def get_pr(self, number):
        p = self.t.api("GET", f"repositories/{self.slug}/pullrequests/{number}")
        item = self._pr(p)
        stat = self.t.api("GET", f"repositories/{self.slug}/pullrequests/{number}/diffstat?pagelen=100").get("values", [])
        commits = self.t.api("GET", f"repositories/{self.slug}/pullrequests/{number}/commits?pagelen=100").get("values", [])
        item.update({
            "body": p.get("description") or "",
            "checks": self._checks(number),
            "mergeable": "",
            "files": [{"path": (s.get("new") or s.get("old") or {}).get("path", ""), "additions": s.get("lines_added", 0),
                       "deletions": s.get("lines_removed", 0), "status": s.get("status", "")} for s in stat],
            "commits": [{"sha": c.get("hash", "")[:7], "message": c.get("message", "").splitlines()[0] if c.get("message") else ""}
                        for c in commits],
            "thread": self._thread("pullrequests", number),
            "reviews": [{"author": login(r.get("user")), "state": "APPROVED" if r.get("approved") else r.get("state", ""), "body": ""}
                        for r in p.get("participants", []) if r.get("role") == "REVIEWER"],
        })
        return item

    def get_diff(self, number):
        return self.t.api("GET", f"repositories/{self.slug}/pullrequests/{number}/diff", raw=True, accept="text/plain")

    def comment(self, number, body, is_pr):
        kind = "pullrequests" if is_pr else "issues"
        r = self.t.api("POST", f"repositories/{self.slug}/{kind}/{number}/comments", {"content": {"raw": body}})
        return r.get("links", {}).get("html", {}).get("href", "")

    def review(self, number, body, event):
        url = self.comment(number, body, True)
        if event == "approve":
            self.t.api("POST", f"repositories/{self.slug}/pullrequests/{number}/approve", {})
        elif event == "request_changes":
            self.t.api("POST", f"repositories/{self.slug}/pullrequests/{number}/request-changes", {})
        return url

    def label(self, number, labels, is_pr):
        raise Unsupported("bitbucket has no labels; put the triage outcome in a comment instead")

    def open_issue(self, title, body, labels):
        r = self.t.api("POST", f"repositories/{self.slug}/issues", {"title": title, "content": {"raw": body}})
        return r.get("links", {}).get("html", {}).get("href", "")

    def close(self, number, is_pr):
        if is_pr:
            r = self.t.api("POST", f"repositories/{self.slug}/pullrequests/{number}/decline", {})
        else:
            r = self.t.api("PUT", f"repositories/{self.slug}/issues/{number}", {"state": "resolved"})
        return r.get("links", {}).get("html", {}).get("href", "")

    def merge(self, number):
        r = self.t.api("POST", f"repositories/{self.slug}/pullrequests/{number}/merge", {"merge_strategy": "squash"})
        return r.get("links", {}).get("html", {}).get("href", "")
