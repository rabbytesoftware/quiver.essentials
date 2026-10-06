Blender is a free and open-source 3D creation suite. It covers the whole pipeline in one program: modeling, sculpting, rigging, animation, simulation, rendering, compositing, motion tracking and video editing. It is developed in the open by the Blender Foundation and a community of contributors, and is used for films, games, visualisation and 3D printing.

![Blender's default scene: the 3D viewport, outliner, properties editor and timeline](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/blender/screenshots/default-scene.jpg)

## Features

- **Modeling and sculpting**: polygon modeling tools and a sculpting mode with brushes for organic shapes.
- **Rendering**: the path-tracing engine Cycles and the real-time engine EEVEE, with a built-in node-based compositor.
- **Animation and rigging**: armatures, shape keys, a timeline and graph editor, and Grease Pencil for 2D animation in 3D space.
- **Simulation and geometry nodes**: physics simulations and procedural modeling with node graphs.
- **Video editing**: a video sequence editor and motion tracking.
- **Python scripting**: the interface and many tools are scriptable, and add-ons extend the program.

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| Linux (x86_64) | Blender's official `.tar.xz` build, unpacked into Quiver's folder, with a desktop menu entry and `blender` on your `PATH`. Needs a 64-bit distribution with glibc 2.28 or newer. Blender publishes no Linux ARM build. |
| macOS (Apple silicon) | Blender's official DMG, as `Blender.app` in Applications, and `blender` on your `PATH`. Requires macOS 13 (Ventura) or later. Intel Macs are not supported by Blender 5; Blender 4.5 LTS was the last release for them. |
| Windows (x64 and ARM64) | Blender's official portable `.zip` for your processor, unpacked into Quiver's folder, with a Start Menu shortcut and `blender` on your `Path`. Requires Windows 8.1 (64-bit) or later. |

Every download is pinned to **Blender 5.2.2, the current Long-Term Support (LTS) release**, from [download.blender.org](https://download.blender.org/release/Blender5.2/) and verified against the SHA-256 checksum Blender publishes next to it. Blender lists 4 CPU cores, 8 GB of RAM and a GPU with 2 GB of VRAM and OpenGL 4.3 as its minimum on Windows and Linux, and 8 GB of RAM on Apple silicon.

Run `quiver path setup` once so your shell finds `~/.quiver/bin` (Linux and macOS), then try `blender --version`.

### Good to know

- **This is Blender 5.2 LTS.** The LTS line receives only bug fixes for two years. Updates come through Quiver: Blender does not update itself.
- **Your preferences and add-ons live outside Quiver's folder** (`~/.config/blender` on Linux, `~/Library/Application Support/Blender` on macOS, `%APPDATA%\Blender Foundation\Blender` on Windows), so uninstalling keeps them and a new Blender version can import them.
- **The Windows build is the portable zip**, not the installer, so no administrator rights are needed and Blender's file associations (double-clicking `.blend` files) are not set up.
- **Disk space**: Blender needs several gigabytes once unpacked, and the download is 270 to 400 MB.
- **Already have Blender?** Quiver never replaces an app it did not install. If `Blender.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.

## License and trademarks

Blender is free software released under the [GNU General Public License](https://www.blender.org/about/license/) (version 2 or later for its source code; version 3 or later for binary distributions), by the Blender Foundation and contributors. This arrow only downloads Blender's official builds from download.blender.org. The Blender name and logo are trademarks of the Blender Foundation; the icon is Blender's app icon from its [source repository](https://projects.blender.org/blender/blender) (mirrored at [github.com/blender/blender](https://github.com/blender/blender)), the banner was generated from it, and the screenshot comes from the official [Blender 5.2 LTS manual](https://docs.blender.org/manual/en/5.2/interface/window_system/introduction.html) (licensed CC BY-SA 4.0 by the Blender Documentation Team). The screenshot shows a 5.0 pre-release build, with the same layout.

```arrow
schema: "arrow@v0"

metadata:
  name: Blender
  description: The free and open-source 3D creation suite
  license: GPL-3.0-or-later
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://www.blender.org
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Blender Foundation and contributors
      url: https://www.blender.org
  media:
    icon: https://raw.githubusercontent.com/blender/blender/v5.2.2/release/freedesktop/icons/scalable/apps/blender.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/blender/banner.svg
  tags:
    - 3d
    - animation
    - rendering
    - desktop

# Blender 5.2.2, the current Long-Term Support release, with the SHA-256 from
# download.blender.org/release/Blender5.2/blender-5.2.2.sha256 (the macOS,
# Linux x64 and Windows x64 files were also hashed after downloading).
# Blender 5 ships no Intel macOS and no Linux ARM build, so those are not
# claimed. Requirements are Blender's published minimums
# (blender.org/download/requirements).
targets:
  # Tarball with one top-level folder, blender-5.2.2-linux-x64, which holds
  # the blender binary and its blender.svg icon.
  linux/amd64:
    requirements:
      cpu_cores: 4
      ram_gb: 8
      disk_gb: 5
    lifecycle:
      install:
        - type: fetch
          title: Download Blender
          url: https://download.blender.org/release/Blender5.2/blender-5.2.2-linux-x64.tar.xz
          checksum: 84098912789dc450e95697c4184fb8a90acbe5111c2ba4aede3fecb57806a168
          to: ${INSTALL_PATH}/.blender.download
          timeout: 30m
        - type: extract
          title: Unpack Blender
          from: ${INSTALL_PATH}/.blender.download
          to: ${INSTALL_PATH}/Blender
          timeout: 15m
    expose:
      cli:
        - name: blender
          path: ${INSTALL_PATH}/Blender/blender-5.2.2-linux-x64/blender
      desktop:
        - name: Blender
          path: ${INSTALL_PATH}/Blender/blender-5.2.2-linux-x64/blender
          icon: ${INSTALL_PATH}/Blender/blender-5.2.2-linux-x64/blender.svg
          categories: [Graphics, 3DGraphics]

  # Apple silicon only (Blender 5 requires it, on macOS 13 or later). The DMG
  # holds Blender.app at its top level; `portable` places it and the desktop
  # entry moves it to Applications, taking the CLI entry along.
  darwin/arm64:
    requirements:
      cpu_cores: 4
      ram_gb: 8
      disk_gb: 5
    lifecycle:
      install:
        - type: fetch
          title: Download Blender
          url: https://download.blender.org/release/Blender5.2/blender-5.2.2-macos-arm64.dmg
          checksum: dc4125399b8bfefe283cc1624d6cfc7809d1cac20ace51072127eb371f31f210
          to: ${INSTALL_PATH}/.blender.download
          timeout: 30m
        - type: portable
          title: Install Blender
          from: ${INSTALL_PATH}/.blender.download
          to: ${INSTALL_PATH}/Blender
          timeout: 15m
    expose:
      desktop:
        - name: Blender
          path: auto
      cli:
        - name: blender
          path: ${INSTALL_PATH}/Blender/Blender.app/Contents/MacOS/Blender

  # Portable zips with one top-level folder named after the build. The two
  # architectures differ only in the downloads and the folder name.
  _windows:
    requirements:
      cpu_cores: 4
      ram_gb: 8
      disk_gb: 5
    lifecycle:
      install:
        - type: fetch
          title: Download Blender
          url:
            windows/amd64: https://download.blender.org/release/Blender5.2/blender-5.2.2-windows-x64.zip
            windows/arm64: https://download.blender.org/release/Blender5.2/blender-5.2.2-windows-arm64.zip
          checksum:
            windows/amd64: 3849d17a682cba006075aaa3f3597ecb5c9c30ec31035b2e092c53e40679b535
            windows/arm64: 2e90b53c9443cc56d2be75a61550a38e4aba942c8cded046ceff98ed58ebc67b
          to: ${INSTALL_PATH}/.blender.download
          timeout: 30m
        - type: extract
          title: Unpack Blender
          from: ${INSTALL_PATH}/.blender.download
          to: ${INSTALL_PATH}/Blender
          timeout: 15m

  # blender-launcher.exe is the windowed launcher (no console), blender.exe
  # the command-line program; both live in the same folder.
  windows/amd64:
    base: _windows
    expose:
      cli:
        - name: blender
          path: ${INSTALL_PATH}/Blender/blender-5.2.2-windows-x64/blender.exe
      desktop:
        - name: Blender
          path: ${INSTALL_PATH}/Blender/blender-5.2.2-windows-x64/blender-launcher.exe

  windows/arm64:
    base: _windows
    expose:
      cli:
        - name: blender
          path: ${INSTALL_PATH}/Blender/blender-5.2.2-windows-arm64/blender.exe
      desktop:
        - name: Blender
          path: ${INSTALL_PATH}/Blender/blender-5.2.2-windows-arm64/blender-launcher.exe
```
