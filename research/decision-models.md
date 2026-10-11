---
title: Decision model APIs
status: draft
tags: [research, ai, meta, duplicates]
related: [agents/goals/GOAL-0004-meta-duplicates-find-similar-entries-optional-model-review.md, modules/meta/overview.md]
inputs: [IN-0022, IN-0023]
updated: 2026-10-11
---

# Decision model APIs

> Checked 2026-10-11 against the provider pages the owner linked (IN-0023). Rate limits and batching are not documented by any of them.

## Summary

The owner's "gpt6 luna, jef, clef" (IN-0022) are **decision models**: they take a *state* (the thing to judge) and a set of **typed questions**, and return **probabilities** rather than prose. They fit meta's duplicate judge (GOAL-0004) well, since "are these the same work?" is exactly a typed question. **None returns a written reason.** The three APIs share the idea but not the wire format: TypeSafe and Cloudflare Clef are nearly identical, and OpenAI's differs.

## Providers

| | OpenAI Decisions | TypeSafe | Cloudflare Workers AI: Clef |
|---|---|---|---|
| Model | `gpt-6-luna` (only model; public beta) | `jev-latest` (e.g. `jev-1.13.0`); the owner called it "Jef" | `clef`, `clef-flash` (`@cf/cloudflare/clef`), 27B multimodal |
| Endpoint | `POST /v1/decisions` | `POST https://api.typesafe.ai/v1/systemone` | `POST https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/cloudflare/clef` |
| Auth | Bearer key | Bearer key | Bearer token |
| Input | `input` (text, or messages with `input_text` / base64 `input_image`) | `state` (string, object or array) | `state` (string, object or array) + optional `images` (up to 4, base64) |
| Questions | `questions[]`: `type`, `name`, `instructions`, `choices` / `levels` | `questions{id}`: `type`, `instructions`, `criteria` | `questions{id}` (1–64): `type`, `instructions`, `criteria` |
| Yes/no | `predicate` → `probability` | `noul` → value 0–1 | `noul` → probability |
| Choice / score | `choice` (`choice`, `probabilities`, `confidence`), `score` (`score`, `probabilities`, `confidence`) | `choice` (max 255 options), `score` (2–10 levels), with `confidence` | `choice`, `score` with probabilities |
| Refusals and errors | `refusal` answer | 401, 422, 429, 529 (back off) | — |
| Price | $0.10 / 1M input tokens, output free | not stated | $0.24 / 1M input tokens (images count), output free |
| Context | — | — | 65,536 tokens (state is truncated to fit) |

## What it means for meta (GOAL-0004)

- **One `DecisionJudge` interface, two wire adapters:**
  - an "OpenAI Decisions" adapter (`input`, `questions[]`, `predicate`);
  - a "state + questions map" adapter (`state`, `questions{}`, `noul`/`choice`/`score`, `criteria`) that serves TypeSafe and Clef. Each is configured by base URL, model and key.
- **Suggested questions per candidate pair:**
  - a yes/no "same work?" (`predicate`/`noul`);
  - a `choice` of `same_work` / `related_work` (sequel, spin-off, adaptation, other edition) / `different`, so related works aren't proposed as duplicates.
  - Store the probabilities and confidence, not prose.
- **State:** a compact JSON of both entries (titles with languages, people, year, type, status, original language, a short description excerpt). Optionally covers as images, where the provider accepts them (OpenAI, Clef).
- **Cost** is input-only and small, but cap tokens per run anyway, and cache verdicts by the pair's content hash.
- **Data:** the owner says sending provider metadata is fine for their personal, non-commercial use (IN-0023, Q-0036). Model use stays opt-in per hoster.

## Sources
- https://developers.openai.com/api/docs/guides/decisions
- https://docs.typesafe.ai/api
- https://developers.cloudflare.com/workers-ai/models/clef/
