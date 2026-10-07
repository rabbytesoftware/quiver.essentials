Claude is Anthropic's AI assistant. This arrow installs it two ways at once: **Claude Code**, the coding agent that lives in your terminal, as the `claude` command on every platform Anthropic builds it for, and the **Claude desktop app** on macOS and Windows.

![Claude Code working in a terminal](https://raw.githubusercontent.com/anthropics/claude-code/v2.1.291/demo.gif)

## Features

- **Claude Code in your terminal**: describe a task in plain language and Claude reads your codebase, edits files, runs commands and works through multi-step changes, asking before it acts. Run `claude` in a project folder to start.
- **The Claude desktop app**: chat with Claude in a native window, with projects, files and connectors, and use Claude Code and Cowork from the same app (Cowork needs a paid plan).
- **One account everywhere**: sign in with your Claude account (or an Anthropic API key for the CLI) and your plan applies to both.
- **Native binaries**: the CLI is a single self-contained executable, so it needs no Node.js.

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | The `claude` command, and `Claude.app` in Applications from Anthropic's official build for your processor. Requires macOS 11 or later. |
| Linux (x86_64 and ARM64) | The `claude` command (glibc build) only. Anthropic ships the Linux desktop app only as a `.deb`, which has no AppImage or tarball equivalent, so there is no Linux desktop app here. |
| Windows (x64 and ARM64) | The `claude` command, and the Claude desktop app, unpacked from Anthropic's official update package into Quiver's folder with a Start Menu shortcut. Requires Windows 10 or later. |

Every download is pinned to an official Anthropic build (Claude Code 2.1.291, Claude desktop 2.19675.1) and verified against its SHA-256 checksum. Run `quiver path setup` once so your shell finds the `claude` command.

### Good to know

- **Pinned versions, updates through Quiver.** Claude Code can also update itself; to keep versions under Quiver's control set `DISABLE_AUTOUPDATER=1`. The desktop builds installed here are not wired to Anthropic's installers, so they do not update themselves: install a newer arrow release to move to a newer version.
- **Linux builds for musl systems (such as Alpine) are not covered.** Anthropic publishes separate musl CLI binaries; this arrow installs the glibc ones.
- **Windows desktop is the app's own update package, run in place.** Anthropic's usual Windows installer (and its MSIX) are not offered at a pinnable address, so Quiver unpacks the exact package the installer would deploy. It has not been tested here against every feature of the app; if something needs Windows app identity, install Anthropic's MSIX instead.
- **Already have Claude.app?** Quiver never replaces an app it did not install: if `Claude.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.
- **Minimum hardware**: Anthropic publishes no minimums for the CLI; the arrow asks for 4 GB of memory and 2 cores as a conservative estimate.

## License and trademarks

Claude Code and the Claude desktop app are proprietary software by Anthropic PBC, used under Anthropic's [terms](https://www.anthropic.com/legal/consumer-terms) and [commercial terms](https://www.anthropic.com/legal/commercial-terms). This arrow only downloads Anthropic's official builds from Anthropic's own servers. Claude and the Claude logo are trademarks of Anthropic PBC; the icon is the app icon shipped inside Anthropic's own macOS build, unmodified, the banner is the social-preview image Anthropic publishes for Claude on [anthropic.com/claude](https://www.anthropic.com/claude), cropped to 2:1 without scaling, and the screenshot is the demo recording in the official [claude-code repository](https://github.com/anthropics/claude-code).

```arrow
schema: "arrow@v0"

metadata:
  name: Claude
  description: Anthropic's Claude Code CLI and Claude desktop app
  license: Proprietary
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://claude.com
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Anthropic PBC
      url: https://www.anthropic.com
  media:
    icon: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/claude/icon.png
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/claude/banner.jpg
  tags:
    - ai
    - cli
    - desktop
    - developer-tools

# Claude Code 2.1.291: the versioned native binaries Anthropic publishes at
# downloads.claude.ai/claude-code-releases/<version>/<platform>/claude, with
# the SHA-256 from that release's manifest.json (the same file claude.ai/install.sh
# trusts). Claude desktop 2.19675.1: macOS zips and Windows Squirrel packages from
# downloads.claude.ai/releases; the macOS checksums were hashed from the files, the
# Windows ones from the nupkg (its SHA-1 matches Anthropic's
# RELEASES file). Anthropic does not delete old builds: checked 2026-10-06,
# when 2.26454.0 was already out, the pinned 2.19675.1 macOS zips and Windows
# nupkgs still downloaded, older nupkgs (2.7032.0) did too, and Claude Code binaries and manifests back to 1.0.100 remain.
# Anthropic's only floating desktop addresses sit behind a Cloudflare challenge
# that a downloader cannot pass, so pinning is the safe choice. Requirements are estimates: Anthropic
# publishes none for the CLI.
targets:
  # Linux: the glibc CLI binary only. Anthropic ships the Linux desktop app
  # only as a .deb, which Quiver does not unpack (no AppImage or tarball exists).
  "linux/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download Claude Code
          url:
            linux/amd64: https://downloads.claude.ai/claude-code-releases/2.1.291/linux-x64/claude
            linux/arm64: https://downloads.claude.ai/claude-code-releases/2.1.291/linux-arm64/claude
          checksum:
            linux/amd64: 078fad28d0297c9a25d306b635b2d8816c6839347520f29eb54ffea5d56142fb
            linux/arm64: c18473a04cc4f077435d5d9081f09ebea46e699eb2825cea64741c4bccb87647
          to: ${INSTALL_PATH}/.claude.download
          timeout: 15m
        - type: portable
          title: Install Claude Code
          from: ${INSTALL_PATH}/.claude.download
          to: ${INSTALL_PATH}/bin
          name: claude
          timeout: 5m
    expose:
      cli:
        - name: claude
          path: ${INSTALL_PATH}/bin/claude

  # macOS: native CLI binary per processor, plus Claude.app from Anthropic's
  # per-processor zip. `portable` records the app and moves it to Applications.
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 3
    lifecycle:
      install:
        - type: fetch
          title: Download Claude Code
          url:
            darwin/amd64: https://downloads.claude.ai/claude-code-releases/2.1.291/darwin-x64/claude
            darwin/arm64: https://downloads.claude.ai/claude-code-releases/2.1.291/darwin-arm64/claude
          checksum:
            darwin/amd64: 223bf4de0e8f38cb254fc38f82fda09f9fcfd4e2aac62b59ef7e7f1960a45ddd
            darwin/arm64: 9a1d2ed6bb4421e8fc80c892c0413f293be3ee50ae3d7dda1a7622197a056690
          to: ${INSTALL_PATH}/.claude.download
          timeout: 15m
        - type: portable
          title: Install Claude Code
          from: ${INSTALL_PATH}/.claude.download
          to: ${INSTALL_PATH}/bin
          name: claude
          timeout: 5m
        - type: fetch
          title: Download Claude desktop
          url:
            darwin/amd64: https://downloads.claude.ai/releases/darwin/x64/2.19675.1/Claude-8613680e2e16d90700c039e084a7883f321ed4e3.zip
            darwin/arm64: https://downloads.claude.ai/releases/darwin/arm64/2.19675.1/Claude-8613680e2e16d90700c039e084a7883f321ed4e3.zip
          checksum:
            darwin/amd64: ddab912dfa679ceea9aecf5aa3e3a27d7b2ecdbf407544ed6500825f3d96fbbe
            darwin/arm64: e074f25fc97fa2e0985e22c3ce562a95a9b79c8a62d60c9798e35d1b9f98e9db
          to: ${INSTALL_PATH}/.claude-desktop.download
          timeout: 20m
        - type: portable
          title: Install Claude desktop
          from: ${INSTALL_PATH}/.claude-desktop.download
          to: ${INSTALL_PATH}/Claude
          timeout: 10m
    expose:
      cli:
        - name: claude
          path: ${INSTALL_PATH}/bin/claude
      desktop:
        - name: Claude
          path: auto

  # Windows: native CLI executable, plus the desktop app from the Squirrel
  # full package (a zip) that Anthropic's own installer deploys, unpacked
  # in place: no installer runs and nothing is written outside the workdir.
  # The CLI folder (bin) goes on the user's Path; the app gets a Start Menu
  # shortcut.
  "windows/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 3
    lifecycle:
      install:
        - type: fetch
          title: Download Claude Code
          url:
            windows/amd64: https://downloads.claude.ai/claude-code-releases/2.1.291/win32-x64/claude.exe
            windows/arm64: https://downloads.claude.ai/claude-code-releases/2.1.291/win32-arm64/claude.exe
          checksum:
            windows/amd64: 70052a17e06561a4563597f79570e81ccc0772474c3c6ac522aa5ccc71773013
            windows/arm64: fb1b35e6d1a91e45478cc6bd4e5ae7138dd00c3f79df339b7ab1fbbbbaf69bc0
          to: ${INSTALL_PATH}/.claude.download
          timeout: 15m
        - type: portable
          title: Install Claude Code
          from: ${INSTALL_PATH}/.claude.download
          to: ${INSTALL_PATH}/bin
          name: claude.exe
          timeout: 5m
        - type: fetch
          title: Download Claude desktop
          url:
            windows/amd64: https://downloads.claude.ai/releases/win32/x64/AnthropicClaude-2.19675.1-full.nupkg
            windows/arm64: https://downloads.claude.ai/releases/win32/arm64/AnthropicClaude-2.19675.1-full.nupkg
          checksum:
            windows/amd64: 4cbd3b28c44c8c72ea3b0ced874b8cec3920317c77991bfe5d59c62b000d2ec4
            windows/arm64: 4119c007a13caac1fc80a2da36e0ed28bb90117feaf4a2c9f33e92faa878b868
          to: ${INSTALL_PATH}/.claude-desktop.download
          timeout: 20m
        - type: extract
          title: Unpack Claude desktop
          from: ${INSTALL_PATH}/.claude-desktop.download
          to: ${INSTALL_PATH}/desktop
          timeout: 10m
    expose:
      cli:
        - name: claude
          path: ${INSTALL_PATH}/bin/claude.exe
      desktop:
        - name: Claude
          path: ${INSTALL_PATH}/desktop/lib/net45/claude.exe
```
