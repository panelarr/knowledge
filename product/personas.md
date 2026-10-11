---
title: Personas
status: draft
tags: [product, personas]
related: [product/vision.md, architecture/multi-user.md]
inputs: [IN-0002]
updated: 2026-10-11
---

# Personas

## Summary

These are the people Panelarr serves. Design reviews check features against them.

| Persona | Who | Needs |
|---|---|---|
| **Hoster / admin** | Runs Docker or Unraid at home, already runs other *arr* apps | Simple install; chooses components; per-source proxies and solvers; sees health; controls users and storage |
| **Household reader** | Partner, sibling, friend with an account | Own library and progress; reads on phone (PWA) and desktop; no setup |
| **Power curator** | Admin or trusted user | Merge sources into one Work, pick scanlators, fix metadata matches, bulk operations |
| **Collector with files** | Has years of CBZ/CBR folders | Point Panelarr at the folders, get metadata and tracking, optionally adopt the files |
| **Tool builder** | Third party | Uses mihon-source or meta standalone through gRPC or OpenAPI |
| **Restricted reader** | A child or guest | Content-rating ceiling, limited sources, no downloads |
