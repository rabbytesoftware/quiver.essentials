WinRAR is an archive manager for Windows. It creates archives in the RAR and ZIP formats, opens and unpacks RAR, ZIP and many other archive types downloaded from the internet, and can shrink data for backups and email attachments. It comes with the command-line tools `Rar.exe` and `UnRAR.exe` as well. WinRAR is **shareware**: you can try it for free, and a license is needed to keep using it after the trial.

![WinRAR's main window browsing a folder](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/winrar/screenshots/main-window.png)

## Features

- **RAR and ZIP archives**: create and extract both, and unpack many other formats such as 7z, TAR, GZ, BZ2, XZ, CAB and ISO.
- **Archive management**: add to, update and test archives, and repair damaged ones when they carry recovery data.
- **Encryption and splitting**: password-protect archives and split large ones into volumes.
- **Self-extracting archives**: create archives that unpack without WinRAR installed.
- **Command line**: `Rar.exe` and `UnRAR.exe` for scripts, plus the `WinRAR.exe` graphical interface.
- **Explorer integration**: right-click menu entries to pack and unpack files.

![WinRAR's archive name and parameters dialog](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/winrar/screenshots/archive-options.png)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| Windows (x64) | WinRAR's official installer, run silently into Quiver's folder. Windows asks for administrator approval, because the installer elevates itself. |
| Windows (ARM64) | Not supported: RARLAB publishes WinRAR for x64 only. |
| macOS, Linux | Not supported by this arrow. RARLAB's separate command-line `rar` tools for those systems are not part of it. |

The download is pinned to WinRAR 7.23, the current release on [rarlab.com](https://www.rarlab.com/download.htm) (an English x64 build; RARLAB also lists newer 7.30 beta builds, which are not used), and verified against its SHA-256 checksum. RARLAB does not publish checksums; the value was computed on the download and matches the one in the WinRAR package of Microsoft's winget community repository.

### Good to know

- **WinRAR is proprietary shareware with a trial.** Its license agreement allows a test period of at most 40 days at no charge, after which a license must be purchased. This arrow installs the trial version; if you already have a license key, WinRAR reads it as usual. By installing, you accept the license agreement shown in WinRAR's `License.txt`.
- **Windows shows a permission prompt.** The installer needs administrator approval to register its Explorer integration and file associations, so it asks for it itself.
- **WinRAR is installed in Quiver's folder**, but the installer also writes outside it: Start Menu shortcuts, file associations, Explorer context menu entries and registry settings. Uninstalling through Quiver runs WinRAR's own uninstaller, which removes them.
- **Your settings** are kept in your user profile (`%APPDATA%\WinRAR`) rather than in Quiver's folder.
- **Updates come through Quiver.** WinRAR does not update itself.
- **Already have WinRAR?** This installs a second copy in Quiver's folder and registers it with Windows like any WinRAR install, so remove an older copy first.

## License and trademarks

WinRAR is proprietary software by Alexander L. Roshal, distributed by win.rar GmbH under the [end user license agreement](https://www.rarlab.com/license.htm) included in the installer. This arrow only downloads WinRAR's official installer from rarlab.com and does not modify it. The WinRAR name and logo belong to win.rar GmbH; the icon is the application icon stored in WinRAR's own `WinRAR.exe`, extracted unmodified, the banner was designed for this arrow around that icon with the product name set beside it, and the screenshots come from RARLAB's [WinRAR product page](https://www.win-rar.com/products-winrar.html) (they show an earlier release with the same layout).

```arrow
schema: "arrow@v0"

metadata:
  name: WinRAR
  description: The RAR and ZIP archive manager for Windows (shareware, free trial)
  license: Proprietary
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://www.rarlab.com
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Alexander Roshal and win.rar GmbH
      url: https://www.win-rar.com
  media:
    icon: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/winrar/icon.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/winrar/banner.png
  tags:
    - archiver
    - compression
    - desktop

# WinRAR 7.23 (English, x64), the stable release on rarlab.com (the 7.30 beta
# is not used). RARLAB publishes no digests, so the SHA-256 was computed on
# the download; it matches the winget-pkgs manifest for RARLab.WinRAR 7.23.0.
# Windows only: RARLAB ships WinRAR for x64 only (its download page lists no ARM64 build), and the Linux/macOS `rar` tools are command-line packages this
# arrow does not cover. Requirements are conservative estimates.
targets:
  # The installer elevates itself (winget: ElevationRequirement elevatesSelf)
  # and takes -s1 for a silent install and -d for the destination, as winget
  # uses. `start /w` waits for it. It creates its own Start Menu entries, so
  # there is no `expose`. Uninstall runs the Uninstall.exe it places in the
  # destination folder, silently (/s); the rmdir removes what is left.
  "windows/amd64":
    requirements:
      cpu_cores: 1
      ram_gb: 1
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download the WinRAR installer
          url: https://www.rarlab.com/rar/winrar-x64-723.exe
          checksum: 8ff0daf3ed564cc743c0e23ff2e253997ffc74460f9673f0b6dd037b2db4ce7b
          to: ${INSTALL_PATH}/WinRARSetup.exe
          timeout: 10m
        - type: run
          title: Install WinRAR
          command: 'start /w "" .\WinRARSetup.exe -s1 -d"%CD%\WinRAR"'
          timeout: 10m
      uninstall:
        - type: run
          title: Uninstall WinRAR
          command: 'start /w "" "%CD%\WinRAR\Uninstall.exe" /s'
          timeout: 5m
          exit_on_failure: false
        - type: run
          title: Remove leftover files
          command: 'rmdir /s /q WinRAR'
          timeout: 2m
          exit_on_failure: false
```
