Visual Studio Code is Microsoft's code editor: a fast, extensible editor with built-in support for JavaScript, TypeScript and Node.js, and a marketplace of extensions that add languages, debuggers, themes and tools for almost any stack. It runs on Windows, macOS and Linux, and ties editing, running, debugging and source control together in one window.

![Debugging a Node.js program in Visual Studio Code](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/vscode/screenshots/debugging.png)

## Features

- **IntelliSense**: completions, parameter info and quick documentation based on variable types, function definitions and imported modules.
- **Run and debug**: launch programs, set breakpoints and inspect variables, the call stack and a debug console without leaving the editor.
- **Built-in Git**: review diffs, stage changes and commit from the Source Control view.
- **Integrated terminal**: a shell inside the editor, in the folder you are working on.
- **Extensions**: add languages, debuggers, themes and tools from the Visual Studio Marketplace.
- **Customizable**: themes, keyboard shortcuts and settings, down to every panel's layout.

![Reviewing changes in the Source Control view](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/vscode/screenshots/source-control.png)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | Microsoft's official zip for your processor, as `Visual Studio Code.app` in Applications. Requires macOS 12 or later. |
| Linux (x86_64 and ARM64) | Microsoft's official tarball for your processor, a desktop menu entry and the `code` command. |
| Windows (x64 and ARM64) | Microsoft's official archive (zip) for your processor, unpacked in Quiver's folder with a Start Menu shortcut. Nothing is written to the registry and there is no installer. |

Every download is pinned to VS Code 1.140.0 and verified against the SHA-256 checksum Microsoft publishes for it.

### Good to know

