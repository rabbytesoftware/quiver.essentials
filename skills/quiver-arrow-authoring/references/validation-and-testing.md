# Validation and testing

Derived from quiver.core's ruleset (`internal/engine/manifold/ruleset/`),
`docs/spec/http-api.md`, and runs against a daemon built from quiver.core
`develop` @ `0fba569` (2026-09-29).

## Contents

1. The validator and its phases
2. Rule codes and how to fix them
3. `scripts/quiver_arrow.py`
4. Sandbox test installs
5. Behaviours validation does not catch
6. Checklist when no daemon is available

---

## 1. The validator and its phases

A quiver.core daemon validates without registering anything:

```
POST /v0/arrow/{ns}/manifest/validate        body: the raw ARROW.md or YAML
POST /v0/collection/{ns}/manifest/validate   body: the raw COLLECTION.md or YAML
```

`{ns}` must be URL-encoded (`/` -> `%2F`, `@` -> `%40`) and well-formed; its
value does not affect arrow validation. Response `data`:
`{valid, errors: [{field, rule, message}], supported_platforms, unsupported_platforms}`
(HTTP 200 when valid, 422 when not).

Validation stops at the first failing phase, so **fixing errors can reveal
new ones**. Loop until `valid: true`:

1. **Parse + schema + precompile rules**: YAML syntax, unknown keys,
   metadata, variables, netbridge, `base` integrity, Overrideable keys and
   coverage.
2. **Target selection**: ambiguous targets surface here as one
   `parse_error`.
3. **Compiled rules**, per platform: pairing, timeouts, variable references,
   expose, portable names, service rules. Each error is repeated once per
   platform it affects (`targets[linux/amd64]...`, `targets[linux/arm64]...`).

Also read `supported_platforms` when it is valid: it must be exactly the set
the upstream really ships for.

## 2. Rule codes and how to fix them

| `rule` | Typical cause | Fix |
|---|---|---|
| `parse_error` | YAML syntax; unknown key; wrong type; missing `targets:` (pre-refactor shape); ambiguous targets | Read the message: it names the line, key or the two ambiguous target keys |
| `required` | `metadata.name` missing | Add it |
| `max_length` | name > 255 or description > 1000 chars | Shorten |
| `invalid_variable` | select `default` not in `values`; `min > max`; bad name | Fix the variable |
| `missing_values` | `type: select` without `values` | Add `values` |
| `invalid_port` | netbridge name/protocol/port out of range | `protocol` tcp/udp/tcp/udp, port 1..65535 |
| `cyclic_base` / `missing_base` | `base:` loop or unknown parent | Point `base` at an existing target, no cycles |
| `invalid_overrideable_key` | a key like `linux` or `windows` | Use `linux/*`, `linux/amd64`, `*` or `default` |
| `insufficient_coverage` | Overrideable map has no `default` and misses a platform its target matches | Add the missing platform key, a `default`, or narrow the target key |
| `no_supported_platform` | no target matches any known platform | Use real `GOOS/GOARCH` keys or globs |
| `missing_pair` | `install` without `uninstall` whose steps are not all workdir-anchored fetch/extract/portable; `uninstall` without `install`; `stop` without `execute` | Anchor every `to` with `${INSTALL_PATH}/...` (preferred), or add an `uninstall` |
| `invalid_timeout` | `1h`, `1.5m`, `1m30s` | `^\d+[sm]$`: `90m`, `30s` |
| `unresolved_variable` | `${NAME}` that is not a built-in, variable or netbridge port; or a probe-restricted name in `preinstalled` | Declare the variable, fix the typo, or use the shell's own `$VAR` form on purpose |
| `export_var_interpolation` | `${...}` inside an `exports` value | Exports are static strings |
| `tools_services_overlap` | same namespace in `tools` and `services` | Keep it in one |
| `service_consumer_missing_lifecycle` | target has `services:` but no `execute`/`stop` | Add both |
| `mixed_kind` | some targets have `execute`, others don't | Make them all services or all packages |
| `invalid_state` | `available_in` value other than `ready`/`running` | Use those two only |
| `no_dependencies_step` | `type: dependencies` written by hand | Remove it; Quiver injects it |
| `invalid_name` | expose entry `name` or `portable.name` fails `^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$` / Windows device name / trailing dot | Rename |
| `invalid_path` / `path_traversal` | expose `path` not `auto` and not starting with `${INSTALL_PATH}`/`${WORKDIR}`, or containing `..` | Anchor it, or use `auto` |
| `invalid_desktop_path` | macOS desktop `path` not ending in `.app` | Point at the bundle, or `auto` |
| `invalid_expose_icon` | icon not empty/http(s)/anchored | Fix the icon value |
| `duplicate_name` | two expose entries of one kind share a name; two variables share a name | Rename |
| Collection: `required_field`, `exclusive_fields`, `auid_with_namespace`, `invalid_auid`, `invalid_path`, `duplicate_namespace` | entry shape problems | See `publishing-and-collections.md` §4 |

