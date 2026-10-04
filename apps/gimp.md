GIMP, the GNU Image Manipulation Program, is a free and open-source image editor for photo retouching, image composition and image authoring. Photographers use it to restore and enhance pictures, artists to paint and compose, and designers to produce icons and interface graphics; it can also be scripted and extended with plug-ins.

![Painting an illustration in GIMP](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/gimp/screenshots/painting.jpg)

## Features

- **Photo manipulation**: retouching, restoring and creative composites, with curves, levels and a full set of colour tools.
- **Non-destructive filters**: filters stay editable after they are applied, so you can tweak them later without redoing your work.
- **Layers, channels and paths**: work on several at once with multi-layer selection.
- **Painting and design**: brushes, text with editable outlines, and tools for icons and interface mockups.
- **Wide file support**: GIMP's own XCF plus common formats, including JPEG XL and QOI.
- **Scriptable and extensible**: plug-ins and scripts in Python 3, Script-Fu, C and more.

![Adjusting a photo with Curves in GIMP](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/gimp/screenshots/photo-editing.jpg)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | GIMP's official DMG for your processor, as `GIMP.app` in Applications. Requires macOS 11 or later. |
| Linux (x86_64 and ARM64) | GIMP's official AppImage for your processor and a desktop menu entry. GIMP supports it on Debian 13 or a comparable distribution. |
| Windows (x64 and ARM64) | GIMP's official installer, run silently for your user. It adds its own Start Menu shortcut. Requires Windows 10 version 1903 or later. |

Every download is pinned to an official GIMP release from [download.gimp.org](https://download.gimp.org/gimp/) and verified against the SHA-256 checksum GIMP publishes for it.

### Good to know

- **Updates come through Quiver.** GIMP can tell you when a new version is out, but does not install it itself.
- **Your settings, brushes and plug-ins live outside Quiver's folder** (GIMP's profile in your user folder), so uninstalling keeps them.
- **On Windows, GIMP installs into your user profile**, not into Quiver's folder. Uninstalling through Quiver runs GIMP's own uninstaller.
- **Already have GIMP?** Quiver never replaces an app it did not install. If `GIMP.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.

## License and trademarks

GIMP is free software released under the [GNU General Public License, version 3 or later](https://gitlab.gnome.org/GNOME/gimp/-/blob/master/COPYING), by the GIMP team. This arrow only downloads GIMP's official builds from download.gimp.org. The GIMP name and the Wilber logo belong to the GIMP project; the icon is GIMP's logo from its [gimp-data repository](https://gitlab.gnome.org/GNOME/gimp-data), the banner was generated from it, and the screenshots come from GIMP's official Microsoft Store listing.

```arrow
schema: "arrow@v0"

metadata:
  name: GIMP
  description: The free and open-source image editor
  license: GPL-3.0-or-later
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://www.gimp.org
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: The GIMP team
      url: https://www.gimp.org
  media:
    icon: https://gitlab.gnome.org/GNOME/gimp-data/-/raw/fe4ecc0bf70fc8ff3bd929ce6abdd50fb5621072/images/logo/gimp-logo.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/gimp/banner.svg
  tags:
    - image-editing
    - photo
    - desktop

# GIMP 3.2.6, with the SHA-256 GIMP publishes for each file in
# www.gimp.org/gimp_versions.json. Requirements are conservative estimates:
# GIMP publishes OS versions but no hardware minimums.
targets:
  # Type-2 AppImages, unpacked in place by `portable`; GIMP lists Debian 13
  # as the minimum it supports them on.
  "linux/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download GIMP
          url:
            linux/amd64: https://download.gimp.org/gimp/v3.2/linux/GIMP-3.2.6-x86_64.AppImage
            linux/arm64: https://download.gimp.org/gimp/v3.2/linux/GIMP-3.2.6-aarch64.AppImage
          checksum:
            linux/amd64: 79ea41bc9b06f78fda181849a9ca8e42d83f1124dedb756f4d52352e2465010f
            linux/arm64: d1b8271e440dc4e36065ca25f219c0534abd2dfb43aeb033c76b16832d395e19
          to: ${INSTALL_PATH}/.gimp.download
          timeout: 20m
        - type: portable
          title: Install GIMP
          from: ${INSTALL_PATH}/.gimp.download
          to: ${INSTALL_PATH}/GIMP
          timeout: 10m
    expose:
      desktop:
        - name: GIMP
          path: auto
          categories: [Graphics, RasterGraphics, Photography]

  # One DMG per processor; requires macOS 11 or later.
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download GIMP
          url:
            darwin/arm64: https://download.gimp.org/gimp/v3.2/macos/gimp-3.2.6-arm64.dmg
            darwin/amd64: https://download.gimp.org/gimp/v3.2/macos/gimp-3.2.6-x86_64.dmg
          checksum:
            darwin/arm64: 854573aec2be6a185aa021109c3c0ca94f210379204b704231bdd191b4060294
            darwin/amd64: ebe633642445d4d6fc6b68e7be7ca581c0b28c18dc9de7747849528c982e5677
          to: ${INSTALL_PATH}/.gimp.download
          timeout: 20m
        - type: portable
          title: Install GIMP
          from: ${INSTALL_PATH}/.gimp.download
          to: ${INSTALL_PATH}/GIMP
          timeout: 10m
    expose:
      desktop:
        - name: GIMP
          path: auto

  # One Inno Setup installer for x64 and ARM64, run per user (/CURRENTUSER,
  # the scope GIMP's WinGet manifest uses): it installs outside the workdir
  # and creates its own Start Menu shortcut, so there is no `expose` here.
  # `uninstall` runs the quiet uninstaller Inno registers under the product
  # code GIMP-3_is1. Requires Windows 10 version 1903 or later.
  "windows/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download the GIMP installer
          url: https://download.gimp.org/gimp/v3.2/windows/gimp-3.2.6-setup.exe
          checksum: 9337cccbc01d4098ee7a3dab215b3afbe6ece99c5287c92441d6f12cf541ebca
          to: ${INSTALL_PATH}/GIMPSetup.exe
          timeout: 20m
        - type: run
          title: Install GIMP
          command: '.\GIMPSetup.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /CURRENTUSER'
          timeout: 15m
      uninstall:
        - type: run
          title: Uninstall GIMP
          command: 'for /f "tokens=2,*" %a in (''reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\GIMP-3_is1" /v QuietUninstallString ^| findstr REG_SZ'') do %b /VERYSILENT /SUPPRESSMSGBOXES /NORESTART'
          timeout: 10m
          exit_on_failure: false
```
