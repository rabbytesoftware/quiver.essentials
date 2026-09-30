---
name: quiver-arrow-authoring
description: Write, fix, validate and test-install Quiver arrows — arrow@v0 manifests (ARROW.md / arrow.yaml) that tell Quiver how to install, run, update and remove a piece of software per OS/arch — and collection@v0 manifests that group them. Use when the user asks to package, publish, "make an arrow", or "add to Quiver" any CLI tool, desktop app or service; to add an arrow to a collection such as quiver.essentials; to convert install instructions or release assets into a Quiver manifest; or to debug a manifest that fails validation or install.
license: GPL-3.0
metadata:
  quiver-core: develop@0fba569
  schemas: arrow@v0, collection@v0
---

# Quiver arrow authoring

You write manifests for Quiver, a decentralised package manager: an **arrow**
is one YAML document telling Quiver how to install, run, update and remove
one piece of software on each platform. Your job is to produce a manifest
that validates **and** installs correctly, built only from verified facts.

Everything in this skill was checked against quiver.core `develop` @
`0fba569`. The `references/` files hold the details; read the one you need
when a step below points at it instead of guessing.

Paths in this skill (`references/...`, `assets/...`, `scripts/...`) are
relative to the directory containing this `SKILL.md`, called `SKILL_DIR`
below. Run the helper by its full path, `python3 "$SKILL_DIR/scripts/quiver_arrow.py"`,
from the project you are working in, so manifest paths stay relative to the
project.

## Workflow

Follow these steps in order. Do not skip validation.

### 1. Gather facts (never guess them)

Establish, from the software's real release page or repository:

- **What it is**: CLI tool, desktop GUI app, or long-running service. This
  decides `expose` and whether there is an `execute`.
- **The exact release** to package (tag) and, for **each** of the six
  platforms (`linux/amd64`, `linux/arm64`, `darwin/amd64`, `darwin/arm64`,
  `windows/amd64`, `windows/arm64`): the asset URL, its format (bare binary,
  tar/zip, AppImage, DMG, MSI, other installer), and its SHA-256.
  `python3 "$SKILL_DIR/scripts/quiver_arrow.py" assets owner/repo [TAG]`
  lists GitHub release assets with their digests; `... checksum URL` hashes
  any URL.
- **What is inside** an archive when it matters (the executable's name and
  sub-path), how the program is started, what settings the user may want to
  change, and whether it needs other software (dependencies).
- **Its official icon and banner**, if any (SVG first): see
  `references/media.md` §3.
- **Where it will be published** (its own repo's `ARROW.md`, a collection,
  or local only): see `references/publishing-and-collections.md` §6.

A platform with no upstream asset is **not supported**: leave it out. If you
cannot reach the network to check, ask the user for the release data rather
than inventing URLs, tags or checksums.

### 2. Pick the shape

