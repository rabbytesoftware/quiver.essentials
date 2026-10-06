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
| Linux (x86_64 and ARM64) | The `.deb` package from Google's own repository, unpacked into Quiver's folder without root, and a desktop menu entry. |
| Windows (x64 and ARM64) | Google's official offline installer, run for your user (no administrator rights). Chrome installs into your user profile and adds its own shortcuts. Requires Windows 10 or later. |

Google publishes no fixed download link for Chrome, only "latest" links that change under you. Quiver therefore uses the versioned, content-addressed download URLs Google's own update service hands out (the ones Chrome itself updates from) and the `.deb` from Google's apt repository. Every file is pinned to Chrome 154 and verified against the SHA-256 checksum Google publishes for it: in the update service's response for macOS and Windows, and in the apt repository's `Packages` index for Linux.

This is Google Chrome itself, not Chrome for Testing: that is a separate build meant for test automation, with no auto-update and a different name and profile.

### Good to know

- **On macOS and Windows, Chrome keeps itself up to date.** Quiver installs the release pinned here; from then on Chrome's own updater installs new versions. Chrome may therefore be newer than the version in this arrow.
- **On Linux, update Chrome through Quiver.** An unpacked `.deb` has no installer scripts, so Google's apt repository, its daily update job and the setuid sandbox helper are not set up.
- **On Linux, Chrome relies on unprivileged user namespaces for its sandbox**, because its setuid helper cannot keep root ownership when unpacked by a normal user. Distributions that restrict them (Ubuntu 24.04 and later, through AppArmor) may stop Chrome from starting until they are allowed. Google lists 64-bit Ubuntu 18.04+, Debian 10+, openSUSE 15.5+ and Fedora 39+ as supported; the launcher needs `bash`.
- **The pinned Linux download can disappear.** Google's apt repository keeps only its current stable release, so once Google publishes a newer one the pinned `.deb` link stops working until the arrow is updated. The macOS and Windows links are content-addressed and are not rotated the same way.
- **Your profile lives outside Quiver's folder** (`~/Library/Application Support/Google/Chrome` on macOS, `~/.config/google-chrome` on Linux, `%LOCALAPPDATA%\Google\Chrome\User Data` on Windows), so uninstalling keeps your bookmarks and settings. Delete it to remove everything.
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
#  - Linux: the .deb in Google's apt repository
#    (dl.google.com/linux/chrome/deb), with the SHA-256 of its Packages index.
# Requirements are conservative estimates: Google publishes OS versions but
# no hardware minimums.
targets:
  # The .deb is an `ar` archive whose data.tar.* member holds /opt/google/chrome.
  # `extract` cannot read `ar` and refuses the absolute symlinks in the data
  # member, so a small POSIX sh loop carves the member out of the .deb by its
  # ar headers (60 bytes each: name 16, size at offset 48, 10 digits) and tar
  # unpacks only ./opt/google/chrome. tar detects the compression itself
  # (xz today); it needs xz support, present on mainstream distributions.
  # The unpacked directory also holds the `google-chrome` launcher (a bash
  # script) and the product_logo PNGs used for the menu entry.
  "linux/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download Chrome
          url:
            linux/amd64: https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_154.0.8037.97-1_amd64.deb
            linux/arm64: https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_154.0.8037.97-1_arm64.deb
          checksum:
            linux/amd64: a4edbe95e9b01db6c9b97d7a1323121eda18362b5620df06abac1b59bee80053
            linux/arm64: e8b589908ac79a0b8bdb8b7fc56824a27221d56fb9757d4541065fe5d1fbf78e
          to: ${INSTALL_PATH}/.chrome.deb
          timeout: 20m
        - type: run
          title: Unpack Chrome
          command: |
            o=8; t=$(wc -c < .chrome.deb)
            while [ "$o" -lt "$t" ]; do
              h=$(dd if=.chrome.deb bs=1 skip="$o" count=60 2>/dev/null)
              n=$(printf '%s' "$h" | cut -c1-16)
              s=$(printf '%s' "$h" | cut -c49-58 | tr -d ' ')
              case "$n" in
                data.tar*)
                  tail -c +$((o+61)) .chrome.deb | head -c "$s" > .chrome-data.tar \
                    && mkdir -p chrome \
                    && tar -xf .chrome-data.tar -C chrome ./opt/google/chrome \
                    && rm -f .chrome-data.tar .chrome.deb
                  exit $?;;
              esac
              o=$((o+60+s+s%2))
            done
            echo "no data.tar member in the .deb" >&2; exit 1
          timeout: 15m
      uninstall:
        - type: run
          title: Remove Chrome
          command: rm -rf ./chrome ./.chrome-data.tar ./.chrome.deb
          timeout: 5m
          exit_on_failure: false
    expose:
      desktop:
        - name: Chrome
          path: ${INSTALL_PATH}/chrome/opt/google/chrome/google-chrome
          icon: ${INSTALL_PATH}/chrome/opt/google/chrome/product_logo_256.png
          categories: [Network, WebBrowser]

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
