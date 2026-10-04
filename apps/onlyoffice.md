ONLYOFFICE Desktop Editors is a free office suite for documents, spreadsheets, presentations and PDFs, in one app with tabs. It works natively with Microsoft Office formats (DOCX, XLSX, PPTX) as well as OpenDocument, and can connect to cloud platforms such as ONLYOFFICE, Nextcloud and ownCloud to edit files together in real time.

![The ONLYOFFICE document editor](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/onlyoffice/screenshots/document-editor.jpg)

## Features

- **Documents**: styles and formatting, tables of contents and mail merge.
- **Spreadsheets**: over 400 functions, charts, templates and macros.
- **Presentations**: formatting tools, objects and a presenter mode.
- **PDFs**: edit text, annotate, and create and fill in forms.
- **Office compatibility**: DOCX, XLSX and PPTX, plus ODT, ODS, ODP and CSV.
- **Collaboration**: connect a cloud to co-edit documents live, with comments and chat.
- **Plugins and AI**: extend the editors with plugins, including AI assistants for writing and translating.

![The ONLYOFFICE spreadsheet editor](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/onlyoffice/screenshots/spreadsheet-editor.jpg)

![The ONLYOFFICE presentation editor](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/onlyoffice/screenshots/presentation-editor.jpg)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | ONLYOFFICE's official DMG for your processor, as `ONLYOFFICE.app` in Applications. Requires macOS 11 or later. |
| Linux (x86_64 and ARM64) | ONLYOFFICE's official AppImage for your processor and a desktop menu entry. |
| Windows (x64 and ARM64) | ONLYOFFICE's official portable build for your processor, unpacked into Quiver's folder, and a Start Menu shortcut. |

Every download is pinned to an official ONLYOFFICE release from [its GitHub releases](https://github.com/ONLYOFFICE/DesktopEditors/releases) and verified against its SHA-256 checksum before it is installed.

### Good to know

- **No account needed.** The editors work on local files; signing in to a cloud is only needed to co-edit.
- **On macOS, ONLYOFFICE can update itself.** Quiver installs the release pinned here; from then on its built-in updater offers new versions. On Linux and Windows, update ONLYOFFICE through Quiver.
- **Your documents are yours.** Files you open and save stay where you keep them; uninstalling removes only the app.
- **Already have ONLYOFFICE?** Quiver never replaces an app it did not install. If `ONLYOFFICE.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.

## License and trademarks

ONLYOFFICE Desktop Editors is free software by Ascensio System SIA, released under the [GNU AGPL v3](https://github.com/ONLYOFFICE/DesktopEditors/blob/master/LICENSE). This arrow only downloads ONLYOFFICE's official builds from its GitHub releases. The ONLYOFFICE name and logo are trademarks of Ascensio System SIA; the icon is the app icon from the [desktop-apps repository](https://github.com/ONLYOFFICE/desktop-apps), the banner was generated from it, and the screenshots come from ONLYOFFICE's official Microsoft Store listing (the Windows app shares the design of the other platforms).

```arrow
schema: "arrow@v0"

metadata:
  name: ONLYOFFICE
  description: Free office suite for documents, spreadsheets, presentations and PDFs
  license: AGPL-3.0
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://www.onlyoffice.com/desktop.aspx
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Ascensio System SIA
      url: https://www.onlyoffice.com
  media:
    icon: https://raw.githubusercontent.com/ONLYOFFICE/desktop-apps/v9.4.0.97/macos/ONLYOFFICE/Images.xcassets/AppIcon.appiconset/1024x1024.png
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/onlyoffice/banner.svg
  tags:
    - office
    - documents
    - desktop

# Every download is a release asset of github.com/ONLYOFFICE/DesktopEditors
# (v9.4.0), with the digest GitHub publishes for it. Requirements are
# conservative estimates: ONLYOFFICE publishes no hardware minimums.
targets:
  # Type-2 AppImages, unpacked in place by `portable`.
  "linux/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download ONLYOFFICE
          url:
            linux/amd64: https://github.com/ONLYOFFICE/DesktopEditors/releases/download/v9.4.0/DesktopEditors-x86_64.AppImage
            linux/arm64: https://github.com/ONLYOFFICE/DesktopEditors/releases/download/v9.4.0/DesktopEditors-arm64.AppImage
          checksum:
            linux/amd64: f5faf24552665262fe94486a510b997d2e5a24bde14df94c802c79bf17f9254c
            linux/arm64: 7dfc2fa195ff9912a4022841613b9a99fdba2a238792648f257007a7df887b7c
          to: ${INSTALL_PATH}/.onlyoffice.download
          timeout: 20m
        - type: portable
          title: Install ONLYOFFICE
          from: ${INSTALL_PATH}/.onlyoffice.download
          to: ${INSTALL_PATH}/ONLYOFFICE
          timeout: 15m
    expose:
      desktop:
        - name: ONLYOFFICE
          path: auto
          categories: [Office, WordProcessor, Spreadsheet, Presentation]

  # One DMG per processor; requires macOS 11 or later. The app updates itself
  # (Sparkle).
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download ONLYOFFICE
          url:
            darwin/arm64: https://github.com/ONLYOFFICE/DesktopEditors/releases/download/v9.4.0/ONLYOFFICE-arm.dmg
            darwin/amd64: https://github.com/ONLYOFFICE/DesktopEditors/releases/download/v9.4.0/ONLYOFFICE-x86_64.dmg
          checksum:
            darwin/arm64: e965be2222609add6b5a70baa2a8cdb599402491fb2925825d9039dcb154beb4
            darwin/amd64: 43ac517493c0c316f268ce4b7dc3810b77a7aefe83c0edc1655476d9f21681d2
          to: ${INSTALL_PATH}/.onlyoffice.download
          timeout: 20m
        - type: portable
          title: Install ONLYOFFICE
          from: ${INSTALL_PATH}/.onlyoffice.download
          to: ${INSTALL_PATH}/ONLYOFFICE
          timeout: 15m
    expose:
      desktop:
        - name: ONLYOFFICE
          path: auto

  # The portable zip holds DesktopEditors.exe at its root.
  "windows/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download ONLYOFFICE
          url:
            windows/amd64: https://github.com/ONLYOFFICE/DesktopEditors/releases/download/v9.4.0/DesktopEditors_x64.zip
            windows/arm64: https://github.com/ONLYOFFICE/DesktopEditors/releases/download/v9.4.0/DesktopEditors_arm64.zip
          checksum:
            windows/amd64: 22ae48a7813954e5079bff1ea211c6583aba67f34f2d0dbcb2431d4a20e94dfc
            windows/arm64: 9224d60b736542cb60b97fd947d5a3f963e064b73a807043745e3dcf0d92d3a8
          to: ${INSTALL_PATH}/.onlyoffice.download
          timeout: 20m
        - type: extract
          title: Unpack ONLYOFFICE
          from: ${INSTALL_PATH}/.onlyoffice.download
          to: ${INSTALL_PATH}/ONLYOFFICE
          timeout: 15m
    expose:
      desktop:
        - name: ONLYOFFICE
          path: ${INSTALL_PATH}/ONLYOFFICE/DesktopEditors.exe
```
