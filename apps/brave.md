Brave is a web browser built on Chromium that blocks ads and trackers by default. It runs the same websites and most of the same extensions as Chrome, and adds privacy features of its own: Shields on every site, fingerprinting protection, private windows that route through Tor, and Brave Search, an independent search engine, as the default.

![Brave's new tab page](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/brave/screenshots/new-tab.jpg)

## Features

- **Shields**: blocks ads, trackers, fingerprinting and cross-site cookies on every site, adjustable per site.
- **Brave Search**: an independent search index, set as the default search engine.
- **Private windows with Tor**: private browsing that also hides your IP address from the sites you visit.
- **Sync**: encrypted sync of bookmarks, passwords and tabs between your devices.
- **Built in**: vertical tabs, page translation, Speedreader and Leo, Brave's AI assistant.
- **Optional extras**: Brave Rewards, the Brave Wallet and the paid Brave VPN are opt-in.

![Shields blocking ads and trackers on a recipe site](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/brave/screenshots/ad-blocker.jpg)

![The new tab page counting trackers blocked and time saved](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/brave/screenshots/privacy-stats.jpg)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | Brave's official DMG for your processor, as `Brave Browser.app` in Applications. Requires macOS 13 or later. |
| Linux (x86_64 and ARM64) | Brave's official zip build, unpacked into Quiver's folder, and a desktop menu entry. |
| Windows (x64 and ARM64) | Brave's official per-user silent installer. It installs Brave for your user and adds its own Start Menu shortcut. Requires Windows 10 or later. |

Every download is pinned to an official Brave release from [Brave's GitHub releases](https://github.com/brave/brave-browser/releases) and verified against its SHA-256 checksum before it runs.

### Good to know

- **On macOS and Windows, Brave keeps itself up to date.** Quiver installs the release pinned here; from then on Brave's own updater installs new versions.
- **On Linux, update Brave through Quiver.** The zip build has no updater of its own; Brave's own Linux updates come only through its package repositories.
- **On Linux, Brave needs unprivileged user namespaces for its sandbox.** The zip build's setuid sandbox helper cannot keep its root ownership when unpacked by a normal user, so Brave relies on user namespaces instead. Distributions that restrict them (Ubuntu 24.04 and later, through AppArmor) may stop Brave from starting until they are allowed for it.
- **Your profile lives outside Quiver's folder** (`~/Library/Application Support/BraveSoftware` on macOS, `~/.config/BraveSoftware` on Linux, `%LOCALAPPDATA%\BraveSoftware` on Windows), so uninstalling keeps your bookmarks and settings. Delete it to remove everything.
- **On Windows, Brave installs into your user profile**, not into Quiver's folder. Uninstalling through Quiver runs Brave's own uninstaller.
- **Already have Brave?** Quiver never replaces an app it did not install. If `Brave Browser.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.

## License and trademarks

Brave is free software by Brave Software, Inc., released under the [Mozilla Public License 2.0](https://github.com/brave/brave-browser/blob/master/LICENSE). This arrow only downloads Brave's official builds from its GitHub releases. The Brave name and lion logo are trademarks of Brave Software, Inc.; the icon is the product logo from the [brave-core repository](https://github.com/brave/brave-core), the banner is the social image from [brave.com](https://brave.com), and the screenshots come from Brave's official Microsoft Store listing.

```arrow
schema: "arrow@v0"

metadata:
  name: Brave
  description: The privacy-first web browser that blocks ads and trackers by default
  license: MPL-2.0
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://brave.com
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Brave Software, Inc.
      url: https://brave.com
  media:
    icon: https://raw.githubusercontent.com/brave/brave-core/v1.96.61/app/theme/brave/product_logo.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/brave/banner.png
  tags:
    - browser
    - privacy
    - desktop

# Every download is a release asset of github.com/brave/brave-browser (Release
# channel v1.96.61), with the digest GitHub publishes for it. Requirements are
# conservative estimates: Brave publishes OS versions but no hardware
# minimums.
targets:
  # The zip is Brave's self-contained Linux build; `brave-browser` is its own
  # launcher script next to the `brave` binary. Linux builds have no updater:
  # new releases come from a newer arrow.
  "linux/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download Brave
          url:
            linux/amd64: https://github.com/brave/brave-browser/releases/download/v1.96.61/brave-browser-1.96.61-linux-amd64.zip
            linux/arm64: https://github.com/brave/brave-browser/releases/download/v1.96.61/brave-browser-1.96.61-linux-arm64.zip
          checksum:
            linux/amd64: c68cf179603470e8001a949294fe98b593f0749ca95f42687d855081b1c394a4
            linux/arm64: 33a1513379505642e4df0dda36a1dd78f735ee351631cffd4a4ac90b1cec0cd5
          to: ${INSTALL_PATH}/.brave.download
          timeout: 15m
        - type: extract
          title: Unpack Brave
          from: ${INSTALL_PATH}/.brave.download
          to: ${INSTALL_PATH}/app
          timeout: 5m
    expose:
      desktop:
        - name: Brave
          path: ${INSTALL_PATH}/app/brave-browser
          icon: ${INSTALL_PATH}/app/product_logo_256.png
          categories: [Network, WebBrowser]

  # One DMG per processor; requires macOS 13 or later.
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download Brave
          url:
            darwin/arm64: https://github.com/brave/brave-browser/releases/download/v1.96.61/Brave-Browser-arm64.dmg
            darwin/amd64: https://github.com/brave/brave-browser/releases/download/v1.96.61/Brave-Browser-x64.dmg
          checksum:
            darwin/arm64: 82d53547108cc995681037fee8fd57e58a3a4311cce1cc0c3150cbb1bc405f14
            darwin/amd64: 1fdcd5530ec1d1004287c587dd84fb6113e7b58478cf72aa5b329dbed1b87f07
          to: ${INSTALL_PATH}/.brave.download
          timeout: 15m
        - type: portable
          title: Install Brave
          from: ${INSTALL_PATH}/.brave.download
          to: ${INSTALL_PATH}/Brave
          timeout: 10m
    expose:
      desktop:
        - name: Brave
          path: auto

  # The silent standalone installer installs per user into
  # %LOCALAPPDATA%\BraveSoftware, outside the workdir, and creates its own
  # Start Menu shortcut, so there is no `expose` here.
  # `uninstall` runs the uninstaller Brave registers for the user, which moves
  # with Brave's self-updates. Requires Windows 10 or later.
  "windows/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download the Brave installer
          url:
            windows/amd64: https://github.com/brave/brave-browser/releases/download/v1.96.61/BraveBrowserStandaloneSilentSetup.exe
            windows/arm64: https://github.com/brave/brave-browser/releases/download/v1.96.61/BraveBrowserStandaloneSilentSetupArm64.exe
          checksum:
            windows/amd64: 36fe4f98bfe7cac4c3f6955106bf5b9af52c2f26446f72fa743d0eeec49610d8
            windows/arm64: 8e9710a69d5248e5057acd392f54675ddcb3c352ce1b3a2fa44c1df89eff7b84
          to: ${INSTALL_PATH}/BraveSetup.exe
          timeout: 15m
        - type: run
          title: Install Brave
          command: '.\BraveSetup.exe'
          timeout: 10m
      uninstall:
        - type: run
          title: Uninstall Brave
          command: 'for /f "tokens=2,*" %a in (''reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\BraveSoftware Brave-Browser" /v UninstallString ^| findstr REG_SZ'') do %b --force-uninstall'
          timeout: 5m
          exit_on_failure: false
```
