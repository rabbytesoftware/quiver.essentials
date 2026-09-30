# arrow@v0 manifest reference

Derived from quiver.core `docs/spec/manifests/v0/arrow.md`, the translator's
JSON Schema (`internal/engine/manifold/translator/arrow/v0/schema.json`) and the
ruleset (`internal/engine/manifold/ruleset/arrow/`), verified against a running
daemon built from quiver.core `develop` @ `0fba569` (2026-09-29). Where the prose
spec and the code disagree, this file follows the code and says so.

## Contents

1. Top-level structure
2. Metadata
3. Targets: keys, selection, abstract targets
4. `base:` inheritance
5. Overrideable fields
6. Lifecycle hooks and pairing
7. Step types
8. `preinstalled`
9. Methods
10. Service vs package

---

## 1. Top-level structure

Unknown keys are rejected at every level (`additionalProperties: false`).

```yaml
schema: "arrow@v0"      # required, exactly this string (never the old `manifest:` key: the schema rejects it)
metadata: {...}         # required; `name` is required
variables: [...]        # optional, global (never inside a target)
netbridge: [...]        # optional, global
targets: {...}          # required, at least one concrete target
```

There is **no version field anywhere**. The git ref the manifest is read at is
the version (see `publishing-and-collections.md`). `metadata.version` is
tolerated and ignored; never write it.

A target:

```yaml
targets:
  <key>:
    base: <another key>          # optional, single parent
    requirements:                # optional, each integer >= 1
      cpu_cores: 1
      ram_gb: 1                  # the key is ram_gb (not memory_gb)
      disk_gb: 1
    tools: [namespace, ...]      # install-time dependencies
    services: [namespace, ...]   # dependencies that must run alongside
    exports: {name: value}       # static values for dependents
    expose: {cli: [...], desktop: [...]}
    lifecycle:
      install: [steps]
      update: [steps]
      execute: [steps]
      stop: [steps]
      uninstall: [steps]
      preinstalled: [steps]
    methods:
      <method-name>: {available_in: [ready|running], steps: [steps]}
```

## 2. Metadata

| Field | Required | Notes |
|---|---|---|
| `name` | yes | Non-empty, <= 255 chars. Convention in real arrows: `owner.project` (e.g. `junegunn.fzf`). |
| `description` | no | <= 1000 chars, one line. |
| `license` | no | SPDX identifier. |
| `url` | no | Homepage. |
| `quiver` | no | Namespace of the collection the arrow belongs to, when it ships in one. |
| `maintainers` | no | List of `{name, email?, url?}` objects (never bare strings). Whoever maintains the *arrow*. |
| `credits` | no | Same shape. Upstream authors of the software. |
| `media` | no | `{icon, banner}` URLs: a square icon and a 2:1 banner, SVG preferred. See `media.md`. |
| `tags` | no | Free-form strings. |
| `generator` | no | Written by Quiver's Fletcher on synthesized manifests. **Omit it in hand-written manifests**: its presence makes the arrow report `origin: inferred`. |

## 3. Targets

### Key forms

| Form | Example | Selected at runtime |
|---|---|---|
| Exact | `linux/amd64` | yes |
| Glob | `linux/*`, `*/arm64`, `*` | yes (`*` matches one path segment) |
| Abstract | `_common`, `_unix` | never; only reachable through `base:`, may omit `lifecycle` |

Concrete platforms Quiver knows: `linux/amd64`, `linux/arm64`, `windows/amd64`,
`windows/arm64`, `darwin/amd64`, `darwin/arm64`. Nothing else can match.

### Selection

For each concrete platform, the most specific matching non-abstract key wins:
exact (3) > one-wildcard glob like `linux/*` or `*/arm64` (2) > `*` (1).

- Two keys of **equal** specificity matching the same platform is a hard error:
  `ambiguous target for OS "linux/amd64": keys "linux/*" and "*/amd64" have equal specificity`.
- A platform no key matches is simply unsupported (not an error).
- If **no** platform compiles, the manifest fails with `no_supported_platform`.

The set of supported platforms is exactly the set of platforms that compile.
Claim only platforms the upstream really ships for. If upstream has no arm64
Linux build, do not write `linux/*`: write `linux/amd64`.

## 4. `base:` inheritance

A target inherits every field of its `base:` (one parent, no cycles, the
parent must exist: `cyclic_base` / `missing_base`). Merge rules:

