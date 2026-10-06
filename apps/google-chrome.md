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
| Windows (x64 and ARM64) | Google's official standalone installer for the current stable release, run for your user (no administrator rights). Chrome installs into your user profile and adds its own shortcuts. Requires Windows 10 or later. |

Not supported: **Linux**. Google publishes Chrome for Linux only as `.deb` and `.rpm` packages, with no AppImage or tarball that Quiver can unpack on every distribution, so this arrow does not support Linux.

Quiver installs the current stable Chrome from Google's own "current" download addresses, so the install always fetches the latest release and can never point at a build Google has removed. These downloads are fetched over HTTPS from Google and are **not checksum-verified**: Google publishes no checksum for a file that changes with every release.

This is Google Chrome itself, not Chrome for Testing: that is a separate build meant for test automation, with no auto-update and a different name and profile.

### Good to know

- **On macOS and Windows, Chrome keeps itself up to date.** Quiver installs the current release at the time you install; from then on Chrome's own updater installs new versions.
- **Your profile lives outside Quiver's folder** (`~/Library/Application Support/Google/Chrome` on macOS, `%LOCALAPPDATA%\Google\Chrome\User Data` on Windows), so uninstalling keeps your bookmarks and settings. Delete it to remove everything.
- **On Windows, Chrome installs into your user profile**, not into Quiver's folder, together with Google's per-user updater. Uninstalling through Quiver runs Chrome's own uninstaller. The installer is about 170 MB; Quiver deletes it after installing.
- **Downloads are not checksum-verified.** They come over HTTPS from Google's servers, but they are "current" links, so no fixed checksum can be pinned.
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

# Google keeps no permanent versioned download URLs for Chrome, so the arrow
# uses its stable "current" addresses and carries no `checksum` (Google
# publishes none for a rolling file); the downloads are HTTPS from Google.
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
          url: https://dl.google.com/chrome/mac/universal/stable/GGRO/googlechrome.dmg
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

  # Google's standalone installer for the current stable release (the tag
  # needsadmin=false makes it install per user into %LOCALAPPDATA%\Google\Chrome),
  # outside the workdir, and creates its own shortcuts: there is no `expose`.
  # It is ~170 MB, so it is deleted once Chrome is installed. `uninstall` runs
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
            windows/amd64: https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7B00000000-0000-0000-0000-000000000000%7D%26lang%3Den%26browser%3D4%26usagestats%3D0%26appname%3DGoogle%2520Chrome%26needsadmin%3Dfalse%26ap%3Dx64-stable-statsdef_1%26installdataindex%3Dempty/chrome/install/ChromeStandaloneSetup64.exe
            windows/arm64: https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7B00000000-0000-0000-0000-000000000000%7D%26lang%3Den%26browser%3D4%26usagestats%3D0%26appname%3DGoogle%2520Chrome%26needsadmin%3Dfalse%26ap%3Darm64-stable-statsdef_1%26installdataindex%3Dempty/chrome/install/ChromeStandaloneSetup64.exe
          to: ${INSTALL_PATH}/ChromeSetup.exe
          timeout: 40m
        - type: run
          title: Install Chrome
          command: '.\ChromeSetup.exe /silent /install >nul 2>&1 <nul && del /q ChromeSetup.exe'
          timeout: 15m
      uninstall:
        - type: run
          title: Uninstall Chrome
          command: 'for /f "tokens=2,*" %a in (''reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome" /v UninstallString ^| findstr REG_SZ'') do %b --uninstall --channel=stable --force-uninstall'
          timeout: 10m
          exit_on_failure: false
```
