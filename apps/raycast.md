Raycast is a launcher for the Mac: one keyboard shortcut opens a search bar that starts apps, finds files, runs commands and answers questions without leaving what you are doing. Built-in tools such as clipboard history, window management and snippets cover everyday chores, and thousands of community extensions connect it to the apps you already use.

![Raycast searching files from its root search](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/raycast/screenshots/file-search.jpg)

## Features

- **One search bar for everything**: apps, files, commands and settings from the same place, all from the keyboard.
- **Built-in tools**: clipboard history, window management, snippets, quicklinks, a calculator, an emoji picker and calendar.
- **Raycast Notes**: a floating notes window for capturing a thought while working on something else.
- **Raycast AI**: quick questions and full chats with AI models, from the search bar.
- **Extensions**: a store of community-built extensions for tools such as Linear, Slack, Notion, Spotify and 1Password.
- **Free to use**: the core app is free; Raycast Pro is an optional paid plan.

![Raycast's calculator answering a question in plain English](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/raycast/screenshots/calculator.jpg)

![Raycast AI chat](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/raycast/screenshots/ai-chat.jpg)

## Installing with Quiver

| Platform | Available | Why |
|---|---|---|
| macOS (Apple silicon) | Yes | Raycast's official DMG, installed as `Raycast.app` in Applications. Raycast 2 requires macOS 26 (Tahoe) or later. |
| macOS (Intel) | No | Raycast 2 runs only on Apple silicon. |
| Windows | No | Raycast for Windows ships as an MSIX package, a format Quiver cannot install. Get it from [raycast.com/windows](https://www.raycast.com/windows). |
| Linux | No | There is no Raycast for Linux. |

Quiver downloads the current official Raycast build for Apple silicon from Raycast's own servers over HTTPS. Raycast publishes no checksum and only keeps a rolling "latest" address, so this download is **not checksum-verified**.

### Good to know

- **The download is not checksum-verified.** It comes over HTTPS from Raycast's own servers; Raycast offers only a rolling "latest" address, so a fixed checksum would stop matching with the next build.
- **Raycast keeps itself up to date.** Quiver installs the build current at install time; from then on Raycast's own updater installs new versions.
- **Already have Raycast?** Quiver never replaces an app it did not install. If `Raycast.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.

## License and trademarks

Raycast is proprietary software by Raycast Technologies Ltd., free to use under its [Terms of Service](https://www.raycast.com/terms-of-service). This arrow only downloads Raycast's official build from Raycast's own servers. The Raycast name and logo are trademarks of Raycast Technologies Ltd.; the icon comes from Raycast's [press kit](https://www.raycast.com/press), the banner is Raycast's own social image from [raycast.com](https://www.raycast.com) (2400x1260, trimmed to 2:1), and the screenshots come from [raycast.com](https://www.raycast.com).

```arrow
schema: "arrow@v0"

metadata:
  name: Raycast
  description: A fast, extendable launcher for your Mac
  license: Proprietary
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://www.raycast.com
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Raycast Technologies Ltd.
      url: https://www.raycast.com
  media:
    icon: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/raycast/icon.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/raycast/banner.png
  tags:
    - launcher
    - productivity
    - desktop

# macOS on Apple silicon only: Raycast 2 is built for arm64 alone and needs
# macOS 26 or later (LSMinimumSystemVersion 26.0). Raycast for Windows ships
# as MSIX, which Quiver cannot install, and there is no Linux build.
targets:
  # Raycast's stable "latest" endpoint (the one raycast.com/download redirects
  # to), which answers with a 302 to the current versioned DMG. It is used
  # instead of that versioned file because Raycast ships new builds every few
  # days (2.6.2 was already superseded by 2.6.3 when this was written) and
  # publishes no retention policy or checksum list, so a pinned URL or digest
  # would rot: the download is therefore not checksum-verified. Raycast updates
  # itself after install. Requirements are conservative estimates: Raycast
  # publishes no hardware minimums.
  darwin/arm64:
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download Raycast
          url: https://x.raycast-releases.com/download/web?platform=macos&architecture=arm64
          to: ${INSTALL_PATH}/.raycast.download
          timeout: 15m
        - type: portable
          title: Install Raycast
          from: ${INSTALL_PATH}/.raycast.download
          to: ${INSTALL_PATH}/Raycast
          timeout: 10m
    expose:
      desktop:
        - name: Raycast
          path: auto
```
