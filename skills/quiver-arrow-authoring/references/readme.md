# The arrow's readme (its Overview page)

Derived from quiver.core `docs/spec/manifests/v0/arrow.md` §2.1 (markdown form
and readme extraction) and quiver.desktop's readme renderer
(`src/features/arrow-details/components/readme-panel.tsx`,
`src/features/arrow-details/lib/readme-sanitize-schema.ts`), as of
quiver.core `develop@0fba569` and quiver.desktop `develop@d948868`.

## Contents

1. Why every arrow should have one
2. The markdown form
3. What Quiver Desktop renders
4. What to write
5. Sources for facts and screenshots
6. Screenshots
7. Checking it

---

## 1. Why every arrow should have one

Quiver Desktop's details page shows the arrow's **readme** in the Overview
tab. Without one, Overview falls back to the bare Details card (requirements,
maintainers, links) and the user learns nothing about the software beyond
the one-line `metadata.description`. A readme is what makes an arrow page
look like a store listing instead of a config file. Write one for every
arrow there is material for, which is almost always.

## 2. The markdown form

A readme only exists when the manifest is delivered as markdown:

| Arrow lives | File |
|---|---|
| in its own repository | `ARROW.md` at the root (instead of `arrow.yaml`) |
| in a collection | `<path>.md` (instead of `<path>.yaml`); the collection entry does not change, `.md` is tried first |

The file is markdown prose plus **one** fenced block whose fence is exactly
` ```arrow `, holding the manifest. Quiver uses the first such block as the
manifest and serves **everything else** (before and after it) as the readme
(`GET /v0/arrow/{ns}/readme`). Put the prose first and the manifest at the
end: the YAML is for Quiver, the prose is for people. An `arrow.yaml` /
`<path>.yaml` has no readme at all.

Converting an existing arrow: rename the file (`git mv x.yaml x.md`), wrap
the YAML in ` ```arrow ` … ` ``` `, write the prose above it. The manifest
itself does not change, and neither does its namespace.

## 3. What Quiver Desktop renders

GitHub-flavoured markdown, sanitized:

- Headings, paragraphs, lists, **tables**, links, inline code and code blocks.
- Images with **absolute** `https://` (or `data:`) URLs, shown full width
  (about 830px) with rounded corners. Relative paths do not work: use the
  raw URL where the image is hosted.
- Raw HTML for what markdown cannot express, filtered to a safe subset:
  `<video>`/`<audio>`/`<source>`/`<track>` are allowed (no `autoplay`).
- ` ```mermaid ` code blocks render as diagrams.
- **Not** rendered: `<iframe>`, scripts, styles, event handlers, anything the
  sanitizer drops. Do not embed YouTube players; link to them.

The hero above the readme already shows the name, icon, banner, description
and tags, so the readme does not need to start with a title or repeat the
banner.

## 4. What to write

Write the readme **for the arrow**: original, factual prose about the
software and about installing it through Quiver. Use the vendor's material as
a source, not as text to paste: no copied marketing copy, no superlatives you
cannot back up.

Recommended structure, adapting it to what the software is:

1. **Opening paragraph** (no heading): what the software is, who it is for,
   what makes it distinctive. Two to four sentences.
2. **A screenshot** of the software itself, right after the opening.
3. **Features**: a bulleted list, bold lead-in per item, one line each.
   Include only features the software really has.
4. **More screenshots** where they show something new (another feature,
   another view). Skip near-duplicates.
5. **Installing with Quiver**: a table of platforms and what Quiver installs
   on each (format, where it ends up, OS version requirements), including the
   platforms that are *not* supported and why.
6. **Good to know**: what a user needs before or after installing: accounts
   or devices it requires, where it keeps data and whether uninstalling
   removes it, self-updating, unverified downloads, installers that write
   outside Quiver's folder, what happens if the software is already
   installed, published hardware minimums.
7. **Usage** (CLIs and services): the commands to try first, the port it
   serves on, the methods the arrow adds.
8. **License and trademarks**: the license (link it), who owns the name and
   logo, where the icon, banner and screenshots come from.

Length: what a reader skims in a minute, typically 300–800 words plus
images. Write in English unless the collection uses another language. Every
statement about installation behaviour must match the manifest; every
statement about the software must come from a source in §5.

## 5. Sources for facts and screenshots

In order of preference:

1. The project's own README, documentation and website.
2. Its official store listings, which carry vendor-written descriptions,
   current screenshots and often system requirements:
   - Microsoft Store: `https://storeedgefd.dsx.mp.microsoft.com/v9.0/products/<id>?market=US&locale=en-us&deviceFamily=Windows.Desktop`
     (`Payload.Images` with `ImageType: screenshot`, `Payload.SystemRequirements`,
     `Payload.Description`). Check `PublisherName` is the real vendor.
   - Apple App Store: `https://itunes.apple.com/lookup?id=<id>` (`screenshotUrls`).
     Many results are iPhone/iPad apps whose screenshots are phone-sized; use
     them only for an arrow that installs that app.
3. Press and brand kits (logos, sometimes screenshots and banners).
4. Screenshots taken from the real, installed app, when the user can provide
   them or the environment can capture them.

Check the publisher of every listing: store search results include
third-party clients named after popular apps. Never describe features from
memory or invent requirements.

## 6. Screenshots

- Show the software itself, current version, at rest (no personal data).
- 2–4 images, each showing something different; 16:9 or the app's own
  window shape.
- Host them where they will stay: an upstream URL pinned to a tag when one
  exists; otherwise `media/<auid>/screenshots/<what-it-shows>.jpg` in the
  collection, referenced by its raw URL (`references/media.md` §5). Store
  and CDN URLs change when the vendor updates a listing: copy those.
- Size: about 1600px wide. JPEG (quality ~85) for photographic or gradient
  marketing composites, PNG or WebP for flat UI; keep each file under ~500 KB.
- Alt text describes what the image shows.
- Say where the screenshots come from in the license section, and when they
  are from another platform than the one the arrow installs (same design).

## 7. Checking it

```sh
python3 "$SKILL_DIR/scripts/quiver_arrow.py" readme apps/myapp.md
```

It extracts the readme the way Quiver does and flags what would render badly
or not at all: no prose, no screenshot, relative or non-https image URLs,
`<iframe>`/`<script>`, an arrow fence that is not the manifest; with
`--online` it also fetches every image and checks it loads. Then validate the
manifest as usual (the validator accepts the `.md` file directly), and when a
sandbox is available confirm what the daemon serves:

```sh
python3 "$SKILL_DIR/scripts/quiver_arrow.py" sandbox seed github.com/owner/repo/myapp@test apps/myapp.md
python3 "$SKILL_DIR/scripts/quiver_arrow.py" sandbox readme github.com/owner/repo/myapp@test
```

Images hosted in a collection only load once committed to the branch the
raw URLs name. To see them before merging, push the branch and seed a copy
whose URLs point at it.
