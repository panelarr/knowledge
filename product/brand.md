---
title: Brand and logo
status: proposed
tags: [product, brand, design]
related: [product/vision.md, modules/mihon-source/overview.md, modules/meta/overview.md]
inputs: [IN-0030]
updated: 2026-10-11
---

# Brand and logo

## Summary

The owner asked for a Panelarr SVG logo, used in every admin as "LOGO Panelarr Meta" and so on (IN-0030). This is the keeper's first draft for the owner to approve. The mark is **a manga page cut into three panels with slanted gutters** on a rounded tile: "panels" for Panelarr, in the *arr* family's rounded-tile style.

## Files

| File | Use |
|---|---|
| [brand/panelarr-icon.svg](brand/panelarr-icon.svg) | Full colour: pink tile `#E0457B`, white panels. Headers, favicons, README badges, image labels |
| [brand/panelarr-icon-mono.svg](brand/panelarr-icon-mono.svg) | One colour (`currentColor`; the panels are cut out). Monochrome spots, overlays, the theme's text colour |

Both use a `64×64` viewBox and stay legible at 16 px.

## Usage in admin UIs and apps

- **Header lockup:** icon (24–28 px) + **"Panelarr"** (bold, the theme's text colour) + the product name in a lighter weight and muted colour: `Panelarr Meta`, `Panelarr Mihon Source`, later `Panelarr` alone for the main app. The wordmark is HTML text in the UI font, not part of the SVG.
- **Favicon:** the colour icon as `favicon.svg` (plus a 32 px PNG fallback if needed). Page title like `Panelarr Meta`.
- **Login screen:** the icon at about 48–64 px above the product name.
- Each admin keeps its own UI accent colour; the logo keeps its pink.
- Served from the app itself (no external hosts), so the strict CSPs stay intact.

## Colours

| Token | Value | Use |
|---|---|---|
| Brand pink | `#E0457B` | Logo tile |
| Panel white | `#FFFFFF` | Logo panels |

## Licence

Proposed: the logo files follow the KB's docs licence (CC BY 4.0) and are copied into each code repo. Trademark wording is part of the open legal question ([Q-0016](../questions/README.md)).
