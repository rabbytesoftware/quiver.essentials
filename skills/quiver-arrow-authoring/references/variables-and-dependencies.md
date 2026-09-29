# Variables, ports and dependencies

Derived from quiver.core `docs/spec/manifests/v0/arrow.md` §7, §10, §11,
`versioning.md`, and the runtime assembler
(`internal/app/repositories/runtime/internal/assembler/internal/variables.go`),
verified against quiver.core `develop` @ `0fba569` (2026-09-29).

## Contents

1. User variables
2. Built-in variables
3. How `${...}` substitution works
4. Resolution order
5. Ports
6. Dependencies: `tools` and `services`
7. `exports` and `${namespace.NAME}`

---

## 1. User variables

Top-level, global to every target: the form a user fills in.

```yaml
variables:
  - name: MAX_PLAYERS
    type: number          # string | number | boolean | select (default: string)
    default: "16"         # ALWAYS a YAML string: quote numbers and booleans
    min: 1
    max: 128
    description: Maximum concurrent players
  - name: MODE
    type: select
    default: "fast"
    values: ["fast", "safe"]   # required for select; default must be one of them
  - name: API_KEY
    type: string
    sensitive: true            # UI hint only (masked input), not a security boundary
    description: API key for the provider
```

Rules (`variables` rule, `invalid_variable` / `duplicate_name` /
`missing_values`): unique non-empty names <= 255 chars, `select` needs
`values` and its `default` must be one of them, `min <= max`.

**A variable with no default is required** whenever a step of the method
being run references it: the run is refused with `required variable not
provided` until the caller passes it. `default: ""` counts as no default.
Such values are not carried over from a previous run either: the caller must
pass them every time. Give sensible defaults unless the user truly must
choose (an API key).

Not every method can receive values, so keep no-default variables out of the
steps that cannot:

- **`stop`**: the daemon ignores variables sent with a stop request. A
  no-default variable referenced in `stop` makes every stop fail.