| The software ships... | Start from | Key steps |
|---|---|---|
| one bare executable per platform | `assets/examples/single-binary-cli.yaml` | `fetch` + `portable` (`name`) + `expose.cli` |
| one tar/zip per platform | `assets/examples/archive-cli.yaml` | `fetch` + `extract` + `expose.cli` (`auto`) |
| AppImage / DMG / zip GUI app | `assets/examples/gui-app.yaml` | `fetch` + `portable` + `expose.desktop` (`auto`) |
| a server / daemon | `assets/examples/service.yaml` | install + `execute` (no timeout) + `stop` (`signal`) + variables |
| an arrow in its own repository | `assets/templates/ARROW.md` | markdown form, readme prose around the ```arrow fence |
| several arrows in one repository | `assets/templates/collection.yaml` | `collection@v0` + one file per arrow |

Use the lowest complexity that fits: one `"*"` target with Overrideable
`url`/`checksum` maps when only the download differs per platform; separate
targets (optionally sharing an abstract `_base` via `base:`) when the steps
themselves differ. Details: `references/manifest-reference.md` §3–5.

### 3. Write the manifest

Apply the hard rules below while writing. Reference while writing:
steps and lifecycle -> `references/manifest-reference.md`; variables,
ports, dependencies -> `references/variables-and-dependencies.md`; CLI and
desktop registration -> `references/expose.md`.

### 4. Icon and banner

Fill `metadata.media` following `references/media.md`: link the project's
official icon (square, SVG preferred) and banner (2:1), pinned to a tag, and
check them with `python3 "$SKILL_DIR/scripts/quiver_arrow.py" media URL`. If
there is an official icon but no usable banner, generate one with the
`banner` command and host it under `media/<auid>/` of the collection
(`quiver.essentials` for its own arrows). Never create or alter an icon.

### 5. Validate, fix, repeat

```sh
python3 "$SKILL_DIR/scripts/quiver_arrow.py" validate path/to/manifest.yaml
python3 "$SKILL_DIR/scripts/quiver_arrow.py" validate --collection collection.yaml
```

It talks to the user's local quiver daemon on macOS/Linux (or `QUIVER_SOCKET`,
or a TCP daemon via `QUIVER_API` + `QUIVER_TOKEN`; local Windows daemons are
not reachable from the script). Validation runs in phases, so new errors can appear after you
fix old ones: repeat until `VALID`, then check that the reported supported
platforms are exactly the ones upstream ships. Error codes and fixes:
`references/validation-and-testing.md` §2. If no daemon is reachable (exit
code 2), use the checklist in §6 of that file and say the result is
unvalidated.

### 6. Test-install when possible

If this machine runs one of the arrow's platforms and a `quiver` binary is
available, install it for real in the isolated sandbox
(`references/validation-and-testing.md` §4): `sandbox up`, `seed`,
`install`, run the exposed command or start the service and probe it,
`sandbox remove`, `sandbox down`. Ask before testing manifests with
`desktop` entries or dependencies: desktop entries are written to the real
system, and the script refuses them until the user agrees.

### 7. Deliver

Give the user:

1. The manifest file(s), placed where they will be published (and the
   collection entry and any generated `media/<auid>/` files when relevant).
2. How it was checked: validator result and supported platforms, sandbox
   result, or "not validated" with the reason.
3. What you assumed or could not verify (an archive's inner layout, an
   untested platform, a missing checksum), stated plainly.
4. How to publish: commit, and for versioned releases push a stable-semver
   tag. If the arrow exposes CLI commands, mention `quiver path setup`.

## Hard rules

These are the mistakes that validate but break at install time, or that the
validator rejects most often.

1. **No `version:` field.** The git ref the manifest is read at is the
   version. Use `${REF}` only for URLs in the software's own repository.
2. **Every download pins a real release and carries its `checksum`**
   (SHA-256 from the release, bare hex or `sha256:` prefix). Never fabricate
   URLs or digests. With `${REF}`-templated URLs the digests must be updated
   in each tagged commit; if you leave them out, say the downloads are
   unverified.
3. **Claim only real platforms.** Target keys must match what upstream
   builds; an x86_64-only AppImage is `linux/amd64`, not `linux/*`.
4. **Overrideable maps must cover every platform their target matches**
   (or have `default`), with keys `default`, `*`, or containing `/`. Never
   bare `linux`/`windows`/`darwin`.
5. **Timeouts are `^\d+[sm]$`** (`30s`, `10m`, `90m`; never `1h`). Give every
   step a `title` and a `timeout`, **except long-running `execute` steps,
   which get no timeout**: a run step's timeout kills the process.
6. **Prefer install-only**: put every download and unpack in the workdir
   with `to: ${INSTALL_PATH}/...` (literal prefix; `./x` does not count) using
   `fetch`/`extract`/`portable`, and omit `uninstall`. Any other install step
   (every `run`, even one that stays in the workdir) requires an `uninstall`
   that undoes it.
7. **Usually omit `update`**: without it, updating reinstalls the new ref from
   its own manifest. An `update` hook runs the *installed* manifest with the
   *installed* `${REF}`, so it can never fetch a newer release; use it only
   for in-place maintenance.
8. **Use `extract` for archives and `portable` for AppImage, DMG, MSI and
   bare executables** instead of `run: tar ...`, `chmod +x` or FUSE. `extract`
   refuses AppImage/DMG. An MSI must be downloaded to a name ending in
   `.msi`. `portable.name` is not Overrideable: give Windows its own target
   when the file needs `.exe`. Give each `portable` a dedicated `to`
   directory nothing else creates, and a stable `from` file name.
9. **Register commands and apps with `expose`**, never with run steps that
   create symlinks, `.desktop` files or shortcuts. CLI `path` is `auto` or
   starts with `${INSTALL_PATH}`; desktop apps from `portable` use `auto`.
10. **Variables**: defaults are quoted strings (`default: "8080"`); `select`
    needs `values` containing the default; a variable without a default (or
    with `""`) must be passed on every run that uses it, so never reference
    one in `stop` (receives no variables), `uninstall` or `update` (the app
    starts them without asking). Values are pasted into commands unescaped:
    prefer `select`/`number` types for anything that reaches a shell.
11. **Ports**: every port a command uses is a `number` variable. A port other
    machines must reach also gets a `netbridge` entry with the same name and
    default (Quiver allocates and router-forwards it once Netbridge is active;
    in the current daemon it is switched off, so the variable is what runs).
    Never rely on a `netbridge`-only name in a command
    (`references/variables-and-dependencies.md` §5).
12. **Services**: `execute` starts the process in the foreground (no `&`, no
    daemonizing flags), `stop` is a `signal` step (`graceful`,
    `exit_on_failure: false`). All targets must agree on being a service. On
    Windows every `signal` is a forced kill (`taskkill /F`): give programs
    that need a clean shutdown an app-specific stop step there. Methods
    cannot run while the service runs, so declare them `available_in: [ready]`.
13. **Commands run in `sh -c` on Unix and `cmd.exe /C` on Windows** from the
    workdir. Windows commands use `.\prog.exe` and cmd syntax. `${NAME}` is
    Quiver's: write environment variables as `$VAR` (no braces) on Unix and
    `%VAR%` on Windows, since a braced `${VAR}` or `${#VAR}` is checked as a
    Quiver name. `elevated: true` has no effect in the current daemon.
14. **Dependency references** are `${<namespace without @ref>.<EXPORT>}` and
    must match an `exports` key the provider really declares; the validator
    does not check them, and a wrong one fails at run time with
    `bad substitution`.
15. **Do not write `metadata.generator`** (reserved for Quiver's own
    synthesized manifests) nor `type: dependencies` steps.
16. **Media are official or derived from official**: icon square, banner
    exactly 2:1, SVG preferred, raster only in high resolution (icon >= 512px,
    banner >= 1200x600). A generated banner embeds the unmodified official
    icon; no icon at all beats an invented one.

## Conventions seen in real arrows

- `metadata.name`: usually `owner.project` in lowercase (e.g. `junegunn.fzf`,
  `rabbytesoftware.appimage-runtime`); follow the collection's own convention
  when adding to one.
- `credits` for the upstream authors, `maintainers` for whoever maintains
  the arrow; both are lists of `{name, url?, email?}` objects.
- Downloads go to a hidden file in the workdir
  (`${INSTALL_PATH}/.<name>.download`, or `.<name>.download.msi` for an MSI,
  whose detection needs the extension), then unpack into `${INSTALL_PATH}/bin`
  (CLIs) or `${INSTALL_PATH}/<AppName>` (apps).
- Titles are short imperative phrases: "Download fzf", "Unpack fzf".
- Inside a collection, set `metadata.quiver` to the collection namespace.

## Files in this skill

| Path | Use it for |
|---|---|
| `references/manifest-reference.md` | Full field reference: targets, `base`, Overrideable, lifecycle, every step type, methods, `preinstalled` |
| `references/variables-and-dependencies.md` | Variables, built-ins, substitution, ports, `tools`/`services`, `exports` |
| `references/expose.md` | CLI and desktop registration, `auto`, per-OS behaviour |
| `references/publishing-and-collections.md` | Namespaces and refs, file locations, versioning, `collection@v0`, Fletcher |
| `references/media.md` | Icon and banner requirements, finding official assets, generating banners, hosting |
| `references/validation-and-testing.md` | Validator phases, error codes, script usage, sandbox, runtime gotchas, offline checklist |
| `assets/examples/*.yaml` | Validated and (except the GUI app) sandbox-installed examples of each shape |
| `assets/templates/` | Starting points for `ARROW.md` and `collection.yaml` |
| `scripts/quiver_arrow.py` | `validate`, `assets`, `checksum`, `media`, `banner`, `sandbox`, `bundle` (Python 3.9+, stdlib only) |