## 3. `scripts/quiver_arrow.py`

Python 3.9+, standard library only. `SKILL_DIR` below is the directory that
contains `SKILL.md` (wherever the skill was installed). Always call the
script by that path, and pass manifest paths as usual, relative to where you
are working:

```sh
python3 "$SKILL_DIR/scripts/quiver_arrow.py" validate path/to/arrow.yaml [more files...]
python3 "$SKILL_DIR/scripts/quiver_arrow.py" validate --collection collection.yaml
python3 "$SKILL_DIR/scripts/quiver_arrow.py" assets owner/repo [TAG]   # release assets + sha256 (GitHub)
python3 "$SKILL_DIR/scripts/quiver_arrow.py" checksum https://...      # download and hash any URL
```

- Which daemon it talks to: `QUIVER_API=http(s)://host:port` (a TCP daemon;
  those require a device token, passed as `QUIVER_TOKEN`), else
  `QUIVER_SOCKET=/path/to.sock`, else the local daemon at
  `~/.quiver/quiver.sock` (running whenever Quiver Desktop or `quiver` is).
  Local daemons on **Windows** listen on a named pipe, which the script does
  not speak: there, validate against a TCP daemon, or fall back to section 6.
- Exit codes: `0` ok, `1` invalid manifest / failed run, `2` environment
  problem (daemon unreachable, unauthorized, network, missing binary, file
  errors). On `2`, fix the environment or fall back to section 6; do not
  report the manifest as valid.
- `assets` needs network access to `api.github.com`; set `GITHUB_TOKEN` when
  rate-limited. It prints `sha256` only when GitHub recorded a digest for the
  asset; otherwise use `checksum URL`.
- Validating does not need the software's platform: any daemon validates
  every target.

## 4. Sandbox test installs

