7-Zip is a free file archiver with a high compression ratio. It packs and unpacks its own 7z format as well as ZIP, TAR, GZIP, BZIP2, XZ and WIM, and opens a long list of other archive and disk-image formats, including RAR (unpack only), ISO, CAB and DMG. It is written by Igor Pavlov and works on personal and commercial computers alike, without registration or payment.

![7-Zip File Manager on Windows](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/7zip/screenshots/file-manager.png)

## Features

- **Strong compression**: the 7z format with LZMA and LZMA2 compression, plus ZIP, TAR, GZIP, BZIP2, XZ and WIM for packing.
- **Wide format support for unpacking**: RAR, ISO, CAB, MSI, DMG, VHD, SquashFS, NTFS and many more.
- **Encryption**: AES-256 encryption for 7z and ZIP archives.
- **Self-extracting archives**: create 7z archives that unpack without 7-Zip installed.
- **One command-line tool everywhere**: `7zz` on Linux and macOS and `7z.exe` on Windows share the same commands (`a` to add, `x` to extract, `l` to list, `t` to test).
- **A file manager on Windows**: `7zFM.exe` browses and edits archives, next to `7zG.exe`, the dialog front end of the same engine.

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| Linux (x86_64 and ARM64) | 7-Zip's official command-line build for your processor, unpacked into Quiver's folder, with `7zz` (and `7z`, the same program) on your `PATH`. The static build `7zzs` sits beside it. |
| macOS (Apple silicon and Intel) | 7-Zip's official command-line build, a single universal `7zz` for both processors, with `7zz` and `7z` on your `PATH`. There is no graphical 7-Zip for macOS. |
| Windows (x64 and ARM64) | 7-Zip's official installer package for your processor, unpacked into Quiver's folder: the console tool `7z`, the file manager `7zFM` (with a Start Menu shortcut) and `7zG`. No administrator rights are needed. |

