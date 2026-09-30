# `expose`: CLI commands and desktop entries

Derived from quiver.core `docs/spec/manifests/v0/arrow.md` §7.4 and
`docs/spec/wizard.md` (Exposure), verified against quiver.core `develop` @
`0fba569` (2026-09-29).

`expose` declares what should appear on the user's system once the arrow is
installed. Quiver places the entries as the last steps of `install`/`update`
and removes them as the first step of `uninstall`. The manifest only states
intent; never write steps that create symlinks, `.desktop` files or shortcuts
yourself.

```yaml
targets:
  "*":
    expose:
      cli:
        - name: mytool
          path: ${INSTALL_PATH}/bin/mytool
      desktop:
        - name: MyApp
          path: auto
          icon: ${INSTALL_PATH}/icon.png
          categories: [Utility]
```

## Entry fields

| Field | Required | Rule |
|---|---|---|
| `name` | yes | `^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$`. Unique within its kind in one target (the same name may be used once in `cli` and once in `desktop`). |
| `path` | yes | `auto`, or starts with `${INSTALL_PATH}` or `${WORKDIR}`. No `..`. On macOS, a `desktop` path must end in `.app` unless it is `auto`. |
| `icon` | no | Empty, an `http(s)://` URL, or a workdir-anchored path with no `..`. Never `auto`. |
| `categories` | no | Free-form desktop menu categories (Linux `.desktop` `Categories=`). |

Violations fail validation with `invalid_name`, `invalid_path` or
`invalid_expose_icon`.

## What each kind does, per OS

| | macOS | Linux | Windows |
|---|---|---|---|
| `cli` | symlink in `~/.quiver/bin` | symlink in `~/.quiver/bin` | the folder of the `.exe` is appended to the user `Path`; the command is the executable's own name |
| `desktop` | the `.app` bundle is moved to `/Applications` (or `~/Applications`) | `.desktop` file in `~/.local/share/applications` | Start Menu shortcut under `Programs\Quiver\` |

- `~/.quiver/bin` is not on `PATH` until the user runs `quiver path setup`
  once (or `POST /v0/system/path`). Mention it when you expose CLI entries.
- A `cli` target file that is not executable is made executable (macOS/Linux).
  On Apple silicon an unsigned Mach-O outside a bundle is ad-hoc signed.
- On Windows a `cli` path must be an `.exe` inside the workdir.

## `path: auto`

Resolved against the installed workdir when the entries are applied:

- **cli**: scans executables in the workdir (4 levels, hidden dirs skipped).
  One -> it. Several -> those named like the repository or the entry `name`;
  else all at the shallowest depth. Each is exposed under **its own file
  name** (`.exe` stripped), not the entry's `name`.
- **desktop**: first source that yields candidates: the apps `portable`
  recorded in `${WORKDIR}/.quiver-apps.json`; else top-level `.app` bundles
  (macOS), `.AppImage` files (Linux) or `.exe` files (Windows); else (Linux,
  Windows) executables named like the repository or the entry. Several
  candidates -> the one named like the repository or the entry; otherwise
  refused as ambiguous.
- An `auto` entry that finds nothing is skipped silently. A spelled-out path
  that does not exist fails that entry (`target not found`).

Prefer an explicit path when you know it (a single binary you named with
`portable.name`). Use `auto` after `extract`/`portable` of a package whose
internal layout you have not inspected, and always for desktop apps produced
by `portable` (it reads the record `portable` wrote).

## Failure behaviour

Each entry is reported as its own step (`Expose cli mytool`). A refused entry
(`owned by <ns>`, `exists and is not managed by quiver`, `ambiguous auto
resolution`) fails **its step only, never the install**. Quiver never
overwrites an entry it did not create, so pick names that will not collide
with common system commands unless the arrow is meant to provide exactly that
command.

## Inheritance

`cli` and `desktop` follow `base:` rules: a child's list replaces the
parent's when declared (even `[]`), and is inherited when omitted.

## Testing caution

The sandbox in `scripts/quiver_arrow.py` isolates `~/.quiver` (including
`~/.quiver/bin`), but **desktop entries always go to the real system**
(Applications folder, `~/.local/share/applications`, Start Menu). The script
refuses to seed a manifest with `desktop` entries unless
`QUIVER_SANDBOX_ALLOW_DESKTOP=1` is set: ask the user first.
