# IN-0029: Real meta import numbers; first try failed on Docker disk

- **Received:** 2026-10-11
- **From:** @aurimasniekis
- **Distilled into:** research/mangabaka.md, modules/meta/overview.md, GOAL-0002 history

---

## §1 Report

`make sync mangabaka` failed on first try my docker ran out of disk space so i had to restart it

(meta sync output, second run)
```
sync finished provider=mangabaka kind=dump status=succeeded upserts=564155 changed=402155 merges=258068 removed=0 took=13m22.582s
records 564155 (changed 402155), merges 258068, removals 0, skipped 0, marked removed 0
active entries 306084, database size 6656 MB
```
(The run resumed with cursor `<sha1>:175629` from the failed first run; the plugin was meta-mangabaka `ad2159f`, managed mode.)