| Field | Rule |
|---|---|
| `requirements` values | child non-zero wins; zero inherits |
| `tools`, `services` | child list replaces the parent's when present |
| `exports`, `methods` | merged key by key; child wins on the same key |
| lifecycle hooks | child list replaces the parent's when present; **`[]` is present** (an explicit empty hook), omitted means inherit |
| `expose.cli`, `expose.desktop` | child list replaces when present (even `[]`); omitted inherits |

A method inherited through `base:` cannot be partially overridden: redefining
it replaces all of its steps.

## 5. Overrideable fields

These step fields, and `exports` values, accept either a plain scalar or a map
keyed by platform:

| Step | Overrideable fields |
|---|---|
| `run` | `command`, `elevated`, `timeout` |
| `fetch` | `url`, `to`, `checksum`, `timeout` |
| `extract` | `from`, `to`, `timeout` |
| `portable` | `from`, `to`, `timeout` (NOT `name`) |
| `signal` | `signal`, `timeout` |

`type`, `title`, `exit_on_failure` and `portable.name` are never Overrideable.
`expose` entry fields are plain strings.

```yaml
url:
  linux/amd64: https://example.com/tool-linux-amd64.tar.gz
  linux/arm64: https://example.com/tool-linux-arm64.tar.gz
command:
  default: ./tool
  "windows/*": '.\tool.exe'
```

- **Keys**: `default`, `*`, or anything containing `/` (`linux/amd64`,
  `linux/*`, `*/arm64`). Bare OS names (`linux`, `windows`) are rejected.
- **Coverage** (`insufficient_coverage`): on every concrete target, each
  platform that target matches must be reached by a key or by a non-empty
  `default`. A `"*"` target with a `url` map therefore needs all six platform
  keys (or a `default`). Checked after `base:` inheritance, so maps inside an
  abstract base only need keys for the platforms its concrete children match.
- **Resolution**: once per platform at compile time, most specific key wins
  (exact > glob > `*`), `default` only when nothing matches. Two equally
  specific keys matching one platform (`"windows/*"` and `"*/amd64"` on
  `windows/amd64`) is an `AmbiguousTargetError`.

Quote keys that start with `*` (`"*"`, `"*/arm64"`, `"windows/*"` is fine
either way but quoting is harmless); YAML treats a leading `*` as an alias.

## 6. Lifecycle hooks and pairing

| Hook | Runs | Notes |
|---|---|---|
| `install` | on install | Quiver prepends a synthetic `dependencies` step (never write `type: dependencies`). |
| `uninstall` | on uninstall | See pairing. |
| `update` | on update | Optional, see "Updating" below. |
| `execute` | on run | Its presence makes the arrow a service (section 10). |
| `stop` | on stop | Requires `execute` (`stop requires execute to also be defined`). `execute` without `stop` is allowed (a program that exits on its own). |
| `preinstalled` | at add time | Detection probe, section 8. |

### Pairing rule (`missing_pair`)

`install` needs an `uninstall`, **unless every install step is a `fetch`,
`extract` or `portable` whose `to` is anchored in the workdir**: the value (and
every Overrideable variant of it) is exactly `${INSTALL_PATH}` or
`${WORKDIR}`, or starts with one of them followed by `/`, and contains no `..`
segment.

- `to: ${INSTALL_PATH}/bin` is anchored. `to: ./bin` is **not** (relative
  paths do land in the workdir at runtime, but the rule only accepts the
  literal prefix), and `${WORKDIR}x` is not.
- The spec prose lists only `fetch`/`extract`; the rule in
  `lifecycle_pairs.go` also accepts `portable`. Fletcher's own manifests rely
  on that.
- `uninstall` without `install` is always invalid.
- An empty list counts as absent: `install: []` + `uninstall: []` is fine.

Install-only is the preferred shape whenever it applies: nothing outside the
workdir needs undoing. As soon as `install` contains any other step (any
`run`, even one that only touches the workdir, or a `fetch`/`extract`/
`portable` whose `to` is not anchored), an `uninstall` is required; write
one that undoes what those steps did (it may be best-effort cleanup with
`exit_on_failure: false`).

### Updating

