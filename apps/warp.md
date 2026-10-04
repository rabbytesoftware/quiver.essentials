Warp is a terminal built for working alongside AI agents. It runs your usual shell (zsh, bash, fish or PowerShell), and around it adds an editor-like input, command output grouped into blocks, and a built-in coding agent you can ask for a command, a fix or a whole change, then watch, steer and review. You can also bring your own CLI agent, such as Claude Code, Codex or Gemini CLI.

![Warp with an agent conversation next to a code review](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/warp/screenshots/agent-and-code-review.jpg)

## Features

- **Agents in the terminal**: describe what you want in natural language; Warp's agent runs commands and edits code while you watch and steer it.
- **Code review and editing**: review an agent's changes, leave comments and send them back for refinement, and edit files without leaving Warp.
- **Blocks**: each command and its output form one block you can copy, share or search.
- **A modern input editor**: multi-line editing, selections and completions where you type commands.
- **Vertical tabs**: tabs that show their git branch, worktree and pull request.
- **Privacy controls**: secret redaction with your own patterns, and command allow and deny lists for the agent.

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | Warp's official universal DMG, as `Warp.app` in Applications. Requires macOS 10.14 or later and hardware that supports Metal. |
| Linux (x86_64 and ARM64) | Warp's official AppImage, unpacked into Quiver's folder, and a desktop menu entry. Requires glibc 2.31 or later and OpenGL ES 3.0+ or Vulkan. |
| Windows (x64 and ARM64) | Warp's official installer, run silently for your user. It adds its own Start Menu shortcut. Requires Windows 10 version 1903 or later. |

Every download is pinned to one official Warp release and verified against its SHA-256 checksum before it runs.

### Good to know

- **An account is optional.** Warp offers to create one on first launch; you can skip it. Features that need the internet, such as AI, are unavailable without a connection.
- **On macOS and Windows, Warp keeps itself up to date.** Quiver installs the release pinned here; from then on Warp's own updater installs new versions. On Linux, Quiver unpacks the AppImage, so update Warp through Quiver.
- **On Windows, Warp installs into your user profile**, not into Quiver's folder, and needs the Microsoft Visual C++ 2015 (or later) Redistributable. Uninstalling through Quiver runs Warp's own uninstaller.
- **Your settings live outside Quiver's folder** (on Windows, in `%APPDATA%\warp`), so uninstalling keeps them.
- **Already have Warp?** Quiver never replaces an app it did not install. If `Warp.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.

## License and trademarks

Warp's client is open source: its UI framework is released under the [MIT License](https://github.com/warpdotdev/warp/blob/master/LICENSE-MIT) and the rest under the [GNU AGPL v3](https://github.com/warpdotdev/warp/blob/master/LICENSE-AGPL), by Denver Technologies, Inc. (Warp). This arrow only downloads Warp's official builds from Warp's own servers. The Warp name and logo are trademarks of Warp; the icon comes from Warp's [brand assets](https://github.com/warpdotdev/brand-assets), the banner was generated from it, and the screenshot comes from the [Warp repository](https://github.com/warpdotdev/warp).

```arrow
schema: "arrow@v0"

metadata:
  name: Warp
  description: The terminal for working with AI agents
  license: AGPL-3.0
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://www.warp.dev
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Warp
      url: https://www.warp.dev
  media:
    icon: https://raw.githubusercontent.com/warpdotdev/brand-assets/22c8994a3efd8631638b96685d98acb445b0ca9b/Logos/Warp-App-Icon.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/warp/banner.svg
  tags:
    - terminal
    - developer-tools
    - desktop

# Every file comes from one release directory on releases.warp.dev
# (v0.2026.09.30.08.29.stable_01); the Windows digests match Warp's WinGet
# manifest for that release. Requirements are conservative estimates: Warp
# publishes OS and graphics requirements but no hardware minimums.
targets:
  # Warp's type-2 AppImages, unpacked in place by `portable`. Warp's updater
  # cannot replace an unpacked AppImage: new releases come from a newer arrow.
  "linux/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download Warp
          url:
            linux/amd64: https://releases.warp.dev/stable/v0.2026.09.30.08.29.stable_01/Warp-x86_64.AppImage
            linux/arm64: https://releases.warp.dev/stable/v0.2026.09.30.08.29.stable_01/Warp-aarch64.AppImage
          checksum:
            linux/amd64: 7ec2b8aec662eda14ba3f5bd5f9f4365d8aca9ed08232cc27c0832660af02458
            linux/arm64: 9cc95cffac199b2168c4ca0c7ee4af995499f4bb508680565a6269cf1df2e060
          to: ${INSTALL_PATH}/.warp.download
          timeout: 15m
        - type: portable
          title: Install Warp
          from: ${INSTALL_PATH}/.warp.download
          to: ${INSTALL_PATH}/Warp
          timeout: 10m
    expose:
      desktop:
        - name: Warp
          path: auto
          categories: [System, TerminalEmulator]

  # One universal (x86_64 + arm64) DMG.
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download Warp
          url: https://releases.warp.dev/stable/v0.2026.09.30.08.29.stable_01/Warp.dmg
          checksum: 35718b4ce8749dce96e763605b8c02517643524f46590c8d7861493fa15c9e9c
          to: ${INSTALL_PATH}/.warp.download
          timeout: 15m
        - type: portable
          title: Install Warp
          from: ${INSTALL_PATH}/.warp.download
          to: ${INSTALL_PATH}/Warp
          timeout: 10m
    expose:
      desktop:
        - name: Warp
          path: auto

  # The Windows installer is Inno Setup, run per user (/CURRENTUSER, the scope
  # Warp's WinGet manifest uses): it installs outside the workdir and creates
  # its own Start Menu shortcut, so there is no `expose` here. `uninstall`
  # runs the quiet uninstaller Inno registers under the product code
  # warp-terminal-stable_is1.
  "windows/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download the Warp installer
          url:
            windows/amd64: https://releases.warp.dev/stable/v0.2026.09.30.08.29.stable_01/WarpSetup.exe
            windows/arm64: https://releases.warp.dev/stable/v0.2026.09.30.08.29.stable_01/WarpSetup-arm64.exe
          checksum:
            windows/amd64: d7299334bc4ee6a2eb8cc38b3964d110bbb770707dd60aed6929084c5f473f33
            windows/arm64: 9ac0a2fd6960d9741a5529bdbcf0058fd3fe41c1454aadfe929e81829a18da33
          to: ${INSTALL_PATH}/WarpSetup.exe
          timeout: 15m
        - type: run
          title: Install Warp
          command: '.\WarpSetup.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /CURRENTUSER'
          timeout: 10m
      uninstall:
        - type: run
          title: Uninstall Warp
          command: 'for /f "tokens=2,*" %a in (''reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\warp-terminal-stable_is1" /v QuietUninstallString ^| findstr REG_SZ'') do %b /VERYSILENT /SUPPRESSMSGBOXES /NORESTART'
          timeout: 5m
          exit_on_failure: false
```