Validation proves the manifest is well-formed, not that it installs. When
the machine can run one of the arrow's platforms and a `quiver` binary is
available, test the real thing in an isolated daemon (its own
`QUIVER_HOME`, never the user's `~/.quiver`):

```sh
Q="$SKILL_DIR/scripts/quiver_arrow.py"
python3 "$Q" sandbox up
python3 "$Q" sandbox seed github.com/owner/repo@v1.2.3 arrow.yaml
python3 "$Q" sandbox install github.com/owner/repo@v1.2.3 [KEY=VALUE ...]
python3 "$Q" sandbox run github.com/owner/repo@v1.2.3 <method> [KEY=VALUE ...]
python3 "$Q" sandbox execute github.com/owner/repo@v1.2.3 [KEY=VALUE ...]
python3 "$Q" sandbox stop github.com/owner/repo@v1.2.3
python3 "$Q" sandbox status github.com/owner/repo@v1.2.3
python3 "$Q" sandbox remove github.com/owner/repo@v1.2.3   # stop + uninstall + remove + delete workdir
python3 "$Q" sandbox down
```

- Needs macOS or Linux (Unix socket). Binary lookup: `QUIVER_BIN`, else
  `quiver` on `PATH`, else `~/.quiver/self/quiver`.
- Data: `QUIVER_SANDBOX_DIR` (default `<tmp>/quiver-arrow-sandbox`); each
  sandbox directory gets its own daemon and socket. CLI entries land in
  `<that>/home/bin`, so you can run them from there.
- `seed` needs an explicit `@ref` and validates first.
- Each lifecycle command waits for **its own** run to finish and exits `0`
  only if that run succeeded. `install` on an already installed arrow prints
  "nothing to do". `execute` returns as soon as the service has been running
  for a few seconds (exit `0`): probe it (e.g. `curl` its port), check
  `sandbox status`, then `sandbox stop`. `stop` takes no variables (the daemon
  ignores them). An `update` that reinstalls moves the arrow to a new
  `@ref`; the command follows it and prints the new namespace.
- Methods and `update` are refused while the service is running; stop it first.
- Desktop entries are not sandboxed (see `expose.md`). `install`/`update`
  refuse, unless `QUIVER_SANDBOX_ALLOW_DESKTOP=1`, any arrow whose compiled
  manifest declares desktop entries **or** has dependencies (whose entries
  cannot be checked in advance). Set it only with the user's consent.
- Step errors show the failing step and exit code, not the program's output.
  To debug a failing `run` step, run the same command by hand inside
  `<sandbox>/home/namespaces/<domain>/<user>/<repo>@<ref>/`.

## 5. Behaviours validation does not catch

Verified on quiver.core `0fba569`; recheck when the core version changes.

- **`timeout` on `execute` kills the service.** The run step's timeout
  bounds the process. Leave `execute` run steps without `timeout`.
- **`netbridge` is switched off in the current daemon.** A `${NAME}` that
  only a `netbridge` entry declares validates, but reaches the shell
  unsubstituted. Declare every port as a `number` variable too (see
  `variables-and-dependencies.md` §5).
- **Unresolved `${ns.NAME}` dependency references** pass validation and reach
  the shell verbatim, where `sh` fails with `bad substitution`. Double-check
  the namespace spelling (no `@ref`) and that the provider really exports that
  name for the platform.
- **`signal` on Windows is always a forced kill** (`taskkill /F`), and
  **`elevated` has no effect**; see `manifest-reference.md` §7.
- **Removing an arrow without uninstalling it** leaves its `~/.quiver/bin`
  links dangling. Uninstall first (`sandbox remove` does).
- **Uninstall keeps the workdir**; only removal deletes it.
- **Wrong checksum or dead URL** only fails at install. Take both from the
  release itself (`assets` / `checksum`), never from memory.
- **Commands that differ per OS** (`./tool` vs `.\tool.exe`, `rm` vs `del`)
  validate either way; make sure each platform's command is right for its
  shell (`sh` vs `cmd.exe`).

## 6. Checklist when no daemon is available

When nothing can run the validator (a chat assistant without tools, no
`quiver` installed), check by hand and **say the manifest is unvalidated**:

- [ ] `schema: "arrow@v0"`; `metadata.name` set; no `version:`; no unknown keys.
- [ ] Every target key is exact, a glob with `/`, `*`, or `_abstract`; no two
      equally specific keys match one platform.
- [ ] Claimed platforms = platforms upstream actually ships.
- [ ] Every Overrideable map covers every platform its target matches, or has
      `default`; keys are `default`, `*` or contain `/`.
- [ ] Every step has `title` and a `timeout` matching `^\d+[sm]$`, except
      long-running `execute` steps, which have none.
- [ ] `install` without `uninstall` only if all steps are fetch/extract/portable
      with `to` starting `${INSTALL_PATH}/`; any `run` in install means an
      `uninstall` is required.
- [ ] No `update` hook that re-downloads via `${REF}` (it would fetch the
      installed release again); usually no `update` hook at all.
- [ ] No no-default variable referenced in `stop`, `uninstall` or `update`.
- [ ] Environment variables written `$VAR` / `%VAR%`, never `${VAR}` or
      `${#VAR}` (those are checked as Quiver names).
- [ ] An MSI download's `to` ends in `.msi`.
- [ ] Methods use `available_in: [ready]` on services.
- [ ] Delivered as `ARROW.md` / `<path>.md` with a readme: prose before the
      ```arrow fence, at least one screenshot with an absolute https URL, no
      `<iframe>`/`<script>`, platform notes matching the manifest.
- [ ] `stop` only with `execute`; services use a `signal` stop.
- [ ] Every `${NAME}` is a built-in, a declared variable, or intentional shell
      syntax; variable defaults are quoted strings; select defaults are in
      `values`.
- [ ] Checksums copied from the release, bare hex or `sha256:`-prefixed.
- [ ] `portable.name` has no `.exe` in a target that also serves Unix.
- [ ] Expose names match `^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$`; paths are `auto`
      or start with `${INSTALL_PATH}`; macOS desktop paths end in `.app`.
- [ ] Windows commands use `.\` and `cmd.exe` syntax.
