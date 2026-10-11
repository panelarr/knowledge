# IN-0022: meta duplicate finding with optional model judging

- **Received:** 2026-10-11
- **From:** @aurimasniekis
- **Distilled into:** GOAL-0004 (proposed), modules/meta/overview.md, Q-0035, Q-0036

---

## §1 Idea

also another goal we can add to meta is to use new find duplicates or matching items in the meta where the entries are kinda same, either by simple word comparison or running through decision model like gpt6 luna,jef,clef (all 3 i think are same api just different providers) so we try to find most similar by our selves and then pass to those models to compare and give user a list of results, the comparison job should also be configurable to use model or just first is enough for user to compare