- **Without an `update` hook** (the usual case): `quiver update` reinstalls.
  It resolves the ref the arrow should move to (a recommended newer ref, the
  installed constraint, or the channel's latest), moves the catalog entry to
  that `namespace@ref`, runs **that** ref's `install` in a fresh workdir, and
  drops the old ref and its workdir **without** running the old `uninstall`.
  An arrow already at that ref is refused as up to date. The arrow's
  namespace changes (`...@v1.2.0` becomes `...@v1.3.0`).
- **With an `update` hook**: the hook runs in place, in the current workdir,
  from the **currently installed manifest**, and `${REF}` is the **current**
  ref. So an `update` that downloads `.../download/${REF}/...` fetches the
  release that is already installed. Only write an `update` hook for in-place
  work that does not need a newer manifest (migrating data, refreshing a
  cache), and never copy the install recipe into it.
- Synthesized (Fletcher) manifests never declare `update`.

### What uninstall and remove actually do

- `uninstall` runs the `uninstall` steps and removes the arrow's `expose`
  entries. It does **not** delete the workdir.
- Removing the arrow from the catalog (`DELETE /v0/arrow/{ns}`,
  `quiver arrow remove`) deletes the workdir.
- If install fails midway the workdir is removed; side effects outside it
  (a registered Windows service, files in system directories) are not rolled
  back. Put irreversible steps last.

## 7. Step types

Every step takes `type` (required), `title` (shown in the UI: always set it),
`timeout`, `exit_on_failure`.

- `timeout` must match `^\d+[sm]$`: `30s`, `5m`, `90m`. No hours, no
  fractions, no compound (`1h30m` is rejected, `1h` too).
- `exit_on_failure` defaults to `true`. Set `false` on best-effort cleanup
  (uninstall `rm` steps, `stop` signals).
- Paths in steps are relative to the workdir (every step runs with
  `${INSTALL_PATH}` as its working directory).

### `run`

```yaml
- type: run
  title: Configure
  command: ./tool --setup --flag ${MY_VAR}
  timeout: 2m
  elevated: false        # optional; accepted, but see below
```

Runs through `sh -c` on Unix and `cmd.exe /C` on Windows, with the ordinary
OS environment. **The timeout bounds the process itself**: when it expires the
process is killed and the step fails with `context deadline exceeded`. Never
put a `timeout` on a long-running `execute` step (a server, a GUI app that
stays open): it would be killed when the timeout expires. Verified on the
daemon: a server with `timeout: 10s` served requests at 5s and was gone at 17s.

`elevated` is part of the schema (meant for sudo/UAC) but the daemon at this
revision does not act on it: the command runs with the daemon's own
privileges either way. Do not rely on it; prefer installs that need no
elevation.

Substitution is textual: `${...}` values are pasted into the command before
the shell parses it, with no escaping (see `variables-and-dependencies.md` §3).

Prefer `extract`/`portable` over `run: tar -xzf ...` and over `chmod +x`:
they are cross-platform, safe against path traversal, and keep the install
eligible for install-only.

### `fetch`

```yaml
- type: fetch
  title: Download tool
  url: https://example.com/tool.tar.gz
  to: ${INSTALL_PATH}/.tool.download
  checksum: 3b1f...e9            # sha256, bare hex or "sha256:<hex>"
  timeout: 10m
```

`checksum` is a SHA-256 digest, case-insensitive, bare or prefixed `sha256:`.
Any other algorithm prefix is rejected. A mismatch deletes the file and fails
the step. Always set it; get it from the release's published digests
(`scripts/quiver_arrow.py assets owner/repo TAG`) or by hashing the file
(`scripts/quiver_arrow.py checksum URL`). Never invent one. A `${REF}`-templated
URL can carry one too: each tag's manifest holds that release's digest, which
means updating the checksum in the commit you tag (see
`publishing-and-collections.md` §3).

### `extract`

```yaml
- type: extract
  title: Unpack tool
  from: ${INSTALL_PATH}/.tool.download
  to: ${INSTALL_PATH}/bin
  timeout: 5m
```

Format detected from content, not extension: tar (plain, gz, xz, bz2, zst),
zip, or a single compressed file. `to` is created if missing. Refuses entries
escaping `to` (absolute paths, `../`, escaping symlinks). Preserves executable
bits. Capped by the daemon's `arrows.extract_max_bytes` (default 8 GiB) and
1,000,000 entries. **Refuses AppImages and DMGs**: use `portable` for those.

### `portable`

```yaml
- type: portable
  title: Install App
  from: ${INSTALL_PATH}/.app.download
  to: ${INSTALL_PATH}/App
  name: app            # optional; only used for a bare executable or single-file compressed payload
  timeout: 15m
```

Materializes an app package as a runnable app inside the workdir. Detects:

1. **AppImage (type 2)**: unpacked in pure Go (no FUSE, no root) into
   `<to>/<stem>`, plus a relocatable `.quiver-run` launcher. Type 1 AppImages
   are unsupported.
2. **DMG**: `darwin/*` targets only.
3. **MSI** (Windows installer package): Windows only, unpacked with an
   administrative `msiexec` extraction (no system-wide install). Detected only
   when `from` **ends in `.msi`** as well as having the MSI signature, so
   download it to e.g. `${INSTALL_PATH}/.tool.download.msi`, not to a bare
   `.download` name.
4. **Archive**: anything `extract` accepts, same rules.
5. **Bare executable** (ELF, Mach-O, PE): copied to `<to>/<name>` (or the
   file name of `from`) with mode 0755.
6. Anything else fails with `unknown format`.

`name` must match `^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$`, must not end in a dot
and must not be a Windows device name (`CON`, `NUL`, `COM1`, ...): rule
`invalid_name`. Because it is not Overrideable, give Windows its own target
when the executable needs `.exe`.

`portable` **owns** `to`, and replaces it wholesale on every later run so no
file from an older release survives, only when all of these hold: `from` and
`to` are both inside the workdir, `to` is a subdirectory (not the workdir
itself) and does not contain `from`, and `to` either does not exist yet or
carries the `.quiver-portable` marker naming this same `from` (relative to
the workdir). Otherwise it merges into `to` and older files can remain. So:
give each `portable` its own dedicated subdirectory, never create that
directory in an earlier step, and keep the download file name (`from`)
stable across releases of the manifest.

It also records what it installed in `${WORKDIR}/.quiver-apps.json`, which
`expose` with `path: auto` reads to find desktop apps. `from` is deleted
afterwards when it lives inside the workdir.

### `signal`

```yaml
- type: signal
  title: Stop server
  signal: graceful       # graceful | kill | interrupt
  timeout: 15s
  exit_on_failure: false
```

Targets the PID recorded by the running `execute`. On macOS/Linux `graceful`
= SIGTERM, `kill` = SIGKILL, `interrupt` = SIGINT. **On Windows all three are
`taskkill /F`**, a forced kill with no chance to clean up. The usual `stop`
hook is a single `graceful` signal with `exit_on_failure: false`; when a
Windows program must shut down cleanly (flush data, save a world), give the
Windows target a `stop` that asks it to exit through its own mechanism (a
CLI command, an admin API) before any `signal`.

## 8. `preinstalled`

Optional probe run at **add** time, before anything is installed: "is this
software already on the machine, put there by something else?" If every step
succeeds, the arrow lands directly in `ready` without running `install`. Any
failure just means "not detected".

- Bounded to 30 s in total, whatever the step timeouts say.
- Only `${ARROW_NAMESPACE}`, `${PLATFORM}`, `${REF}` and variables **with a
  default** are available; `${INSTALL_PATH}`/`${WORKDIR}` are not
  (`unresolved_variable`).
- A probe that cannot verify anything (no steps, an empty command) counts as
  not detected.

```yaml
preinstalled:
  - type: run
    title: Look for an existing install
    command: test -d /Applications/MyApp.app
    timeout: 5s
```

Use it only when a user may genuinely already have the software from another
installer, and make the check precise.

## 9. Methods

Custom actions a user can run on an installed arrow.

```yaml
methods:
  version:
    available_in: [ready]            # `ready` and `running` are the only valid values
    steps:
      - type: run
        title: Print version
        command: ./bin/tool --version
        timeout: 30s
```

Per target; a method on `linux/*` need not exist on `windows/*`. Use short
kebab-case names (`version`, `reset-config`); users invoke them as
`quiver <namespace> <method>`.

A method is an execution like any other: while it runs the arrow is
`running`, then it returns to `ready`. Quiver refuses to start any execution
while another is active, so **a method cannot run while the arrow's
`execute` (a service) is running**, whatever `available_in` says. In practice
`available_in: [ready]` is what works; listing `running` does not let a
method reach a live service.

## 10. Service vs package

An arrow is a **service** when its targets declare `execute`, a **package**
otherwise. All compiled targets must agree (`mixed_kind`). A target that
lists `services:` must itself define `execute` and `stop`
(rule `service_consumer_missing_lifecycle`).
