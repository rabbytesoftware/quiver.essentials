Google Chrome is Google's web browser. It signs in with a Google account to sync bookmarks, passwords and tabs between devices, runs the extensions in the Chrome Web Store, and keeps separate profiles for work, home or anyone else who shares the computer.

![Chrome with themes, profiles and a new tab page](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/google-chrome/screenshots/themes-and-profiles.png)

## Features

- **Sync**: sign in with a Google account to carry bookmarks, history, passwords and open tabs across your computers and phone.
- **Extensions and themes**: add-ons from the Chrome Web Store, and themes that restyle the browser and its new tab page.
- **Profiles**: separate sets of bookmarks, extensions, settings and sign-ins, so work and personal browsing stay apart.
- **Password Manager**: offers to save logins and fills them in on the sites you use.
- **Safety Check and Privacy Guide**: built-in pages that review your passwords, extensions, updates and privacy settings.
- **Tab management**: tab groups, and an energy-saver mode that reduces what the browser does in the background.

![Chrome's new tab page in a dark theme](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/google-chrome/screenshots/new-tab.png)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | Google's official universal DMG, as `Google Chrome.app` in Applications. Requires macOS 13 or later. |
| Windows (x64 and ARM64) | Google's official offline installer, run for your user (no administrator rights). Chrome installs into your user profile and adds its own shortcuts. Requires Windows 10 or later. |

Not supported: **Linux**. Google publishes Chrome for Linux only as `.deb` and `.rpm` packages, with no AppImage or tarball that Quiver can unpack on every distribution, so this arrow does not support Linux.

Google publishes no fixed download link for Chrome, only "latest" links that change under you. Quiver therefore uses the versioned, content-addressed download URLs Google's own update service hands out (the ones Chrome itself updates from). Every file is pinned to Chrome 154 and verified against the SHA-256 checksum Google publishes for it in the update service's response.

This is Google Chrome itself, not Chrome for Testing: that is a separate build meant for test automation, with no auto-update and a different name and profile.

### Good to know

- **On macOS and Windows, Chrome keeps itself up to date.** Quiver installs the release pinned here; from then on Chrome's own updater installs new versions. Chrome may therefore be newer than the version in this arrow.
- **Your profile lives outside Quiver's folder** (`~/Library/Application Support/Google/Chrome` on macOS, `%LOCALAPPDATA%\Google\Chrome\User Data` on Windows), so uninstalling keeps your bookmarks and settings. Delete it to remove everything.
- **On Windows, Chrome installs into your user profile**, not into Quiver's folder, together with Google's per-user updater. Uninstalling through Quiver runs Chrome's own uninstaller. The installer is about 500 MB; Quiver deletes it after installing.
- **Already have Chrome?** Quiver never replaces an app it did not install. If `Google Chrome.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.
- **Using Chrome is subject to Google's terms.** Chrome is not open source and Quiver does not redistribute it: it downloads Google's files straight from Google's servers onto your machine.

## License and trademarks

Google Chrome is proprietary software by Google LLC, free to use under the [Google Chrome Terms of Service](https://www.google.com/chrome/terms/); it is built on the open-source Chromium project. This arrow only downloads Google's official builds from Google's own servers. The Google Chrome name and logo are trademarks of Google LLC; the icon is the logo published on [google.com/chrome](https://www.google.com/chrome/), the banner and screenshots are Google's official images from that page (the banner is its homepage image, cropped to 2:1).

```arrow
schema: "arrow@v0"

metadata:
  name: Google Chrome
  description: Google's web browser, with sync, extensions and profiles
  license: Proprietary
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://www.google.com/chrome/
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Google LLC
      url: https://www.google.com/chrome/
  media:
    icon: https://www.google.com/chrome/static/images/chrome-logo-m100.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/google-chrome/banner.png
  tags:
    - browser
    - desktop

# Chrome 154. Google offers only rolling "latest" links, so the pins come from
# its own metadata:
#  - macOS and Windows: the response of Google's update service
#    (update.googleapis.com/service/update2/json, Omaha protocol 3.1, stable
#    channel), which names an immutable versioned URL under
#    dl.google.com/release2/chrome/ and its SHA-256.
#  - Linux is not supported: Google ships it only as .deb/.rpm.
# Requirements are conservative estimates: Google publishes OS versions but
# no hardware minimums.
targets:

  # One universal DMG (Intel and Apple silicon); requires macOS 13 or later.
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download Chrome
          url: https://dl.google.com/release2/chrome/oesfoc5zcpr4zxi27ozbzxre4i_154.0.8037.98/GoogleChrome-154.0.8037.98.dmg
          checksum: 7f85cdec42632b482b2afc5fe8ee04bcf730082cec1328c0041d788632f57542
          to: ${INSTALL_PATH}/.chrome.download
          timeout: 30m
        - type: portable
          title: Install Chrome
          from: ${INSTALL_PATH}/.chrome.download
          to: ${INSTALL_PATH}/Chrome
          timeout: 10m
    expose:
      desktop:
        - name: Chrome
          path: auto

  # Google's offline installer (the same file its updater runs), started without
  # --system-level so it installs per user into %LOCALAPPDATA%\Google\Chrome,
  # outside the workdir, and creates its own shortcuts: there is no `expose`.
  # It is ~500 MB, so it is deleted once Chrome is installed. `uninstall` runs
  # the setup.exe Chrome registers for the user under the "Google Chrome"
  # uninstall key (it moves with Chrome's own updates); --force-uninstall skips
  # the confirmation dialog. Requires Windows 10 or later.
  "windows/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download the Chrome installer
          url:
            windows/amd64: https://dl.google.com/release2/chrome/ac3stf7x6z62hvwmphhro6dpbhpq_154.0.8037.98/154.0.8037.98_chrome_installer_uncompressed.exe
            windows/arm64: https://dl.google.com/release2/chrome/acywoj3yjdggwoxnkmqxkimevloq_154.0.8037.98/154.0.8037.98_chrome_installer_uncompressed.exe
          checksum:
            windows/amd64: 2d5f2073185cdf8e72bd70b19970bcb2e1ade19a85d68b6be2a3fe672816941d
            windows/arm64: d3a01842d9d7bd56c5ea8323558df1f61b7b87018d0624dabf2ffdf32b2d7549
          to: ${INSTALL_PATH}/ChromeSetup.exe
          timeout: 40m
        - type: run
          title: Install Chrome
          command: '.\ChromeSetup.exe --do-not-launch-chrome --channel=stable >nul 2>&1 <nul && del /q ChromeSetup.exe'
          timeout: 15m
      uninstall:
        - type: run
          title: Uninstall Chrome
          command: 'for /f "tokens=2,*" %a in (''reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome" /v UninstallString ^| findstr REG_SZ'') do %b --uninstall --channel=stable --force-uninstall'
          timeout: 10m
          exit_on_failure: false
```
