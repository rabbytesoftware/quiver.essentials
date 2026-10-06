VLC is a free, open-source media player from the VideoLAN project. It plays most audio and video files, discs and network streams without needing extra codec packs, and can also convert, record and stream media.

![VLC playing a video on macOS, with its media information window](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/vlc/screenshots/playback.jpg)

## Features

- **Plays almost everything**: files, discs, webcams, devices and network streams, with the codecs built in.
- **Subtitles and audio tracks**: loads subtitle files and switches between audio and subtitle tracks while playing.
- **Audio and video effects**: an equalizer, compressor and spatializer for sound, and filters for the picture.
- **Streaming**: plays network streams, and VideoLAN's page also lists it as a media converter.
- **Free and open source**: its source code is published by VideoLAN.

![VLC's audio effects window with the equalizer](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/vlc/screenshots/audio-effects.jpg)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | VideoLAN's official universal DMG, as `VLC.app` in Applications. |
| Windows (x64 and ARM64) | VideoLAN's official portable `.zip` build, unpacked into Quiver's folder, and a Start Menu shortcut. |
| Linux | **Not supported.** VideoLAN publishes no Linux binary: it offers source code and points to your distribution's package or to its Snap, and Snap and Flatpak both need a system-wide service (snapd, Flatpak) rather than a per-user install. |

Every download is pinned to VLC 3.0.24 on [get.videolan.org](https://get.videolan.org/vlc/3.0.24/) and verified against the SHA-256 checksum VideoLAN publishes next to each file.

### Good to know

- **Updates come through Quiver.** VLC can tell you when a new version exists but does not install it itself.
- **Your preferences live outside Quiver's folder** (`~/Library/Preferences/org.videolan.vlc` and `~/Library/Application Support/org.videolan.vlc` on macOS, `%APPDATA%\vlc` on Windows), so uninstalling keeps them.
- **The Windows build is the portable zip**, so it does not register file types or the "Open with" entry the way VideoLAN's installer does; use VLC's own Preferences, or Windows' "Open with", to make it your default player.
- **Already have VLC?** Quiver never replaces an app it did not install. If `VLC.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.
- **Version**: this arrow installs VLC 3.0.24, the release VideoLAN's download page currently offers.
- The screenshots are from VideoLAN's website and show an older release (VLC 2.2 on macOS); the current interface looks similar but not identical.

## License and trademarks

VLC is free software by the VideoLAN project, released under the [GNU General Public License, version 2 or later](https://www.videolan.org/legal.html) (its libVLC engine under the LGPL). This arrow only downloads VideoLAN's official builds from get.videolan.org. The VLC name and cone logo belong to the VideoLAN non-profit organisation; the icon is VLC's app icon from its [source repository](https://code.videolan.org/videolan/vlc), the banner was generated from it, and the screenshots come from [videolan.org](https://www.videolan.org/vlc/screenshots.html).

```arrow
schema: "arrow@v0"

metadata:
  name: VLC media player
  description: The free and open-source media player that plays almost everything
  license: GPL-2.0-or-later
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://www.videolan.org/vlc/
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: VideoLAN
      url: https://www.videolan.org
  media:
    icon: https://code.videolan.org/videolan/vlc/-/raw/3.0.24/extras/package/macosx/asset_sources/vlc_app_icon.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/vlc/banner.svg
  tags:
    - media-player
    - video
    - audio
    - desktop

# VLC 3.0.24 from get.videolan.org, with the .sha256 files VideoLAN publishes
# beside each download. VideoLAN ships no Linux binary (only source, distro
# packages and a Snap), so there is no linux target. Requirements are
# conservative estimates: VideoLAN publishes no hardware minimums.
targets:
  # One universal DMG (Intel and Apple silicon).
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download VLC
          url: https://get.videolan.org/vlc/3.0.24/macosx/vlc-3.0.24-universal.dmg
          checksum: 2c8e89f7f42e53c2fb0e87b6dfa39b49f1364b25080aaa2e476ac74c0d7beb3c
          to: ${INSTALL_PATH}/.vlc.download
          timeout: 15m
        - type: portable
          title: Install VLC
          from: ${INSTALL_PATH}/.vlc.download
          to: ${INSTALL_PATH}/VLC
          timeout: 10m
    expose:
      desktop:
        - name: VLC
          path: auto

  # The portable zip unpacks into a `vlc-3.0.24` folder holding vlc.exe.
  "windows/*":
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download VLC
          url:
            windows/amd64: https://get.videolan.org/vlc/3.0.24/win64/vlc-3.0.24-win64.zip
            windows/arm64: https://get.videolan.org/vlc/3.0.24/winarm64/vlc-3.0.24-winarm64.zip
          checksum:
            windows/amd64: fcf30850371ad10c9373cc4f0f4501e7dee49e3e9ae9f20c72fb2661a1ca6323
            windows/arm64: f096226211f67f8e06e50cd0d6a948d842db128ff22a676dc1ca1cc6114baba5
          to: ${INSTALL_PATH}/.vlc.download.zip
          timeout: 15m
        - type: extract
          title: Unpack VLC
          from: ${INSTALL_PATH}/.vlc.download.zip
          to: ${INSTALL_PATH}/app
          timeout: 5m
    expose:
      desktop:
        - name: VLC
          path: ${INSTALL_PATH}/app/vlc-3.0.24/vlc.exe
```