- **These are Microsoft's official builds, not "Code - OSS".** The source code is MIT-licensed, but the builds Microsoft distributes are licensed under the [Microsoft Software License Terms](https://code.visualstudio.com/license) and send usage data to Microsoft by default. You can turn it off with the `telemetry.telemetryLevel` setting, as described in [Microsoft's telemetry documentation](https://code.visualstudio.com/docs/configure/telemetry). The Visual Studio Marketplace is available because these are Microsoft's builds.
- **Updates come through Quiver.** On macOS, VS Code can also update itself in place; on Linux and Windows the archive builds are not updated by the app, so install a newer Quiver release of this arrow to move to a new version.
- **Your settings and extensions live outside Quiver's folder** (`~/.config/Code` and `~/.vscode` on Linux, `~/Library/Application Support/Code` and `~/.vscode` on macOS, `%APPDATA%\Code` and `%USERPROFILE%\.vscode` on Windows), so uninstalling keeps them and they are shared with any other VS Code you have. To keep everything inside Quiver's folder on Windows, create a `data` folder next to `Code.exe` in the arrow's folder ([portable mode](https://code.visualstudio.com/docs/editor/portable)).
- **The `code` command.** Quiver adds it on Linux only (after `quiver path setup`). On macOS the app is moved to Applications, so use the command palette's "Shell Command: Install 'code' command in PATH". On Windows the folder holds `bin\code.cmd` if you want it on your `PATH`.
- **Linux sandbox.** The tarball's `chrome-sandbox` helper is not installed setuid, so VS Code relies on unprivileged user namespaces. On distributions that restrict them (such as Ubuntu 24.04 and later) it may refuse to start, and you must launch it with `--no-sandbox` or allow it in your AppArmor policy.
- **Already have VS Code?** Quiver never replaces an app it did not install. If `Visual Studio Code.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.
- **Minimum hardware**: Microsoft recommends a 1.6 GHz processor and 1 GB of memory; Quiver asks for 2 cores and 2 GB to be comfortable.

## License and trademarks

Visual Studio Code is a product of Microsoft Corporation, distributed under the [Microsoft Software License Terms](https://code.visualstudio.com/license); the source code is available under the MIT license as [Code - OSS](https://github.com/microsoft/vscode). This arrow only downloads Microsoft's official builds from Microsoft's own servers. The Visual Studio Code name and logo are trademarks of Microsoft; the icon is the product icon from the [vscode repository](https://github.com/microsoft/vscode), the banner was generated from it, and the screenshots come from the [VS Code documentation](https://code.visualstudio.com/docs).

```arrow
schema: "arrow@v0"

metadata:
  name: Visual Studio Code
  description: Microsoft's extensible code editor, with debugging, Git and an extension marketplace
  license: Proprietary
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://code.visualstudio.com
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Microsoft
      url: https://code.visualstudio.com
  media:
    icon: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/vscode/icon.png
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/vscode/banner.svg
  tags:
    - editor
    - ide
    - development
    - desktop

# VS Code 1.140.0 (commit 07f806f9...), the exact versioned URLs and SHA-256
# digests served by update.code.visualstudio.com/api/update/<platform>/stable/latest.
# These are Microsoft's official builds (telemetry on by default, Microsoft
# license), not Code - OSS. Requirements: Microsoft recommends 1.6 GHz and
# 1 GB of RAM; cores and disk are conservative estimates.
targets:
  # Tarballs unpack into VSCode-linux-<arch>/. chrome-sandbox is not setuid,
  # so Electron falls back to user namespaces. The ARM64 folder name follows
  # the same convention as x64 and is unverified.
  linux/amd64:
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download Visual Studio Code
          url: https://vscode.download.prss.microsoft.com/dbazure/download/stable/07f806f999227108933c2e30515b26eecc1fda74/code-stable-x64-1790759436.tar.gz
          checksum: d32031e9e213d59532af3cf32fcb8b357a1cdd10417967b4f5b5ba30436dc0dc
          to: ${INSTALL_PATH}/.vscode.download
          timeout: 20m
        - type: extract
          title: Unpack Visual Studio Code
          from: ${INSTALL_PATH}/.vscode.download
          to: ${INSTALL_PATH}/app
          timeout: 10m
    expose:
      cli:
        - name: code
          path: ${INSTALL_PATH}/app/VSCode-linux-x64/bin/code
      desktop:
        - name: VSCode
          path: ${INSTALL_PATH}/app/VSCode-linux-x64/code
          icon: ${INSTALL_PATH}/app/VSCode-linux-x64/resources/app/resources/linux/code.png
          categories: [Development, IDE, TextEditor]

  linux/arm64:
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download Visual Studio Code
          url: https://vscode.download.prss.microsoft.com/dbazure/download/stable/07f806f999227108933c2e30515b26eecc1fda74/code-stable-arm64-1790759311.tar.gz
          checksum: 9609a7655c4bc2a101b343ff22aa91f6678b46d9565b914c0608bd7f2e577fa6
          to: ${INSTALL_PATH}/.vscode.download
          timeout: 20m
        - type: extract
          title: Unpack Visual Studio Code
          from: ${INSTALL_PATH}/.vscode.download
          to: ${INSTALL_PATH}/app
          timeout: 10m
    expose:
      cli:
        - name: code
          path: ${INSTALL_PATH}/app/VSCode-linux-arm64/bin/code
      desktop:
        - name: VSCode
          path: ${INSTALL_PATH}/app/VSCode-linux-arm64/code
          icon: ${INSTALL_PATH}/app/VSCode-linux-arm64/resources/app/resources/linux/code.png
          categories: [Development, IDE, TextEditor]

  # One zip per processor holding "Visual Studio Code.app"; requires macOS 12
  # or later. The bundle is moved to Applications, so no `cli` entry: its
  # `bin/code` would point into a folder that no longer holds the app.
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download Visual Studio Code
          url:
            darwin/arm64: https://vscode.download.prss.microsoft.com/dbazure/download/stable/07f806f999227108933c2e30515b26eecc1fda74/VSCode-darwin-arm64.zip
            darwin/amd64: https://vscode.download.prss.microsoft.com/dbazure/download/stable/07f806f999227108933c2e30515b26eecc1fda74/VSCode-darwin.zip
          checksum:
            darwin/arm64: 86a64f1cc9f4e0b5fc44969530994742f4bd61e7b98d9637238c5e24b26593b0
            darwin/amd64: 5f56ee60956865d79711dd8a1ceef7d94b72ba2c5539a1e46642db07a3d256d2
          to: ${INSTALL_PATH}/.vscode.download
          timeout: 20m
        - type: portable
          title: Install Visual Studio Code
          from: ${INSTALL_PATH}/.vscode.download
          to: ${INSTALL_PATH}/VSCode
          timeout: 10m
    expose:
      desktop:
        - name: VSCode
          path: ${INSTALL_PATH}/VSCode/Visual Studio Code.app

  # The archive (zip) build, not the installer: it unpacks entirely inside the
  # workdir (Code.exe at its root), writes nothing to the registry and needs no
  # uninstall. The ARM64 zip is assumed to share the x64 layout (unverified).
  "windows/*":
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download Visual Studio Code
          url:
            windows/amd64: https://vscode.download.prss.microsoft.com/dbazure/download/stable/07f806f999227108933c2e30515b26eecc1fda74/VSCode-win32-x64-1.140.0.zip
            windows/arm64: https://vscode.download.prss.microsoft.com/dbazure/download/stable/07f806f999227108933c2e30515b26eecc1fda74/VSCode-win32-arm64-1.140.0.zip
          checksum:
            windows/amd64: 52f47072473375767d63ea5be9ffb96a3092124223fe5ce036834a299715014e
            windows/arm64: d55904f6048e351890bac7ac70d2380a8daa5e9ca2290a184ad4988c9f4d3432
          to: ${INSTALL_PATH}/.vscode.download
          timeout: 20m
        - type: extract
          title: Unpack Visual Studio Code
          from: ${INSTALL_PATH}/.vscode.download
          to: ${INSTALL_PATH}/VSCode
          timeout: 10m
    expose:
      desktop:
        - name: VSCode
          path: ${INSTALL_PATH}/VSCode/Code.exe
```
