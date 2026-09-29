# Publishing: where manifests live, refs, and collections

Derived from quiver.core `docs/spec/manifests/v0/{arrow,collection,versioning}.md`,
`docs/spec/manifold.md` §4.1 and `internal/engine/manifold/resolver/resolver.go`,
verified against quiver.core `develop` @ `0fba569` (2026-09-29).

## Contents

1. Namespaces
2. Where the manifest file goes
3. The ref is the version
4. collection@v0
5. Fletcher (repositories without a manifest)
6. Choosing where to publish

---

## 1. Namespaces

```
domain/user/repo[/auid][@ref]
github.com/junegunn/fzf                  # refless: latest stable release, else default branch
github.com/junegunn/fzf@v0.74.4          # exact tag, branch or commit
github.com/owner/tool@v1.*               # glob, matched against tags only
github.com/rabbytesoftware/quiver.essentials/appimage-runtime   # arrow inside a collection
```

- **Refless** resolution: the latest release on the **stable** channel (the
  host's latest release, else the newest stable-semver tag such as `1.2` or
  `v1.2.3`). If there is none, or that tag has no manifest, Quiver tries the
  repository's **other release channels** (beta, nightly, ...) and only then
  the default branch. So a refless reference prefers stable, but can land on
  a prerelease when no stable release carries a manifest.
- **Globs** (`@v1.*`) match tags only, newest stable semver first; no tag
  matching is an error. Stable-semver matches always rank first; a
  non-stable tag (`v1.3.0-rc.1`) is picked only when no stable tag matches.
- Prefer refless or a glob in `tools:` so dependents follow updates; pin an
  exact ref only when a specific build is required. Avoid the literal
  `@latest` (it is sent to the host as a tag named `latest`).

## 2. Where the manifest file goes

| Situation | Files tried, in order |
|---|---|
| Arrow owns its repository (`github.com/owner/repo`) | `ARROW.md`, then `arrow.yaml`, at the repository root |
| Arrow inside a collection (`github.com/owner/coll/<auid>`) | `<path>.md`, then `<path>.yaml`, where `path` comes from the collection entry |
| Collection | `COLLECTION.md`, then `collection.yaml`, at the repository root |

**Markdown form** (`ARROW.md`, `<path>.md`): the first fenced block whose
fence is exactly ` ```arrow ` is the manifest; everything else is the arrow's
readme, shown on its details page. `arrow.yaml` has no readme. Prefer
`ARROW.md` for an arrow in its own repository: the prose documents it for free.
(For collections the fence is ` ```collection `.)

## 3. The ref is the version

Quiver reads the manifest *at a git ref*, and that ref is the arrow's
version. Consequences for authors:

- Never write `version:`; tag releases instead.
- `${REF}` is that ref, verbatim. When the arrow ships in the **same**
  repository as the release assets, and tags match the release names, a URL
  can be written once:
  `https://github.com/owner/tool/releases/download/${REF}/tool-linux-amd64.tar.gz`.
  Each tag's manifest is read at that tag, so it can still carry that
  release's `checksum`: update the digests in the commit you tag (typically
  from the release pipeline). Omitting the checksum is possible but leaves
  downloads unverified; say so if you do.
- `${REF}` inside an `update` hook is the **currently installed** ref, not
  the next one (see `manifest-reference.md` §6, "Updating").
- For an arrow published **elsewhere** (a collection, a fork), `${REF}` is
  the collection's ref and says nothing about the upstream software: pin the
  upstream version in the URL and add the checksum. Updating the software
  means editing the manifest and tagging a new collection release.
- To publish a new version, commit the manifest change and push a
  stable-semver tag (`v1.3.0`). Refless users get it automatically.

## 4. collection@v0

A collection is a curated list of arrows in one repository. It does not
install or order anything; it points.

```yaml
schema: "collection@v0"

metadata:
  name: "My Collection"             # required
  description: "What it groups"     # required
  url: "https://github.com/owner/coll"
  maintainers: ["owner"]            # plain strings here, unlike arrow metadata
  tags: ["tooling"]
  media: {icon: "https://...", banner: "https://..."}

arrows:
  - path: mytool                    # local: ./mytool.md or ./mytool.yaml -> <coll ns>/mytool
  - auid: other-tool                # local, explicit identity
    path: tools/other-tool          #   file ./tools/other-tool.{md,yaml}  -> <coll ns>/other-tool
  - namespace: github.com/owner/x   # external arrow in its own repo
  - github.com/owner/y              # external, string shorthand
```

Rules (`validate --collection` checks them):

- `name`, `description` and a non-empty `arrows` list are required.
  No `version:`.
- Each entry has exactly one of `path` / `namespace`; `auid` only with
  `path`; `auid` has no `/` or `@`; `path` has no `..`, `\`, `?`, `#`.
- Resolved namespaces must be unique (`duplicate_namespace`).
- A local arrow's public namespace is the collection's namespace (without
  ref) plus the auid; it is always read at the collection's ref.
- Once published, keep `auid`s stable: they are the arrows' identities.
  Moving a file is safe when its entry has an explicit `auid`.
- Inside a local arrow, set `metadata.quiver` to the collection namespace.

Adding an arrow to an existing collection = add its file at the chosen path
+ add the entry to `arrows:` + validate both.

## 5. Fletcher (repositories without a manifest)

When enabled on a daemon (`manifold.fletcher.enabled`, off by default), Quiver
can synthesize a manifest from a repository's release assets if the
repository has no `ARROW.md`/`arrow.yaml`. Those arrows report
`origin: inferred`. Fletcher cannot express services, variables, methods,
dependencies or custom install logic, refuses low-confidence builds, and
never runs on a repository that ships a manifest. A hand-written manifest is
the way to get any of those, or to fix what Fletcher guessed wrong.

## 6. Choosing where to publish

| The user... | Publish as |
|---|---|
| owns the software's repository | `ARROW.md` at its root; `${REF}` URLs are an option |
| does not own it, wants it in their own collection | `<path>.yaml` in their collection repo + a collection entry; pinned URLs + checksums |
| contributes to an existing collection (e.g. quiver.essentials) | same as above, following that repo's conventions and review process |
| only needs it locally / for testing | any file, registered with `quiver arrow seed <ns@ref> --file <file>` (seeding always needs an explicit `@ref`) |
