# media

Icons and banners for this collection's arrows, referenced from their
`metadata.media` by raw URL:

```
media/<auid>/banner.svg   # 2:1
media/<auid>/icon.svg     # square
```

```yaml
metadata:
  media:
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/<auid>/banner.svg
```

`<auid>` is the arrow's identity in `collection.yaml` (its `auid`, or the last
segment of its `path`). Files live here only when the project has no stable
official URL for them, or when the banner is generated from the project's
official icon. Official assets that upstream already publishes are linked at
an upstream tag instead of copied.

SVG first; raster only at icon >= 512px or banner >= 1200x600. How to find,
check and generate them:
[`skills/quiver-arrow-authoring/references/media.md`](../skills/quiver-arrow-authoring/references/media.md).
