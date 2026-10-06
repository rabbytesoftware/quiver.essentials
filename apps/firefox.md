Firefox is the web browser from the non-profit Mozilla Foundation. It runs on its own engine (Gecko) rather than Chromium, blocks cross-site tracking by default, and supports a large catalogue of add-ons and themes.

![Firefox's new tab page listing its privacy protections](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/firefox/screenshots/privacy-and-extensions.jpg)

## Features

- **Total Cookie Protection**: keeps cookies from following you from site to site, alongside blocking of cryptominers and fingerprinting.
- **Private browsing**: private windows that block third-party cookies and content trackers and clear your history when closed.
- **Sync**: with a Firefox account, passwords, bookmarks and open tabs follow you between computers and your phone.
- **Built-in password manager**: saves logins, fills them in and suggests strong passwords.
- **Picture-in-Picture**: pops a video out into its own window that stays on top while you browse elsewhere.
- **PDF viewer and editor**: view, print, annotate and sign PDFs in the browser.
- **Offline translation**: translates web pages on your computer rather than in the cloud.
- **Reader View and add-ons**: a distraction-free reading mode, and extensions and themes from Mozilla's add-on site.

![Firefox open next to a phone, syncing tabs between devices](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/firefox/screenshots/sync-tabs.jpg)

![A video playing in Firefox's Picture-in-Picture window](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/firefox/screenshots/picture-in-picture.jpg)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | Mozilla's official DMG (one universal build), as `Firefox.app` in Applications. |
| Linux (x86_64 and ARM64) | Mozilla's official `.tar.xz` build, unpacked into Quiver's folder, and a desktop menu entry. Needs glibc 2.17 and GTK 3.14 (glibc 2.28 on ARM64). |
| Windows (x64 and ARM64) | Mozilla's official installer, run silently into Quiver's folder for your user, without administrator rights. It adds its own Start Menu shortcut. Requires Windows 10 or later. |

Every download is pinned to Firefox 157.0 on [archive.mozilla.org](https://archive.mozilla.org/pub/firefox/releases/157.0/) and verified against the SHA-256 checksum Mozilla publishes in that release's `SHA256SUMS` file. The builds are English (US); Firefox's language can be changed in its settings by installing a language pack.

### Good to know

- **Firefox keeps itself up to date** on every platform, in place. Quiver installs the release pinned here; Firefox may be newer afterwards, and reinstalling through Quiver goes back to the pinned version.
- **Your profile lives outside Quiver's folder** (`~/Library/Application Support/Firefox` on macOS, `~/.mozilla/firefox` on Linux, `%APPDATA%\Mozilla\Firefox` on Windows), so uninstalling keeps your bookmarks and settings. Delete it to remove everything.
- **On Windows, Firefox is installed inside Quiver's folder**, but the installer also writes Start Menu and registry entries for your user. Uninstalling through Quiver runs Firefox's own uninstaller; the Mozilla Maintenance Service, which needs administrator rights, is not installed.
- **Already have Firefox?** Quiver never replaces an app it did not install. If `Firefox.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.
- **Hardware**: Mozilla lists 1 GHz or faster processors, 2 GB of RAM for the 64-bit Windows version and 500 MB of disk space on Windows. Mozilla's page still states macOS 10.15 or later.

## License and trademarks

Firefox is free software by Mozilla, released under the [Mozilla Public License 2.0](https://www.mozilla.org/MPL/2.0/). This arrow only downloads Mozilla's official builds from archive.mozilla.org. The Firefox name and logo are trademarks of the Mozilla Foundation, used under its [logo and trademark policy](https://www.mozilla.org/foundation/trademarks/policy/); the icon is the logo from Mozilla's [Firefox source repository](https://github.com/mozilla-firefox/firefox), the banner was generated from it, and the screenshots come from Mozilla's official Microsoft Store listing.

```arrow
schema: "arrow@v0"

metadata:
  name: Firefox
  description: The independent web browser from Mozilla, built for privacy
  license: MPL-2.0
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://www.mozilla.org/firefox/
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Mozilla
      url: https://www.mozilla.org
  media:
    icon: https://raw.githubusercontent.com/mozilla-firefox/firefox/FIREFOX_157_0_RELEASE/browser/branding/official/content/about-logo.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/firefox/banner.svg
  tags:
    - browser
    - privacy
    - desktop

# Firefox 157.0 (en-US), straight from archive.mozilla.org with the SHA-256
# values of that release's SHA256SUMS. Requirements are conservative estimates:
# Mozilla's published minimums are lower.
targets:
  # Self-contained tarballs; Firefox updates itself inside the unpacked folder.
  # The archive's top folder is `firefox/`, holding the `firefox` launcher and
  # the icons under browser/chrome/icons/default.
  "linux/*":
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download Firefox
          url:
            linux/amd64: https://archive.mozilla.org/pub/firefox/releases/157.0/linux-x86_64/en-US/firefox-157.0.tar.xz
            linux/arm64: https://archive.mozilla.org/pub/firefox/releases/157.0/linux-aarch64/en-US/firefox-157.0.tar.xz
          checksum:
            linux/amd64: 42f2c62a562316982ef5a796738c57602bf84a984f5c616e80bcff4627f78fff
            linux/arm64: 73fc3d6f6f4d3fcdeee59db90156568af9959405120ad686e535f572995074d0
          to: ${INSTALL_PATH}/.firefox.download
          timeout: 15m
        - type: extract
          title: Unpack Firefox
          from: ${INSTALL_PATH}/.firefox.download
          to: ${INSTALL_PATH}/app
          timeout: 5m
    expose:
      desktop:
        - name: Firefox
          path: ${INSTALL_PATH}/app/firefox/firefox
          icon: ${INSTALL_PATH}/app/firefox/browser/chrome/icons/default/default128.png
          categories: [Network, WebBrowser]

  # One DMG for both processors (Firefox's own self-update replaces the app in place).
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download Firefox
          url: https://archive.mozilla.org/pub/firefox/releases/157.0/mac/en-US/Firefox%20157.0.dmg
          checksum: df6d8c79b6126bcf24cb70ebab9371916a662028e2d706e462d432e78fdf396c
          to: ${INSTALL_PATH}/.firefox.download
          timeout: 15m
        - type: portable
          title: Install Firefox
          from: ${INSTALL_PATH}/.firefox.download
          to: ${INSTALL_PATH}/Firefox
          timeout: 10m
    expose:
      desktop:
        - name: Firefox
          path: auto

  # The full installer, run silently (/S) into the workdir (/InstallDirectoryPath)
  # so that no administrator rights are needed and the uninstaller has a fixed
  # path. The Maintenance Service (which needs admin) is skipped; desktop and
  # taskbar shortcuts are off, the installer's own Start Menu shortcut is the
  # entry point, so there is no `expose`. The installer is deleted afterwards.
  # `uninstall` runs the helper.exe Firefox writes into its install folder.
  # Requires Windows 10 or later.
  "windows/*":
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download the Firefox installer
          url:
            windows/amd64: https://archive.mozilla.org/pub/firefox/releases/157.0/win64/en-US/Firefox%20Setup%20157.0.exe
            windows/arm64: https://archive.mozilla.org/pub/firefox/releases/157.0/win64-aarch64/en-US/Firefox%20Setup%20157.0.exe
          checksum:
            windows/amd64: 58c90afab6e4b9a6b34d2958fe06d1a143dd9226ea8834377e5cd45e815936d7
            windows/arm64: 511f539825c249db351eb0616db8c7860c49dbd39499264105081e7536fcf670
          to: ${INSTALL_PATH}/FirefoxSetup.exe
          timeout: 15m
        - type: run
          title: Install Firefox
          command: '.\FirefoxSetup.exe /S /InstallDirectoryPath="%CD%\Firefox" /MaintenanceService=false /DesktopShortcut=false /TaskbarShortcut=false /PreventRebootRequired=true && del /q FirefoxSetup.exe'
          timeout: 10m
      uninstall:
        - type: run
          title: Uninstall Firefox
          command: '.\Firefox\uninstall\helper.exe /S'
          timeout: 5m
          exit_on_failure: false
```
