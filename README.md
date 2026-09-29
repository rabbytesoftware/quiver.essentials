# quiver.essentials

A Quiver collection of arrows that are essential to Quiver's own development and
ecosystem tooling — shared install-time dependencies (`tools:`) that other arrows,
including Rabbyte's own products, depend on instead of reimplementing.

Followable as `github.com/rabbytesoftware/quiver.essentials`. Individual arrows are
addressable directly without following the collection, e.g.
`github.com/rabbytesoftware/quiver.essentials/appimage-runtime`.

See `collection.yaml` for the manifest and [docs/spec/manifests/v0/collection.md](
https://github.com/rabbytesoftware/quiver.core/blob/develop/docs/spec/manifests/v0/collection.md)
in `quiver.core` for the schema this repo follows.

## Agent skills

[`skills/`](skills/README.md) holds skills that teach AI agents to work with
Quiver. [`quiver-arrow-authoring`](skills/quiver-arrow-authoring/SKILL.md) lets
an agent (Claude Code, Codex, Gemini CLI, or any chat assistant via a bundled
file) write, validate and test-install arrows and collections — including new
arrows for this collection.
