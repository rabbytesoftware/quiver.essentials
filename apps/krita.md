Krita is a free and open-source painting program made by artists for artists: concept art, illustration, comics, textures and hand-drawn animation. It is built around the brush engine, with over a hundred brushes, layers, filters and animation tools. Krita is developed by the KDE community and supported by the Krita Foundation.

![Painting an illustration in Krita](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/krita/screenshots/painting.jpg)

## Features

- **Brushes and brush engines**: over 100 brushes and nine brush engines, from colour smudge to particle and filter brushes, with three kinds of stabilizers for smooth lines.
- **Layers**: paint, vector, filter, group and file layers, with selections and transforms.
- **Animation**: a 2D animation workspace with a timeline, onion skinning, audio and export to video.
- **Drawing assistants**: vanishing points, ellipses and more, plus wrap-around mode for seamless textures.
- **Colour management and HDR**: ICC and OpenColorIO colour management, and HDR painting.
- **Vector and text tools**, PSD support and a Python scripting API.

![Adjusting curves with a filter in Krita](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/krita/screenshots/filters.jpg)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | Krita's official universal DMG, as `krita.app` in Applications. Requires macOS 10.15 or later. |
| Linux (x86_64) | Krita's official AppImage and a desktop menu entry. Krita publishes no AppImage for ARM. |
| Windows (x64) | Krita's official portable build, unpacked into Quiver's folder, and a Start Menu shortcut. Krita publishes no Windows build for ARM. |

Every download is pinned to an official Krita release from [download.kde.org](https://download.kde.org/stable/krita/) and verified against the SHA-256 checksum published there.

### Good to know

- **This is Krita 5.3**, the version krita.org recommends for download. Krita 6, built on Qt 6, is released alongside it.
- **Updates come through Quiver.** These builds do not update themselves.
- **Your resources and settings live outside Quiver's folder** (`~/Library/Application Support/krita` on macOS, `~/.local/share/krita` on Linux, `%APPDATA%\krita` on Windows), so uninstalling keeps your brushes and settings.
- **Already have Krita?** Quiver never replaces an app it did not install. If `krita.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.

## License and trademarks

Krita is free software released as a whole under the [GNU General Public License, version 3](https://invent.kde.org/graphics/krita/-/blob/master/COPYING) by the Krita developers and the KDE community; individual files may carry compatible licenses. This arrow only downloads Krita's official builds from download.kde.org. The Krita name and logo belong to the Krita Foundation; the icon is Krita's app icon from its [source repository](https://invent.kde.org/graphics/krita), the banner was generated from it, and the screenshots come from Krita's official Microsoft Store listing.

```arrow
schema: "arrow@v0"

metadata:
  name: Krita
  description: Free digital painting for illustrators, concept artists and animators
  license: GPL-3.0-only
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://krita.org
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Krita Foundation and the KDE community
      url: https://krita.org
  media:
    icon: https://invent.kde.org/graphics/krita/-/raw/v6.0.4/krita/pics/branding/default/1024-apps-krita.png
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/krita/banner.svg
  tags:
    - painting
    - illustration
    - desktop

# Krita 5.3.4, the release krita.org offers for download, with the SHA-256
# download.kde.org publishes next to each file. Krita ships Linux and Windows
# for x86_64 only. Requirements are conservative estimates: Krita publishes
# none for these builds.
targets:
  # A type-2 AppImage, unpacked in place by `portable`.
  linux/amd64:
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download Krita
          url: https://download.kde.org/stable/krita/5.3.4/krita-5.3.4-x86_64.AppImage
          checksum: 217c2f3cf17c2c604deb8708253ee6d2bd884f508424c20e788c562ddc50f24d
          to: ${INSTALL_PATH}/.krita.download
          timeout: 20m
        - type: portable
          title: Install Krita
          from: ${INSTALL_PATH}/.krita.download
          to: ${INSTALL_PATH}/Krita
          timeout: 10m
    expose:
      desktop:
        - name: Krita
          path: auto
          categories: [Graphics, RasterGraphics]

  # One universal (x86_64 + arm64) DMG; requires macOS 10.15 or later.
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download Krita
          url: https://download.kde.org/stable/krita/5.3.4/krita-5.3.4-signed.dmg
          checksum: 8e66539e38b8becfd31093a7701144c340c1789370b75e10a3703322739275d7
          to: ${INSTALL_PATH}/.krita.download
          timeout: 20m
        - type: portable
          title: Install Krita
          from: ${INSTALL_PATH}/.krita.download
          to: ${INSTALL_PATH}/Krita
          timeout: 10m
    expose:
      desktop:
        - name: Krita
          path: auto

  # The portable zip unpacks into krita-x64-5.3.4/.
  windows/amd64:
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download Krita
          url: https://download.kde.org/stable/krita/5.3.4/krita-x64-5.3.4.zip
          checksum: 4bf5b51100b30fa68edd12b995932b82f8a0080ef115b5461941fa2d186d126c
          to: ${INSTALL_PATH}/.krita.download
          timeout: 20m
        - type: extract
          title: Unpack Krita
          from: ${INSTALL_PATH}/.krita.download
          to: ${INSTALL_PATH}/Krita
          timeout: 10m
    expose:
      desktop:
        - name: Krita
          path: ${INSTALL_PATH}/Krita/krita-x64-5.3.4/bin/krita.exe
```
