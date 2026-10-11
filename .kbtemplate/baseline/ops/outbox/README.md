# Outbox

Drafted forge actions waiting for the operator: comments, reviews, labels, assignments, new issues. One file per action, created with `python3 tools/kb.py ops draft …` ([authority](../../meta/authority.md)).

```markdown
---
forge: github
repo: api
action: review            # comment | review | label | assign | open_issue | close | merge
target: 42                # issue/PR number (empty for open_issue)
kind: pr                  # pr | issue
event: request_changes    # review only: comment | approve | request_changes
labels: []                # label/open_issue only
created: 2026-10-12T09:30:00Z
state: draft              # draft -> approved -> posted   (or discarded)
---
<!-- Notes for the operator: why this review, what I checked. Not posted. -->

The text that will be posted.
```

Tell the agent "approve" (or edit the file and set `state: approved`), then it runs `kb.py ops post <file>`. Posted drafts keep `posted_url` as a record. Delete or archive them when you like.