Every download is pinned to 7-Zip 26.04 (2026-10-05) from [7-zip.org](https://www.7-zip.org/download.html) and verified against its SHA-256 checksum. 7-Zip does not publish builds for 32-bit Linux or Windows, which Quiver does not target.

Run `quiver path setup` once so your shell finds `~/.quiver/bin` (Linux and macOS), then try:

```sh
7zz a backup.7z Documents/
7zz x backup.7z
7zz l backup.7z
```

### Good to know

- **Windows: this is a portable copy, not the installer.** Quiver unpacks the installer's contents (using 7-Zip's own `7zr.exe`) into its folder instead of running the installer, so nothing is written to the registry and no administrator rights are needed. Because of that, the Explorer right-click menu, file associations and the "Open with 7-Zip" entries that the installer sets up are not added; open archives from the 7-Zip File Manager or the command line. The folder also holds an `Uninstall.exe` that Quiver does not use.
- **On Windows the `7z` command is available in new terminals**: Quiver adds 7-Zip's folder to your user `Path`, so `7zFM` and `7zG` are there too.
- **Updates come through Quiver.** 7-Zip has no built-in updater.
- **Your settings** (the File Manager's options) live in your user profile on Windows, not in Quiver's folder.
- **Already have 7-Zip or p7zip?** Quiver never overwrites a command it did not create. If `7z` already exists in `~/.quiver/bin`, that one stays and `7zz` still works.

## License and trademarks

7-Zip is free software by Igor Pavlov, under the GNU LGPL (version 2.1 or later) with parts of `7z.dll` under the BSD licenses and parts under the LGPL with the "unRAR license restriction"; see its [license terms](https://www.7-zip.org/license.txt). This arrow only downloads 7-Zip's official builds from 7-zip.org. The icon is 7-Zip's File Manager icon from its [source repository](https://github.com/ip7z/7zip), unmodified and placed in a square SVG, and the banner was designed for this arrow around that same icon (enlarged by a whole-number factor, pixel for pixel) with the product name set beside it. The screenshot is the 7-Zip File Manager, captured on Windows 11 while testing this arrow.

```arrow
schema: "arrow@v0"

metadata:
  name: 7-Zip
  description: The free file archiver with a high compression ratio
  license: LGPL-2.1-or-later
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://www.7-zip.org
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Igor Pavlov
      url: https://www.7-zip.org
  media:
    icon: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/7zip/icon.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/7zip/banner.png
  tags:
    - archiver
    - compression
    - cli
    - desktop

# 7-Zip 26.04 (2026-10-05) from 7-zip.org. The SHA-256 values were computed on
# the downloads and match the digests on the ip7z/7zip GitHub release.
# Requirements are conservative estimates: 7-Zip publishes none.
targets:
  # Official console build (7zz, plus the static 7zzs): a tar.xz whose files
  # sit at the archive root, so it is unpacked into its own folder. Quiver's built-in xz reader rejects this archive's filter chain, so the system `tar` (with xz support) unpacks it.
  "linux/*":
    requirements:
      cpu_cores: 1
      ram_gb: 1
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download 7-Zip
          url:
            linux/amd64: https://www.7-zip.org/a/7z2604-linux-x64.tar.xz
            linux/arm64: https://www.7-zip.org/a/7z2604-linux-arm64.tar.xz
          checksum:
            linux/amd64: fc0327ba27e89bd086cf426dff17d77de582953cdbbc10a6576540a06853ffcd
            linux/arm64: 5b0ac3aa91c1e3499f011d6af69d7f6b4de3ef2f011d9e2ff44c58ebd04aa388
          to: ${INSTALL_PATH}/.7zip.download
          timeout: 10m
        - type: run
          title: Unpack 7-Zip
          command: 'mkdir -p 7-Zip && tar -xf .7zip.download -C 7-Zip && rm -f .7zip.download'
          timeout: 5m
      uninstall:
        - type: run
          title: Remove 7-Zip
          command: 'rm -rf 7-Zip'
          timeout: 2m
    expose:
      cli:
        - name: 7zz
          path: ${INSTALL_PATH}/7-Zip/7zz
        - name: 7z
          path: ${INSTALL_PATH}/7-Zip/7zz

  # One universal (arm64 + x86_64) 7zz for both Macs.
  "darwin/*":
    requirements:
      cpu_cores: 1
      ram_gb: 1
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download 7-Zip
          url: https://www.7-zip.org/a/7z2604-mac.tar.xz
          checksum: bee04358cbcbc7106273cee0e8d72916db2696c48067a3538c34d8cd6fd16578
          to: ${INSTALL_PATH}/.7zip.download
          timeout: 10m
        - type: run
          title: Unpack 7-Zip
          command: 'mkdir -p 7-Zip && tar -xf .7zip.download -C 7-Zip && rm -f .7zip.download'
          timeout: 5m
      uninstall:
        - type: run
          title: Remove 7-Zip
          command: 'rm -rf 7-Zip'
          timeout: 2m
    expose:
      cli:
        - name: 7zz
          path: ${INSTALL_PATH}/7-Zip/7zz
        - name: 7z
          path: ${INSTALL_PATH}/7-Zip/7zz

  # 7-Zip's Windows installer is a small stub followed by a plain 7z archive,
  # so 7-Zip's own 7zr.exe unpacks it (-t7z finds the archive after the stub)
  # into a portable folder: no administrator rights, no registry entries, no
  # Explorer context menu. The two downloads are deleted once unpacked;
  # `uninstall` removes the folder. 7zr.exe is an x86 program, which Windows
  # on ARM runs through emulation.
  "windows/*":
    requirements:
      cpu_cores: 1
      ram_gb: 1
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download 7zr
          url: https://www.7-zip.org/a/7zr.exe
          checksum: 256feca8e274e5da655e2a284fabafd9f554365eb164862089dacd4e8276d282
          to: ${INSTALL_PATH}/.7zr.exe
          timeout: 5m
        - type: fetch
          title: Download 7-Zip
          url:
            windows/amd64: https://www.7-zip.org/a/7z2604-x64.exe
            windows/arm64: https://www.7-zip.org/a/7z2604-arm64.exe
          checksum:
            windows/amd64: d54bf805f9f3704d1e8db2fa3498ae7ef2df0312b40b558e7c71c734430a665d
            windows/arm64: d4117b95495b0e925334ae7b5bddf2853513274603de15dee6acf03999fbc09c
          to: ${INSTALL_PATH}/.7zip-setup.exe
          timeout: 10m
        - type: run
          title: Unpack 7-Zip
          command: '.\.7zr.exe x -t7z -y -o7-Zip .\.7zip-setup.exe'
          timeout: 5m
        - type: run
          title: Remove the installer files
          command: 'del /f /q .7zr.exe .7zip-setup.exe'
          timeout: 1m
          exit_on_failure: false
      uninstall:
        - type: run
          title: Remove 7-Zip
          command: 'rmdir /s /q 7-Zip'
          timeout: 2m
          exit_on_failure: false
    expose:
      cli:
        - name: 7z
          path: ${INSTALL_PATH}/7-Zip/7z.exe
      desktop:
        - name: 7-Zip
          path: ${INSTALL_PATH}/7-Zip/7zFM.exe
```
