calibre is a free, open-source e-book manager. It keeps a library of your books with their metadata and covers, converts between e-book formats, edits and views books, sends them to your reader, and can serve the library over your network. Its set of command-line tools, such as `ebook-convert`, make it just as useful in scripts as in the window.

![calibre's bookshelf view of a library](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/calibre/screenshots/bookshelf.png)

## Features

- **Library management**: browse your books by cover, shelf or table, search and sort by any field, and keep tags, series and custom columns.
- **Format conversion**: convert between many e-book formats, with options for the look, page setup, structure detection and table of contents.
- **Metadata**: download metadata and covers for a book, and edit or create metadata in any field.
- **E-book editor and viewer**: a built-in editor for the HTML, CSS and files inside a book, and a viewer for the major e-book formats.
- **Devices**: send books to your e-reader, converting to a format it supports when needed.
- **Content server**: share your library and read it from other devices on your network.
- **News**: download magazines and newspapers from the web into e-books.
- **Command-line tools**: `ebook-convert`, `ebook-meta`, `ebook-polish`, `calibredb` and more, exposed by this arrow.

![calibre's e-book conversion dialog](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/calibre/screenshots/convert.png)

![calibre's e-book editor](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/calibre/screenshots/editor.png)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | calibre's official DMG, as `calibre.app` in Applications, plus the command-line tools linked from inside the app. Requires macOS 14 or later. |
| Linux (x86_64 and ARM64) | calibre's official binary tarball for your processor, unpacked into Quiver's folder, with a desktop menu entry and the command-line tools. It is the same build calibre's own installer script puts in `/opt`, without needing root. |
| Windows (x64) | calibre's official 64-bit MSI, unpacked into Quiver's folder without installing system-wide (no administrator rights), a Start Menu shortcut, and the folder with the command-line tools added to your `Path`. Requires Windows 10 version 1809 or later. calibre publishes no Windows ARM64 build, so it is not offered. |

Every download is pinned to calibre 9.15.0 from the [official GitHub releases](https://github.com/kovidgoyal/calibre/releases) and verified against its SHA-256 checksum.

### Good to know

- **Run `quiver path setup` once** so your shell finds the commands in `~/.quiver/bin`. On Windows the folder holding them is added to your user `Path` instead; open a new terminal afterwards.
- **Your library and settings live outside Quiver's folder.** calibre keeps your books in a library folder you choose and its settings in your user profile, so uninstalling or updating the arrow leaves them in place.
- **calibre tells you about new versions but does not install them.** Updating comes through Quiver, which installs the release pinned in the new version of the arrow.
- **Linux needs a few system libraries**, as for calibre's own installer: glibc 2.34 or newer, and the X11/XCB libraries such as `libxcb-cursor0` and `libxcb-xinerama0` (plus `libegl1` and `libopengl0` on bare servers). If calibre fails on Wayland, start it as `QT_QPA_PLATFORM=xcb calibre`.
- **On Windows the MSI is only unpacked**, so Windows does not list calibre under Installed apps and file associations are not registered.
- **Already have calibre?** Quiver never replaces an app it did not install. If `calibre.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.
- **Minimum hardware**: calibre publishes none.

## License and trademarks

calibre is free software by Kovid Goyal and contributors, released under the [GNU General Public License, version 3](https://github.com/kovidgoyal/calibre/blob/master/LICENSE). This arrow only downloads calibre's official builds from its GitHub releases. The calibre name and logo belong to its author; the icon is calibre's own logo (`resources/images/calibre.svg`), the banner was generated from it, and the screenshots come from calibre's [user manual](https://manual.calibre-ebook.com/), whose conversion and editor images show older versions of the interface.

```arrow
schema: "arrow@v0"

metadata:
  name: calibre
  description: "The e-book manager: library, conversion, viewer, editor and command-line tools"
  license: GPL-3.0-only
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://calibre-ebook.com
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Kovid Goyal
      url: https://calibre-ebook.com
  media:
    icon: https://raw.githubusercontent.com/kovidgoyal/calibre/v9.15.0/resources/images/calibre.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/calibre/banner.svg
  tags:
    - ebooks
    - conversion
    - desktop
    - cli

# calibre 9.15.0, with the SHA-256 digests GitHub records for the release
# assets. calibre publishes no hardware minimums, so requirements are
# conservative estimates.
targets:
  # The official binary tarballs (what linux-installer.sh downloads). The
  # archive root holds the executables, lib/ and resources/ directly, so it is
  # unpacked into calibre/ and the tools are exposed from there.
  "linux/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download calibre
          url:
            linux/amd64: https://github.com/kovidgoyal/calibre/releases/download/v9.15.0/calibre-9.15.0-x86_64.txz
            linux/arm64: https://github.com/kovidgoyal/calibre/releases/download/v9.15.0/calibre-9.15.0-arm64.txz
          checksum:
            linux/amd64: 3f5301c0aa51e5fb2d5f6dcd04024ba4e86501ab328ce5d9d6760efccb887990
            linux/arm64: 15ab887f9d787809bc834ca0ea6408e981b409f0b23046c41c18de948eb50a38
          to: ${INSTALL_PATH}/.calibre.download
          timeout: 20m
        - type: extract
          title: Unpack calibre
          from: ${INSTALL_PATH}/.calibre.download
          to: ${INSTALL_PATH}/calibre
          timeout: 10m
    expose:
      desktop:
        - name: calibre
          path: ${INSTALL_PATH}/calibre/calibre
          icon: ${INSTALL_PATH}/calibre/resources/images/lt.png
          categories: [Office, Education]
      cli:
        - name: calibre
          path: ${INSTALL_PATH}/calibre/calibre
        - name: calibredb
          path: ${INSTALL_PATH}/calibre/calibredb
        - name: calibre-debug
          path: ${INSTALL_PATH}/calibre/calibre-debug
        - name: calibre-server
          path: ${INSTALL_PATH}/calibre/calibre-server
        - name: calibre-smtp
          path: ${INSTALL_PATH}/calibre/calibre-smtp
        - name: calibre-customize
          path: ${INSTALL_PATH}/calibre/calibre-customize
        - name: ebook-convert
          path: ${INSTALL_PATH}/calibre/ebook-convert
        - name: ebook-device
          path: ${INSTALL_PATH}/calibre/ebook-device
        - name: ebook-edit
          path: ${INSTALL_PATH}/calibre/ebook-edit
        - name: ebook-meta
          path: ${INSTALL_PATH}/calibre/ebook-meta
        - name: ebook-polish
          path: ${INSTALL_PATH}/calibre/ebook-polish
        - name: ebook-viewer
          path: ${INSTALL_PATH}/calibre/ebook-viewer
        - name: fetch-ebook-metadata
          path: ${INSTALL_PATH}/calibre/fetch-ebook-metadata
        - name: web2disk
          path: ${INSTALL_PATH}/calibre/web2disk
  # One DMG for both processors (universal); requires macOS 14 or later. The
  # desktop entry moves calibre.app to Applications and the CLI entries follow
  # it, linking to the launchers inside the bundle.
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download calibre
          url: https://github.com/kovidgoyal/calibre/releases/download/v9.15.0/calibre-9.15.0.dmg
          checksum: 1b3a7451175b73ae2baa28fe1bc1c53ee34d65b489881e7ec02c20f9e0ff6019
          to: ${INSTALL_PATH}/.calibre.download
          timeout: 30m
        - type: portable
          title: Install calibre
          from: ${INSTALL_PATH}/.calibre.download
          to: ${INSTALL_PATH}/Calibre
          timeout: 15m
    expose:
      desktop:
        - name: calibre
          path: auto
      cli:
        - name: calibre
          path: ${INSTALL_PATH}/Calibre/calibre.app/Contents/MacOS/calibre
        - name: calibredb
          path: ${INSTALL_PATH}/Calibre/calibre.app/Contents/MacOS/calibredb
        - name: calibre-debug
          path: ${INSTALL_PATH}/Calibre/calibre.app/Contents/MacOS/calibre-debug
        - name: calibre-server
          path: ${INSTALL_PATH}/Calibre/calibre.app/Contents/MacOS/calibre-server
        - name: calibre-smtp
          path: ${INSTALL_PATH}/Calibre/calibre.app/Contents/MacOS/calibre-smtp
        - name: calibre-customize
          path: ${INSTALL_PATH}/Calibre/calibre.app/Contents/MacOS/calibre-customize
        - name: ebook-convert
          path: ${INSTALL_PATH}/Calibre/calibre.app/Contents/MacOS/ebook-convert
        - name: ebook-device
          path: ${INSTALL_PATH}/Calibre/calibre.app/Contents/MacOS/ebook-device
        - name: ebook-edit
          path: ${INSTALL_PATH}/Calibre/calibre.app/Contents/MacOS/ebook-edit
        - name: ebook-meta
          path: ${INSTALL_PATH}/Calibre/calibre.app/Contents/MacOS/ebook-meta
        - name: ebook-polish
          path: ${INSTALL_PATH}/Calibre/calibre.app/Contents/MacOS/ebook-polish
        - name: ebook-viewer
          path: ${INSTALL_PATH}/Calibre/calibre.app/Contents/MacOS/ebook-viewer
        - name: fetch-ebook-metadata
          path: ${INSTALL_PATH}/Calibre/calibre.app/Contents/MacOS/fetch-ebook-metadata
        - name: web2disk
          path: ${INSTALL_PATH}/Calibre/calibre.app/Contents/MacOS/web2disk
  # Only a 64-bit x64 build exists for Windows. The MSI is unpacked with an
  # administrative extraction (no system-wide install, no elevation); it must
  # be downloaded to a name ending in .msi. `auto` finds calibre.exe, and the
  # folder holding it, with every calibre tool, is appended to the user Path.
  # Requires Windows 10 version 1809 or later.
  windows/amd64:
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download calibre
          url: https://github.com/kovidgoyal/calibre/releases/download/v9.15.0/calibre-64bit-9.15.0.msi
          checksum: 0f96ae06165c2419607c1c66726c091a78e89e08ea69f077cf3e2c884e800853
          to: ${INSTALL_PATH}/.calibre.download.msi
          timeout: 30m
        - type: portable
          title: Unpack calibre
          from: ${INSTALL_PATH}/.calibre.download.msi
          to: ${INSTALL_PATH}/calibre
          timeout: 15m
    expose:
      desktop:
        - name: calibre
          path: auto
      cli:
        - name: calibre
          path: auto
```
