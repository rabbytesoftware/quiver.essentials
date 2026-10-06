Pumble is a team chat app from CAKE.com with a free plan: channels for topics and projects, direct messages, threads, file sharing, voice and video calls with screen sharing, and integrations with other tools.

![Pumble on desktop and mobile](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/pumble/screenshots/desktop-and-mobile.png)

## Features

- **Channels and direct messages**: public and private channels, one-to-one and group conversations.
- **Threads**: keep replies together so busy channels stay readable.
- **Files and search**: share files in conversations and search messages and attachments.
- **Voice and video calls**: calls and meetings with screen sharing.
- **Guests and permissions**: invite people from outside the team and control what they can see.
- **Integrations**: connect other tools so their updates arrive in Pumble.

![Channels and a thread in Pumble](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/pumble/screenshots/channels-and-threads.png)

![A video call in Pumble](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/pumble/screenshots/video-call.png)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | Pumble's universal DMG, as `Pumble.app` in Applications. Requires macOS 12 or later. |
| Linux (x86_64) | The contents of Pumble's official `.deb` package, unpacked in Quiver's folder, with a desktop menu entry. Pumble publishes no Linux build for ARM. Needs `ar` (binutils) and `tar` with xz support, or `dpkg-deb`. |
| Windows (x64) | Pumble's official installer, run silently for your user. |
| Windows (ARM64) | Not supported: Pumble's Windows installer contains only an x64 build. |

Every download is pinned to Pumble 1.4.71 from pumble.com and verified against its SHA-256 checksum. Pumble publishes no checksums, so the digests were computed from the files at the time of writing.

### Good to know

- **Pumble checks for updates itself.** Its builds ship with an update feed on pumble.com; Quiver installs the version pinned here, and a newer Quiver release of this arrow moves you to a newer one.
- **Linux is a rootless repackaging of the `.deb`.** Pumble publishes Linux only as `.deb` and `.rpm`, so Quiver unpacks the package into its own folder without installing it. The setuid sandbox helper is therefore not set up, and on distributions that restrict unprivileged user namespaces (such as Ubuntu 24.04 and later) Pumble may refuse to start without `--no-sandbox`.
- **On Windows, Pumble installs into your user profile**, not into Quiver's folder, and adds its own shortcuts. Uninstalling through Quiver runs the uninstaller Pumble registered for your user.
- **Already have Pumble?** Quiver never replaces an app it did not install. If `Pumble.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.
- **Requirements**: Pumble does not publish hardware minimums; Quiver asks for 2 cores and 4 GB of memory as a conservative estimate.

## License and trademarks

Pumble is proprietary software by CAKE.com, free to use under its [terms of service](https://pumble.com/terms-of-service). This arrow only downloads Pumble's official builds from pumble.com. The Pumble name and logo are trademarks of CAKE.com; the icon is Pumble's app icon and the banner is its social image, both as published on pumble.com, and the screenshots come from [pumble.com](https://pumble.com).

```arrow
schema: "arrow@v0"

metadata:
  name: Pumble
  description: Free team chat with channels, threads and video calls
  license: Proprietary
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://pumble.com
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: CAKE.com
      url: https://cake.com
  media:
    icon: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/pumble/icon.png
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/pumble/banner.png
  tags:
    - chat
    - team
    - desktop

# Pumble 1.4.71, the versioned files linked from pumble.com/download (an
# unversioned update feed also exists at pumble.com/download/desktop/<os>/).
# Pumble publishes only SHA-512 in its update feed, so the SHA-256 digests
# below were computed from the downloaded files. Pumble publishes no hardware
# minimums; requirements are conservative estimates.
targets:
  # Linux ships only as .deb/.rpm (amd64 only). Quiver cannot unpack a .deb,
  # so a `run` step does it rootlessly into the workdir (dpkg-deb, else
  # ar + tar), which needs an `uninstall`.
  linux/amd64:
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download Pumble
          url: https://pumble.com/download/desktop/linux/Pumble-linux-1.4.71.deb
          checksum: cdf9ca78d2b63c89f9e6d949b022e39bfe91d448edc31a4fa9319b452eacbe85
          to: ${INSTALL_PATH}/.pumble.deb
          timeout: 10m
        - type: run
          title: Unpack Pumble
          command: 'mkdir -p app && (dpkg-deb -x .pumble.deb app || (cd app && ar x ../.pumble.deb data.tar.xz && tar -xf data.tar.xz && rm -f data.tar.xz))'
          timeout: 5m
      uninstall:
        - type: run
          title: Remove Pumble
          command: 'rm -rf app .pumble.deb'
          timeout: 2m
          exit_on_failure: false
    expose:
      desktop:
        - name: Pumble
          path: ${INSTALL_PATH}/app/opt/Pumble/pumble-desktop
          icon: ${INSTALL_PATH}/app/usr/share/icons/hicolor/256x256/apps/pumble-desktop.png
          categories: [Network, Office]

  # One universal (x86_64 + arm64) DMG; requires macOS 12 or later.
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download Pumble
          url: https://pumble.com/download/desktop/mac/Pumble-mac-1.4.71.dmg
          checksum: 96fb5fb2044c92526d085bdb6d6940c5e6a65b8575506305697f91a5d493cd29
          to: ${INSTALL_PATH}/.pumble.download
          timeout: 15m
        - type: portable
          title: Install Pumble
          from: ${INSTALL_PATH}/.pumble.download
          to: ${INSTALL_PATH}/Pumble
          timeout: 10m
    expose:
      desktop:
        - name: Pumble
          path: auto

  # NSIS (electron-builder) installer carrying an x64 payload only, so ARM64
  # is not claimed. /S is silent and /currentuser asks for a per-user install
  # (into %LOCALAPPDATA%\Programs); the installer adds its own shortcuts, so
  # there is no `expose`. `uninstall` finds the uninstall command Pumble
  # registered under HKCU by display name, as the exact key name is unknown.
  windows/amd64:
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download the Pumble installer
          url: https://pumble.com/download/desktop/windows/Pumble-win-1.4.71.exe
          checksum: ce9c0373de437c7975029690c1875f096b63377ee8b31fb3efec0ed95aac1361
          to: ${INSTALL_PATH}/PumbleSetup.exe
          timeout: 15m
        - type: run
          title: Install Pumble
          command: '.\PumbleSetup.exe /S /currentuser'
          timeout: 10m
      uninstall:
        - type: run
          title: Uninstall Pumble
          command: 'powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-ChildItem HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall | Get-ItemProperty | Where-Object { $_.DisplayName -like ''Pumble*'' } | ForEach-Object { Start-Process -Wait -FilePath cmd.exe -ArgumentList ''/c'', $_.QuietUninstallString }"'
          timeout: 5m
          exit_on_failure: false
```
