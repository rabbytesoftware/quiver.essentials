Codex is OpenAI's coding agent. This arrow installs **Codex CLI**, the agent that runs in your terminal and works on the code in front of it, on every platform OpenAI builds it for, and the **Codex desktop app** where OpenAI ships one that Quiver can install: macOS on Apple silicon. OpenAI now ships its desktop app under the ChatGPT name (it holds both ChatGPT and Codex), so on those two platforms the app you get is called ChatGPT.

![Codex CLI in a terminal](https://raw.githubusercontent.com/openai/codex/rust-v0.160.1/.github/codex-cli-splash.png)

## Features

- **A coding agent in your terminal**: run `codex` in a project and describe what you want; Codex reads and edits files, runs commands and works through multi-step tasks, asking for approval before it acts according to your settings.
- **Sandboxed by default**: commands run inside an OS-level sandbox, and you choose how much Codex may do without asking.
- **Sign in with ChatGPT or an API key**: use the plan you already have, or OpenAI API credits.
- **The desktop app (macOS)**: run several chats and projects in parallel from one window, open and review files, and use the same Codex agent with a visual interface. Start it from the app menu, or with `codex app` on a machine that has it.
- **Self-contained**: the CLI is a native Rust program with its helper tools (such as `ripgrep`) bundled in its package, so it needs no Node.js.

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS, Apple silicon | Codex CLI (the `codex` command) and the ChatGPT desktop app, from OpenAI's current macOS disk image, as `ChatGPT.app` in Applications. The app requires macOS 13 or later. |
| macOS, Intel | Codex CLI only. OpenAI's desktop app is built for Apple silicon only. |
| Linux (x86_64 and ARM64) | Codex CLI only (OpenAI's static musl build, which runs on any distribution). OpenAI ships its Linux desktop app only as a `.deb`, which has no AppImage or tarball equivalent, so there is no Linux desktop app here. |
| Windows (x64 and ARM64) | Codex CLI only. OpenAI distributes the Windows desktop app through the Microsoft Store and as a MSIX at an address that always points at the newest build, which cannot be pinned and verified, so Quiver does not install it. |

Codex CLI is pinned to OpenAI's release 0.160.1 and verified against its SHA-256 checksum. The desktop app is different: OpenAI only offers it at addresses that always serve the newest build, so Quiver installs the current release and cannot checksum it (see below). Run `quiver path setup` once so your shell finds the `codex` command.

### Good to know

- **The desktop app download is not checksum-verified.** OpenAI replaces the file at its macOS download address with every release, so no fixed checksum can stay correct. Quiver fetches it over HTTPS from OpenAI's own servers and installs whatever the current release is.
- **Updates come through Quiver for the CLI.** Installing a newer release of this arrow replaces the pinned version.
- **The macOS desktop app updates itself** through its built-in updater, as it does when installed by hand.
- **Already have the app?** Quiver never replaces an app it did not install: if `ChatGPT.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.
- **The CLI is installed as a package** (the `codex` program plus its `codex-path` and `codex-resources` folders), so keep it in place: `codex` finds its helpers relative to itself.
- **Minimum hardware**: OpenAI publishes none for the CLI; the arrow asks for 4 GB of memory and 2 cores as a conservative estimate.

## License and trademarks

Codex CLI is open source software released by OpenAI under the [Apache License 2.0](https://github.com/openai/codex/blob/main/LICENSE). The desktop app is proprietary software by OpenAI, used under OpenAI's [terms](https://openai.com/policies/). This arrow only downloads OpenAI's official builds from OpenAI's servers and GitHub releases. OpenAI, ChatGPT and Codex are trademarks of OpenAI; the icon is the Codex app icon shipped inside OpenAI's own macOS build, unmodified, the banner is composed from that icon (unaltered), the abstract Codex artwork from [developers.openai.com/codex](https://developers.openai.com/codex) and the official terminal capture from the openai/codex repository, with the product name set in text, and the screenshot comes from the official [openai/codex repository](https://github.com/openai/codex).

```arrow
schema: "arrow@v0"

metadata:
  name: Codex
  description: OpenAI's Codex CLI coding agent and desktop app
  license: Apache-2.0 AND Proprietary
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://developers.openai.com/codex
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: OpenAI
      url: https://openai.com
  media:
    icon: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/codex/icon.png
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/codex/banner.png
  tags:
    - ai
    - cli
    - desktop
    - developer-tools

# Codex CLI rust-v0.160.1: the codex-package-<target> tarballs from the GitHub
# release (the layout OpenAI's own install scripts deploy: bin/codex plus the
# codex-path and codex-resources helpers), with the SHA-256 digests GitHub
# publishes. Linux uses the musl build, which runs on any distribution.
# Desktop app (shipped as "ChatGPT"): OpenAI rotates builds and only documents
# a rolling address (Codex.dmg), so that
# download carries no checksum on purpose (a pinned one would break at the next
# release). The CLI package tarballs are GitHub release assets and stay pinned.
# The Windows app is only offered as a Microsoft Store listing and an
# unversioned MSIX (ChatGPT-x64.msix), which is not installed. The Linux desktop
# app exists only as a .deb, which Quiver does not use. Intel macs have
# no desktop build. Requirements are estimates: OpenAI publishes none.
targets:
  "linux/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download Codex CLI
          url:
            linux/amd64: https://github.com/openai/codex/releases/download/rust-v0.160.1/codex-package-x86_64-unknown-linux-musl.tar.gz
            linux/arm64: https://github.com/openai/codex/releases/download/rust-v0.160.1/codex-package-aarch64-unknown-linux-musl.tar.gz
          checksum:
            linux/amd64: 340801565906a7028f6baaa9ab6853addaef221f0016a1417a7c1ffdd96c21f0
            linux/arm64: dff0954438fa455c2197ddb1f421d8d68625d98de610f76bedb6e5bc837ea35b
          to: ${INSTALL_PATH}/.codex.download
          timeout: 15m
        - type: extract
          title: Unpack Codex CLI
          from: ${INSTALL_PATH}/.codex.download
          to: ${INSTALL_PATH}/codex
          timeout: 5m
    expose:
      cli:
        - name: codex
          path: ${INSTALL_PATH}/codex/bin/codex

  # Apple silicon: CLI plus the desktop app (ChatGPT.app, macOS 13 or later).
  darwin/arm64:
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 4
    lifecycle:
      install:
        - type: fetch
          title: Download Codex CLI
          url: https://github.com/openai/codex/releases/download/rust-v0.160.1/codex-package-aarch64-apple-darwin.tar.gz
          checksum: f73527ee09c6db869acbb37b709866b339ea74ef91d2de255e9c74ec960c6314
          to: ${INSTALL_PATH}/.codex.download
          timeout: 15m
        - type: extract
          title: Unpack Codex CLI
          from: ${INSTALL_PATH}/.codex.download
          to: ${INSTALL_PATH}/codex
          timeout: 5m
        - type: fetch
          title: Download the Codex desktop app
          url: https://persistent.oaistatic.com/codex-app-prod/Codex.dmg
          to: ${INSTALL_PATH}/.codex-app.download
          timeout: 30m
        - type: portable
          title: Install the Codex desktop app
          from: ${INSTALL_PATH}/.codex-app.download
          to: ${INSTALL_PATH}/ChatGPT
          timeout: 15m
    expose:
      cli:
        - name: codex
          path: ${INSTALL_PATH}/codex/bin/codex
      desktop:
        - name: ChatGPT
          path: auto

  # Intel Macs: OpenAI builds the desktop app for Apple silicon only.
  darwin/amd64:
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download Codex CLI
          url: https://github.com/openai/codex/releases/download/rust-v0.160.1/codex-package-x86_64-apple-darwin.tar.gz
          checksum: a98f330c9b1652cef2edc7bc2ee4c47a0fe19fa098b686381be3c8842abf0ac0
          to: ${INSTALL_PATH}/.codex.download
          timeout: 15m
        - type: extract
          title: Unpack Codex CLI
          from: ${INSTALL_PATH}/.codex.download
          to: ${INSTALL_PATH}/codex
          timeout: 5m
    expose:
      cli:
        - name: codex
          path: ${INSTALL_PATH}/codex/bin/codex

  # Windows: CLI only (the desktop app has no pinnable download).
  "windows/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download Codex CLI
          url:
            windows/amd64: https://github.com/openai/codex/releases/download/rust-v0.160.1/codex-package-x86_64-pc-windows-msvc.tar.gz
            windows/arm64: https://github.com/openai/codex/releases/download/rust-v0.160.1/codex-package-aarch64-pc-windows-msvc.tar.gz
          checksum:
            windows/amd64: 25c6fe4e46d5bff939312fc46de67ace37561f6f1f89b409af63fd8cc6098425
            windows/arm64: 844e17c492175ec62f8c11890ed89ef208d3502d2c79622c3be9876d2755f085
          to: ${INSTALL_PATH}/.codex.download
          timeout: 15m
        - type: extract
          title: Unpack Codex CLI
          from: ${INSTALL_PATH}/.codex.download
          to: ${INSTALL_PATH}/codex
          timeout: 5m
    expose:
      cli:
        - name: codex
          path: ${INSTALL_PATH}/codex/bin/codex.exe
```
