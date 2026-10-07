Figma is a collaborative design tool for interfaces, prototypes and design systems. Several people can work in the same file at once, with live cursors and comments, and the same files open in the browser and in the desktop app. The desktop app adds access to the fonts installed on your computer, desktop notifications and local plugin development.

![The Figma Design editor](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/figma/screenshots/design-editor.jpg)

## Features

- **Multiplayer canvas**: edit the same file together, with live cursors, comments and cursor chat.
- **Components and variables**: reusable UI elements and shared values for colour, spacing and text, kept consistent across files.
- **Auto layout**: frames that resize and reflow as their content changes.
- **Prototyping**: link frames into interactive prototypes and present them from the app.
- **Dev Mode**: inspect designs and hand them off to developers, with code snippets and Code Connect.
- **Branching and merging**: try changes in a branch without touching the main file.

![Auto layout reflowing a card as it is resized](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/figma/screenshots/auto-layout.jpg)

![Variables and styles for typography, colour, spacing and motion](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/figma/screenshots/variables.jpg)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | Figma's official app for your processor, as `Figma.app` in Applications. Requires macOS 12 or later. |
| Windows (x64 and ARM64) | Figma's official installer, run silently. It installs Figma for your user and adds its own Start Menu shortcut. Requires Windows 10 or later, 64-bit. |
| Linux | Not available: Figma publishes no desktop app for Linux. Use Figma in the browser instead. |

Every download is pinned to an official Figma build and verified against its SHA-256 checksum before it runs.

### Good to know

- **You need a Figma account.** The app asks you to sign in on first launch; Figma's Starter plan is free.
- **Figma keeps itself up to date.** Quiver installs the build pinned here; from then on Figma's own updater installs new versions. Figma stops supporting a desktop version six months after its release.
- **On Windows, Figma installs into your user profile** (`%LOCALAPPDATA%\Figma`), not into Quiver's folder. Uninstalling through Quiver runs Figma's own uninstaller.
- **Already have Figma?** Quiver never replaces an app it did not install. If `Figma.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.

## License and trademarks

Figma is proprietary software by Figma, Inc., used under its [Terms of Service](https://www.figma.com/legal/tos/). This arrow only downloads Figma's official builds from Figma's own servers. The Figma name and logo are trademarks of Figma, Inc.; the icon is the full-colour Figma icon from its [brand guidelines](https://www.figma.com/using-the-figma-brand/), unmodified and placed on a square canvas, the banner is the social-share image of Figma's [Figma Design page](https://www.figma.com/design/), cropped to 2:1, and the screenshots come from Figma's [product page](https://www.figma.com/design/).

```arrow
schema: "arrow@v0"

metadata:
  name: Figma
  description: The collaborative interface design tool, on your desktop
  license: Proprietary
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://www.figma.com/downloads/
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Figma, Inc.
      url: https://www.figma.com
  media:
    icon: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/figma/icon.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/figma/banner.jpg
  tags:
    - design
    - prototyping
    - desktop

# Figma updates itself after install on every platform, so the pinned builds
# below are only what the first install fetches. Requirements are
# conservative estimates: Figma publishes OS versions but no hardware
# minimums. There is no Linux desktop app.
targets:
  # One build per processor (the zip holds Figma.app); requires macOS 12 or
  # later. The versioned URLs are the ones Figma's RELEASE.json names.
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download Figma
          url:
            darwin/arm64: https://desktop.figma.com/mac-arm/Figma-126.9.11.zip
            darwin/amd64: https://desktop.figma.com/mac/Figma-126.9.11.zip
          checksum:
            darwin/arm64: 0c93c31c79338e0c108b139dc08e3a1256699faaa7a3248042e7aa2c5fde3043
            darwin/amd64: 667f016dcfdacbdfb288ee52d72f0054ca695f42da63bab2bf25655551433e93
          to: ${INSTALL_PATH}/.figma.download
          timeout: 15m
        - type: portable
          title: Install Figma
          from: ${INSTALL_PATH}/.figma.download
          to: ${INSTALL_PATH}/Figma
          timeout: 10m
    expose:
      desktop:
        - name: Figma
          path: auto

  # The Windows installer is Squirrel: it installs per user into
  # %LOCALAPPDATA%\Figma, outside the workdir, and creates its own Start Menu
  # shortcut, so there is no `expose` here and `uninstall` runs Squirrel's own
  # uninstaller. Requires Windows 10 or later, 64-bit.
  "windows/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download the Figma installer
          url:
            windows/amd64: https://desktop.figma.com/win/build/Figma-126.9.11.exe
            windows/arm64: https://desktop.figma.com/win-arm/build/Figma-126.9.11.exe
          checksum:
            windows/amd64: a685f473b50220b94831303a2b83d653e075f2dfde199dfc85672974a59f3d8e
            windows/arm64: 475136547c239f1ed2bdad135e6f90740082808ec4c3423b9e007640199c9bd2
          to: ${INSTALL_PATH}/FigmaSetup.exe
          timeout: 15m
        - type: run
          title: Install Figma
          command: '.\FigmaSetup.exe --silent'
          timeout: 10m
      uninstall:
        - type: run
          title: Uninstall Figma
          command: '"%LOCALAPPDATA%\Figma\Update.exe" --uninstall -s'
          timeout: 5m
          exit_on_failure: false
```
