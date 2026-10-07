Obsidian is a note-taking app that works on a folder of plain Markdown files on your own computer. You link notes to each other, see how they connect, and shape the app with plugins and themes, while your notes stay in open, portable files that any other tool can read. It suits personal notes, journals, research and knowledge bases, and it is free to use.

![Obsidian's Bases view, a table over notes and their properties](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/obsidian/screenshots/bases.png)

## Features

- **Notes are Markdown files**: a vault is an ordinary folder, so your notes stay readable and portable outside Obsidian.
- **Links and backlinks**: connect notes with internal links and see which other notes point back to the one you are reading.
- **Graph view**: a visual map of how your notes relate to each other.
- **Canvas**: an infinite space to lay out notes, images and ideas and connect them.
- **Bases**: turn notes and their properties into table-like views you can filter and sort.
- **Plugins and themes**: a large community catalogue extends or restyles the app.
- **Command line**: a built-in CLI, once you enable it in Settings, controls the running app from a terminal.
- **Optional paid services**: Obsidian Sync and Obsidian Publish are separate subscriptions; the app works fully offline without them.

![A Canvas in Obsidian, laid out as a diagram](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/obsidian/screenshots/canvas.png)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | Obsidian's official universal DMG, as `Obsidian.app` in Applications. |
| Linux (x86_64 and ARM64) | Obsidian's official AppImage for your processor, unpacked into Quiver's folder, with a desktop menu entry. |
| Windows (x64 and ARM64) | Obsidian's official installer, run silently for your user. It installs into your user profile and adds its own Start Menu shortcut. |

Every download is pinned to Obsidian 1.14.4 from the [official GitHub releases](https://github.com/obsidianmd/obsidian-releases/releases) and verified against its SHA-256 checksum.

### Good to know

- **Obsidian updates itself in two layers.** With automatic updates on (the default), the app downloads newer app versions into your user profile and applies them on restart. The installer, which carries Electron, is updated only by installing again, and Obsidian tells you when that is needed. Updating the arrow through Quiver installs a newer pinned installer.
- **Keep your vaults outside Quiver's folder.** A vault is any folder you pick, and Quiver never touches it. Obsidian's settings and the app updates it downloads live in your user profile (for example `~/.config/obsidian` on Linux), so removing the arrow leaves them in place.
- **On Windows, Obsidian installs into your user profile** (by default `%LOCALAPPDATA%\Programs\Obsidian`), not into Quiver's folder. Uninstalling through Quiver runs Obsidian's own uninstaller.
- **On Linux the AppImage is unpacked, so no FUSE is needed**, and the menu entry launches it with the arguments Obsidian's AppImage defines.
- **Already have Obsidian?** Quiver never replaces an app it did not install. If `Obsidian.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.
- **Minimum hardware**: Obsidian publishes none.

## License and trademarks

Obsidian is proprietary software by the Obsidian team, free to use, including at work; organizations can optionally support it with a [commercial license](https://obsidian.md/pricing). This arrow only downloads Obsidian's official builds from its GitHub releases. The Obsidian name and logo belong to Obsidian; the icon is the logo from [obsidian.md](https://obsidian.md/brand) and the banner is Obsidian's own social-share image from [obsidian.md](https://obsidian.md), cropped to 2:1, and the screenshots come from Obsidian's [help documentation](https://obsidian.md/help/).

```arrow
schema: "arrow@v0"

metadata:
  name: Obsidian
  description: A private, extensible note-taking app built on plain Markdown files
  license: Proprietary
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://obsidian.md
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Obsidian
      url: https://obsidian.md
  media:
    icon: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/obsidian/icon.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/obsidian/banner.png
  tags:
    - notes
    - markdown
    - knowledge-base
    - desktop

# Obsidian 1.14.4 from the obsidianmd/obsidian-releases GitHub release, with the
# SHA-256 digests GitHub records for each asset. Obsidian publishes no hardware
# minimums, so requirements are conservative estimates. The app updates itself
# after install (the asar is downloaded into the user profile); the pinned
# installers are the base the first install starts from.
targets:
  # Type-2 AppImages, unpacked in place by `portable` (no FUSE). The unpacked
  # AppDir keeps the desktop file's Exec arguments in the .quiver-run launcher.
  "linux/*":
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download Obsidian
          url:
            linux/amd64: https://github.com/obsidianmd/obsidian-releases/releases/download/v1.14.4/Obsidian-1.14.4.AppImage
            linux/arm64: https://github.com/obsidianmd/obsidian-releases/releases/download/v1.14.4/Obsidian-1.14.4-arm64.AppImage
          checksum:
            linux/amd64: 6362ddbeeeebb7bbccb48fae009572cf2284ef92f5c919c1332aba48de6ffeaa
            linux/arm64: 721829a4f0ffadf7674f396aed58a5699e116b76b78747873d1751193efb66a9
          to: ${INSTALL_PATH}/.obsidian.download
          timeout: 20m
        - type: portable
          title: Install Obsidian
          from: ${INSTALL_PATH}/.obsidian.download
          to: ${INSTALL_PATH}/Obsidian
          timeout: 10m
    expose:
      desktop:
        - name: Obsidian
          path: auto
          categories: [Office, TextEditor]

  # One universal DMG for both processors.
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download Obsidian
          url: https://github.com/obsidianmd/obsidian-releases/releases/download/v1.14.4/Obsidian-1.14.4.dmg
          checksum: dcf818dd20ee5d9dd3e782eee0c0c4c47cc225383b051c2fc9af7d5772f59f70
          to: ${INSTALL_PATH}/.obsidian.download
          timeout: 20m
        - type: portable
          title: Install Obsidian
          from: ${INSTALL_PATH}/.obsidian.download
          to: ${INSTALL_PATH}/Obsidian
          timeout: 10m
    expose:
      desktop:
        - name: Obsidian
          path: auto

  # One NSIS installer for x64 and ARM64 (the same file in Obsidian's WinGet
  # manifest). `/S` is silent and `/currentuser` is the per-user scope WinGet
  # uses: no administrator rights, installed into %LOCALAPPDATA%\Programs\Obsidian
  # with its own Start Menu shortcut, so there is no `expose` here. `uninstall`
  # runs the uninstaller the installer writes next to the app.
  "windows/*":
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download the Obsidian installer
          url: https://github.com/obsidianmd/obsidian-releases/releases/download/v1.14.4/Obsidian-1.14.4.exe
          checksum: 28662520368d5956df7798076b8370ac730164a8863dcd4f678ced53f63faa00
          to: ${INSTALL_PATH}/ObsidianSetup.exe
          timeout: 30m
        - type: run
          title: Install Obsidian
          command: '.\ObsidianSetup.exe /S /currentuser >nul 2>&1 <nul'
          timeout: 15m
      uninstall:
        - type: run
          title: Uninstall Obsidian
          command: '"%LOCALAPPDATA%\Programs\Obsidian\Uninstall Obsidian.exe" /S /currentuser'
          timeout: 10m
          exit_on_failure: false
```
