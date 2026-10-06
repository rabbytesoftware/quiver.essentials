Spotify is a music, podcast and audiobook streaming service. The desktop app plays songs, albums, playlists and podcasts from Spotify's catalogue, with personalised mixes such as Discover Weekly, a listening queue shared across your devices, and the option to download tracks for offline play with a Premium subscription.

![Spotify's home screen](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/spotify/screenshots/home.jpg)

## Features

- **Music and podcasts in one app**: search a very large catalogue, follow artists and shows, and keep playlists and a library of liked songs.
- **Made for you**: Discover Weekly and other playlists built from what you listen to.
- **Spotify Connect**: start a song on one device and carry on, or control another device, from the app.
- **Free and Premium**: Spotify is free to use with ads; a Premium subscription removes the ads and allows offline downloads.

![Discover Weekly in the desktop app](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/spotify/screenshots/discover-weekly.jpg)

![Following a podcast](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/spotify/screenshots/podcasts.jpg)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | Spotify's official DMG for your processor, as `Spotify.app` in Applications. Requires macOS 13 or later. |
| Windows (x64 and ARM64) | Spotify's official full installer for your processor, run silently for your user. It adds its own Start Menu shortcut. Requires Windows 10 or later. |

Not supported: **Linux**. Spotify publishes its Linux client only as a Debian package, a Snap and a Flatpak, which need system-wide installation, and offers no tarball or AppImage that Quiver could install without administrator rights.

### Good to know

- **Spotify keeps itself up to date.** Quiver installs the current build; from then on Spotify's own updater installs new versions, as it does when installed by hand.
- **The downloads are not versioned, so they are not checksum-verified.** Spotify serves its installers from fixed addresses that it replaces in place with each release, which can be as often as weekly, so Quiver cannot pin a checksum without the install breaking after the next release. Quiver therefore installs whatever Spotify currently publishes at those addresses, downloaded over HTTPS directly from Spotify, without a checksum check.
- **On Windows, Spotify installs into your user profile** (`%APPDATA%\Spotify`), not into Quiver's folder, and runs without administrator rights. Uninstalling through Quiver runs Spotify's own uninstaller.
- **On macOS your data stays outside the app** (`~/Library/Application Support/Spotify` and its caches), so removing the arrow does not delete your cache or downloaded music.
- **Already have Spotify?** Quiver never replaces an app it did not install. If `Spotify.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.
- **A Spotify account is required** to listen.

## License and trademarks

Spotify is proprietary software by Spotify AB, free to use under its [Terms of Use](https://www.spotify.com/legal/end-user-agreement/). This arrow only downloads Spotify's official builds from Spotify's own servers. The Spotify name and logo are trademarks of Spotify AB; the icon is the logo from Spotify's [design guidelines](https://developer.spotify.com/documentation/design) (with its canvas padded to a square), the banner is a promotional image from the same Microsoft Store listing, cropped to 2:1, and the screenshots come from Spotify's official Microsoft Store listing.

```arrow
schema: "arrow@v0"

metadata:
  name: Spotify
  description: Music and podcast streaming from Spotify
  license: Proprietary
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://www.spotify.com/download/
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Spotify AB
      url: https://www.spotify.com
  media:
    icon: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/spotify/icon.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/spotify/banner.jpg
  tags:
    - music
    - podcasts
    - desktop

# Spotify 1.3.3.264 (g-hash daf3b824 on Windows), released 2026-10-01.
# LIMITATION: Spotify offers no versioned URLs. Every download below is a
# rolling "latest" address that Spotify overwrites on each release, so no
# checksum can be pinned: a pinned digest would stop matching after the next
# release and break the install. The downloads are therefore unverified by
# Quiver (they come over HTTPS straight from Spotify's CDN). Spotify updates
# itself after install on every platform. Requirements are conservative estimates, since
# Spotify publishes no hardware minimums.
#
# Linux is deliberately absent: Spotify ships Linux only as a .deb (apt),
# Snap and Flatpak, all of which need root, and no portable archive.
targets:
  # Per-arch DMG holding Spotify.app; Homebrew's cask lists macOS 13 or later.
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download Spotify
          url:
            darwin/arm64: https://download.scdn.co/SpotifyARM64.dmg
            darwin/amd64: https://download.scdn.co/Spotify.dmg
          to: ${INSTALL_PATH}/.spotify.download
          timeout: 20m
        - type: portable
          title: Install Spotify
          from: ${INSTALL_PATH}/.spotify.download
          to: ${INSTALL_PATH}/Spotify
          timeout: 10m
    expose:
      desktop:
        - name: Spotify
          path: auto

  # Spotify's full (offline) installer, one per architecture. `/silent` installs
  # per user into %APPDATA%\Spotify without elevation (winget's manifest for
  # Spotify.Spotify uses `/silent /skip-app-launch` with scope user and
  # elevation prohibited) and creates its own Start Menu shortcut, so there is
  # no `expose`. The uninstaller is the Spotify.exe the installer leaves in
  # %APPDATA%\Spotify.
  "windows/*":
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download the Spotify installer
          url:
            windows/amd64: https://download.scdn.co/SpotifyFullSetupX64.exe
            windows/arm64: https://download.scdn.co/SpotifyFullSetupARM64.exe
          to: ${INSTALL_PATH}/SpotifySetup.exe
          timeout: 20m
        - type: run
          title: Install Spotify
          command: '.\SpotifySetup.exe /silent /skip-app-launch >nul 2>&1 <nul'
          timeout: 15m
      uninstall:
        - type: run
          title: Uninstall Spotify
          command: 'if exist "%APPDATA%\Spotify\Spotify.exe" "%APPDATA%\Spotify\Spotify.exe" /uninstall /silent & del /f /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Spotify.lnk"'
          timeout: 5m
          exit_on_failure: false
```