- **`uninstall`** and **`update`**: Quiver Desktop starts them without asking
  for values (and the helper's `sandbox remove` uninstalls with none). A
  no-default variable there blocks uninstalling or updating from the app.

Only `install`, `execute` and custom methods are started with a form the user
fills in.

Names: use `UPPER_SNAKE_CASE`. The built-in names below are reserved; a user
cannot override them.

## 2. Built-in variables

| Variable | Value |
|---|---|
| `${INSTALL_PATH}` | The arrow's workdir (its own directory under `~/.quiver/namespaces/...`) |
| `${WORKDIR}` | Same path as `INSTALL_PATH` |
| `${ARROW_NAMESPACE}` | The full `namespace@ref` |
| `${PLATFORM}` | `GOOS/GOARCH`, e.g. `linux/amd64` |
| `${REF}` | The git ref the manifest was read at, verbatim (e.g. `v1.2.0`, `main`) |

There is no `${VERSION}`: use `${REF}` (see `publishing-and-collections.md`).
`preinstalled` steps only get `ARROW_NAMESPACE`, `PLATFORM`, `REF` and user
variables that have a default.

## 3. How `${...}` substitution works

Quiver replaces `${NAME}` in step fields right before the step runs, on the
raw string, in one pass. The shell only ever sees final values.

- `${NAME}` Quiver resolved -> replaced.
- `${NAME}` Quiver did not resolve -> **left verbatim**. A plain name then
  reaches `sh` as an environment variable and usually expands to empty; a
  dependency reference like `${github.com/owner/repo.BIN}` makes `sh` abort
  with `bad substitution`, and `cmd.exe` passes it through literally. The
  validator catches unknown plain names (`unresolved_variable`) but not
  `${namespace.NAME}` references, so check those by hand.
- Other `$` forms belong to the shell and pass through untouched: `$HOME`,
  `$1`, `$(cmd)`, `${VAR:-default}`, `\$`. **Exception:** any `${...}` whose
  body has no `.` or `:` is checked as a Quiver name, so shell forms such as
  `${#VAR}` or `${VAR}` for an environment variable fail validation with
  `unresolved_variable`. Write `$VAR` (no braces) for environment variables.
- Substitution is plain text pasted into the command **before** the shell
  parses it, with no escaping. A value containing a space, quote, `;`, `&`
  or `$( )` becomes shell syntax, even inside double quotes (`"${ROOT}"`
  with `ROOT=$(rm -rf ~)` runs it). Quote values that may contain spaces, and
  constrain free-text variables that reach a command: prefer `select` or
  `number` types, and never pass a `sensitive` value through a command line
  that other users can see in the process list.
- Quiver's variables are **not** exported to the process environment. A
  program that needs one must receive it on its command line.
- A `${...}` inside a variable's *value* is not expanded again (single pass).
- On Windows the command goes to `cmd.exe /C`: use `%VAR%` for environment
  variables there, and quote paths with spaces normally.

## 4. Resolution order

Later layers win:

1. Built-ins
2. Dependency values (`${ns.INSTALL_PATH}`, `${ns.EXPORT}`)
3. User variable defaults
4. Netbridge ports (switched off in the current daemon; see section 5)
5. Values from the arrow's previous run (only for variables that have a default)
6. Values the user passes for this run

## 5. Ports

Additional sources: quiver.core `docs/spec/netbridge.md`,
`internal/engine/netbridge/netbridge.go`.

### What `netbridge` is for

`netbridge:` declares the ports a **server** listens on:

```yaml
netbridge:
  - name: GAME_PORT
    protocol: tcp            # tcp | udp | tcp/udp
    default: 27015           # preferred port, integer 1..65535
    required: true           # fail the run if no port can be had
```

As designed, when a method runs Quiver's Netbridge engine takes the preferred
port if it is free (otherwise one from the ephemeral range, 49152–65535),
asks the router to forward it to this machine (UPnP / NAT-PMP, best effort,
switchable with the daemon's `netbridge.enabled`), and binds the number to
`${GAME_PORT}`. It is how a game server or any service meant to be reached
from other machines gets a free port that is actually reachable.

### Current daemon behaviour

In quiver.core @ `0fba569` this is deliberately switched off: the runtime
does not call Netbridge, so nothing is allocated or forwarded and
`${GAME_PORT}` is **not substituted**. The validator accepts it; at run time
it reaches the shell verbatim, expands to empty, and the program starts
without its port. Verified on a running daemon.

### What to write

Give every port a `number` variable, so the arrow works today. When the port
is one other machines must reach (game servers, services with `0.0.0.0`
binds), also declare a `netbridge` entry **with the same name**:

```yaml
variables:
  - name: GAME_PORT
    type: number
    default: "27015"
    min: 1024
    max: 65535
    description: Port the server listens on

netbridge:
  - name: GAME_PORT
    protocol: tcp/udp
    default: 27015
    required: true
```

```yaml
command: ./server --port ${GAME_PORT}
```

With the resolution order in section 4, the variable default (layer 3) is
what runs today; once Netbridge is active its allocation (layer 4) replaces
that default and the port is forwarded, with no change to the manifest; a
value the user passes (layer 6) wins either way. The validator accepts the
shared name. Keep the two `default`s equal.

For a port that only this machine uses (a local web UI bound to
`127.0.0.1`), the variable alone is enough: router forwarding would only
expose it.

## 6. Dependencies: `tools` and `services`

Per target, lists of namespaces (see `publishing-and-collections.md` for
namespace and ref syntax).

```yaml
targets:
  "linux/*":
    tools:
      - github.com/rabbytesoftware/quiver.essentials/appimage-runtime   # latest stable
      - github.com/valve/steamcmd@v1.2.3                                  # exact ref
      - github.com/valve/steamcmd@v1.*                                    # glob, resolved against tags
    services:
      - github.com/owner/app/database@v2.*
```

- `tools`: installed before this arrow installs; never started or stopped by
  it. Use them for helpers, runtimes, libraries.
- `services`: must be running alongside this arrow; implies installation.
  A target with `services` must define `execute` and `stop`.
- The same namespace must not be in both lists (`tools_services_overlap`).
- Dependencies are installed transitively, in topological order, each as its
  own arrow (`namespace@ref`). Two versions of one dependency coexist.
- Validation does not check that a dependency exists or exports what you
  reference; a sandbox install does.

## 7. `exports` and `${namespace.NAME}`

A dependency publishes stable values; dependents read them instead of
guessing file layouts.

Provider:

```yaml
targets:
  "linux/*":
    exports:
      extract: ./appimage-extract.sh          # relative to the provider's workdir
      python: /usr/bin/python3                # absolute: passed through
```

Consumer:

```yaml
targets:
  "linux/*":
    tools:
      - github.com/rabbytesoftware/quiver.essentials/appimage-runtime
    lifecycle:
      install:
        - type: run
          title: Extract the AppImage
          command: ${github.com/rabbytesoftware/quiver.essentials/appimage-runtime.extract} ./app.AppImage
          timeout: 1m
```

Rules, as the runtime implements them:

- The reference key is the dependency's namespace **without its `@ref`**, a
  dot, then the export name: `${github.com/owner/repo.NAME}` even when the
  `tools` entry pins `@v1.2.3`.
- `${github.com/owner/repo.INSTALL_PATH}` is always available for a
  dependency, with or without `exports`.
- An export value starting with `./` is joined to the provider's workdir.
  Any other relative value is passed as written; absolute values pass through.
- Export values are static: no `${...}` inside them (`export_var_interpolation`).
  They are Overrideable, so they can differ per platform:

  ```yaml
  exports:
    bin:
      default: ./bin/tool
      "windows/*": ./bin/tool.exe
  ```

- The provider's export is read from its target for the same platform; a
  provider that does not support the platform contributes nothing.
