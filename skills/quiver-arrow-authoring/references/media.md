# Icons and banners (`metadata.media`)

Derived from quiver.desktop's arrow views (`src/features/arrow-details/components/hero.tsx`,
`src/features/search/components/card/arrow-card.tsx`,
`src/features/collection/styles/collection.css`,
`src/features/sidebar/components/arrows/arrow-icon.tsx`) and quiver.core's
Fletcher media heuristics (`internal/engine/manifold/fletcher/internal/media/`),
as of quiver.desktop `develop@a01a40c` and quiver.core `develop@0fba569`.

## Contents

1. What the desktop needs
2. Quality bar
3. Finding the official assets
4. Generating a banner
5. Hosting and URLs
6. Checklist

---

## 1. What the desktop needs

```yaml
metadata:
  media:
    icon: https://...     # square
    banner: https://...   # 2:1
```

Both are **URLs** fetched by the app's webview; nothing is uploaded with the
manifest. Omit a field rather than pointing it at something unsuitable.

| Field | Where it shows | Frame |
|---|---|---|
| `icon` | sidebar rows, tiles, the details hero, search cards without a banner | small square avatar, image cropped with `object-cover`; without an icon the app shows the name's initial |
| `banner` | details hero (up to 440px wide), search result cards, collection hero | **2:1** box; the hero letterboxes it (`contain`), cards and collection heroes crop it (`cover`) |

So a banner must be exactly 2:1 to look right everywhere, and keep its
important content (logo, name) away from the edges, which cropping may cut.

## 2. Quality bar

Prefer **SVG** for both: sharp at every size and density, small, and
writable by any agent. Use raster only when no SVG exists, and only at a
size that stays crisp on high-density screens. `media` in the helper script
applies exactly these thresholds:

| | Good | Acceptable | Reject |
|---|---|---|---|
| icon | square SVG; square PNG/WebP >= 512px | square raster >= 256px | not square (beyond 2%), < 256px, unknown format |
| banner | 2:1 SVG; 2:1 raster >= 1200x600 | 2:1 raster >= 800x400; other landscape shapes (warned: will be cropped or letterboxed) | narrower than 1.5:1, below 800x400 |

JPEG is fine for photographic banners; PNG or WebP for anything with flat
colour or text. Avoid GIF.

```sh
python3 "$SKILL_DIR/scripts/quiver_arrow.py" media <url-or-file> [...]
```

## 3. Finding the official assets

Use only assets the project itself publishes. In this order:

1. **Icon**, SVG first: the repository's icon sources, e.g.
   `dist/linux/hicolor/scalable/apps/*.svg`, `src-tauri/icons/`,
   `assets/`, `resources/`, `docs/`, `build/icon.*`, `logo.svg`,
   `*.desktop` `Icon=` targets, a macOS `.icns`/Windows `.ico` source's
   PNG export; then the project website's logo / `apple-touch-icon`.
   (Fletcher probes `src-tauri/icons/icon.png`, `build/icon.png` and
   `logo.svg`, and README images that are square.)
2. **Banner**: a wide image near the top of the README, the repository's
   social preview / the website's `og:image`, or a hero image on the website.
   It must be the project's own artwork, landscape, and pass the quality bar.
3. List candidates with the GitHub tree API or by reading the repository;
   check each with `media`. Link files **at a tag**, never at a moving branch:
   `https://raw.githubusercontent.com/OWNER/REPO/<tag>/path/icon.svg`.

Never draw, trace, recolour or "improve" a logo, and never invent one for
software that has none: leave `icon` out and the app shows the initial. A
generic stock image is not a banner either.

## 4. Generating a banner

When the project publishes a usable icon but no suitable banner, generate
one around that icon:

```sh
python3 "$SKILL_DIR/scripts/quiver_arrow.py" banner \
  --icon https://raw.githubusercontent.com/OWNER/REPO/<tag>/path/icon.svg \
  --name "Display Name" \
  --background '#1F2937' \
  --out media/<auid>/banner.svg
```

- Output: a 1200x600 SVG with the official icon (embedded as a data URI,
  unmodified) and the display name, centred on a solid background.
  Embedding is required: an SVG shown as an image cannot load external
  files.
- `--icon` must pass the icon check; SVG strongly preferred (a raster icon
  is embedded at its own resolution, so it must be >= 512px to stay sharp).
  Embedded files are capped at 1 MiB.
- `--background`: the project's brand colour when it has one (from its
  website or icon), otherwise a neutral dark (`#1F2937`) or light
  (`#F3F4F6`) tone that contrasts with the icon. Text colour defaults to
  black or white for contrast; override with `--text-color`.
- `--name`: the software's display name (the arrow's `metadata.name`).
  Long names shrink automatically; the command warns when one may not fit.
- Re-run `media` on the result: it must report `banner: good`. If a real
  browser is available, look at it too (in a 2:1 box, with `contain` and
  with `cover`).

Do not generate icons.

## 5. Hosting and URLs

`metadata.media` needs a public URL, so decide where each file lives:

| Asset | Where | URL |
|---|---|---|
| Official icon/banner in the upstream repo | leave it there | raw URL pinned to an upstream **tag** |
| Official asset only on a website | link it, if the URL is stable | as published |
| Generated banner (or an official asset with no stable URL) for an arrow in **quiver.essentials** | `media/<auid>/banner.svg` (or `icon.svg`, `icon.png`) in this repository | `https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/<auid>/banner.svg` |
| Generated banner for an arrow in another collection | the same `media/<auid>/` layout in that collection's repository | that repository's raw URL |
| Generated banner for an arrow in its own repository | a stable path in that repository (e.g. `docs/banner.svg`) | raw URL on its default branch or a tag |

`<auid>` is the arrow's public identity in the collection (its `auid`, or
the last segment of its `path`). Commit the media file in the same change as
the manifest that references it, and keep the file name stable: arrows keep
pointing at it across releases.

## 6. Checklist

- [ ] Icon: official, square, SVG (or raster >= 512px), `media` says `good`.
- [ ] Banner: official or generated from the official icon, exactly 2:1,
      `media` says `good`.
- [ ] URLs are public, pinned to a tag (upstream) or at the hosting path above.
- [ ] Generated files committed under `media/<auid>/` with the manifest.
- [ ] No invented, traced or altered logos.
