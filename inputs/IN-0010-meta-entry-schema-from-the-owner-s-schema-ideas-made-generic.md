# IN-0010: meta entry schema from the owner's schema ideas, made generic

- **Received:** 2026-10-11
- **From:** @aurimasniekis
- **Distilled into:** contracts/metadata-schema.md, contracts/metadata-plugin.md, modules/meta/overview.md, GOAL-0002
- **Redacted:** a local file path is written as `[redacted]`. The owner asked that it never be mentioned; the ideas are credited only as the owner's schema ideas.

---

## §1 Request

for `meta` service item schema i think u can try to see what i tried to define before as it was based on mangabaka and etc, adjust maybe to be more generic and would allow to pull other sources too `[redacted]` (dont mention this anywhere just user provided some ideas of schema fiels and etc)

## §2 What the owner's schema ideas contained (keeper's summary)

- **Entry:** type, status, title, native title, romanized title, description, content rating, alternative titles, secondary titles per language, licences per language, tags, genres, adaptations, final reference, authors, artists, editors, other people, companies, publishers, relationships, links, items, last item, total items, cover image, provider sources, announcement / start / end dates (partial), created / updated.
- **Person:** name, original name, aliases (+ original), birth / death (partial dates), gender, country, language, biography, social links, links, image. **Company:** name, original name, aliases, founded / closed, status, type, country, language, description, links, image.
- **Credits:** person + role (+ character name for voice actors), order, joined / left dates; company + role, order, dates, links.
- **Tag:** parent, name, description, content rating, spoiler, genre, explicit, level, count, implied-by tags. Tag weight: core, defining, recurrent, incidental, unweighted.
- **Image:** format, size, file size, URL, SHA-256, thumbhash, blurhash, scaled widths 150/250/350 at x1–x3.
- **Title:** type (alternative, native, official, romanized, unofficial), language, note, traits, primary/official/native/alternative flags.
- **References and items:** a reference = unit (chapter, volume, part, arc, season, episode, issue, book, …) + qualifier (exact, approximate, estimated, before, after, up to, through) + value. Items = unit, number, name, description, release date, links.
- **Relations:** type (adaptation, alternative, prequel, sequel, side story, spin-off, …), chronology (narrative, release), manual flag, note. **Adaptations:** type (anime variants, live action, drama, film, game, visual novel, audio/radio drama, stage, …), title, start/end references, dates.
- **Enums:** entry types (novel, light novel, web novel, manga, manhwa, manhua, OEL, comic, western comic, graphic novel, webcomic, webtoon, doujinshi, one-shot, anthology, visual novel, artbook, guidebook, magazine, fanfic, other), statuses (releasing, completed, hiatus, cancelled, upcoming, unknown), content ratings (safe, suggestive, erotic, pornographic, unknown), person roles, company types/roles/statuses, link types.
- **Provider:** a type, find by ID, optional "find all" with an estimated count.
