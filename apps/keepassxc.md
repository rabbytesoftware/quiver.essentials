KeePassXC is a free, open-source password manager that keeps your logins in an encrypted database file on your own computer: no account, no cloud service and no subscription. Besides usernames and passwords it stores URLs, notes, attachments and one-time-password secrets, and it can fill them into other applications for you. The same database format is used on Windows, macOS and Linux, so one file works wherever you take it.

![A KeePassXC database with groups, entries and the entry preview](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/keepassxc/screenshots/database.png)

## Features

- **Encrypted local databases**: entries live in a file you choose and control, organised in groups and searchable, with tags, custom icons and a history of past versions.
- **Password and passphrase generator**: build random passwords or word-based passphrases with the character sets and length you need.
- **Auto-Type**: type a username and password into another window with a global shortcut, with per-entry sequences.
- **Browser integration**: fill logins in your web browser through the KeePassXC-Browser extension.
- **Authenticator codes**: store TOTP secrets alongside the login they belong to.
- **SSH agent**: use SSH keys stored in your database.
- **Import and reports**: bring in entries from CSV and other password managers, and review weak or reused passwords in database reports.
- **Command line**: `keepassxc-cli` reads and edits databases from a terminal or script.

![Editing an entry in KeePassXC](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/keepassxc/screenshots/edit-entry.png)

![The advanced password generator in KeePassXC](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/keepassxc/screenshots/password-generator.png)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | KeePassXC's official DMG for your processor, as `KeePassXC.app` in Applications, plus the `keepassxc-cli` command. Requires macOS 12 or later. |
| Linux (x86_64) | KeePassXC's official AppImage, a desktop menu entry and the `keepassxc-cli` command. KeePassXC publishes no AppImage for ARM. |
| Windows (x64) | KeePassXC's official portable ZIP, a Start Menu shortcut and the `keepassxc-cli` command. Requires Windows 10 or 11 and the Microsoft Visual C++ Redistributable. KeePassXC 2.7 has no native Windows ARM64 build, so ARM64 is not offered. |

Every download is pinned to KeePassXC 2.7.12 and verified against its SHA-256 checksum, which matches the digest KeePassXC publishes next to each file.

### Good to know

- **Run `quiver path setup` once** so your shell finds `keepassxc-cli` in `~/.quiver/bin`. On Windows the folder holding `keepassxc-cli.exe` is added to your user `Path` instead.
- **Keep your databases outside Quiver's folder.** KeePassXC saves a database wherever you tell it to, and Quiver never touches those files. Removing the arrow deletes only the program.
- **On Windows the ZIP is the portable build**: it keeps its settings (`keepassxc.ini`) next to the program, inside Quiver's folder, so updating or removing the arrow resets them. On macOS and Linux settings are kept in your user profile and survive.
- **Updates come through Quiver**: installing a new release replaces the app.
- **Already have KeePassXC?** Quiver never replaces an app it did not install. If `KeePassXC.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.
- **The AppImage is a fixed 2.7.12 build.** KeePassXC's own recommended Linux package is the Flatpak on Flathub; this arrow is for when you want a per-user install managed by Quiver.

## License and trademarks

KeePassXC is free software by the KeePassXC Team, licensed under the GNU General Public License version 2 or version 3 (see its [repository](https://github.com/keepassxreboot/keepassxc)). This arrow only downloads KeePassXC's official builds from its GitHub releases. The KeePassXC name and logo belong to the KeePassXC Team; the icon is the project's own, the banner was generated from it, and the screenshots come from [keepassxc.org](https://keepassxc.org/screenshots/) (taken on Windows; the interface is the same on every platform).

```arrow
schema: "arrow@v0"

metadata:
  name: KeePassXC
  description: A free, open-source offline password manager with auto-type and browser integration
  license: GPL-2.0-only OR GPL-3.0-only
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://keepassxc.org
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: The KeePassXC Team
      url: https://keepassxc.org
  media:
    icon: https://raw.githubusercontent.com/keepassxreboot/keepassxc/2.7.12/share/icons/application/scalable/apps/keepassxc.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/keepassxc/banner.svg
  tags:
    - password-manager
    - security
    - desktop
    - cli

# KeePassXC 2.7.12, with the SHA-256 digests GitHub records for the release
# assets (identical to the .DIGEST files KeePassXC publishes). KeePassXC
# publishes no hardware minimums, so requirements are conservative estimates.
# 2.8 is still in beta; it is the first release with native Windows ARM64.
targets:
  # Upstream ships the AppImage for x86_64 only. `portable` unpacks it into
  # app/KeePassXC (the stem of the download name). AppRun cannot start the CLI
  # from a symlink (it needs `cli` as first argument), so the CLI entry points
  # at the bundled keepassxc-cli, which finds its libraries through
  # $ORIGIN/../lib.
  linux/amd64:
    requirements:
      cpu_cores: 1
      ram_gb: 1
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download KeePassXC
          url: https://github.com/keepassxreboot/keepassxc/releases/download/2.7.12/KeePassXC-2.7.12-x86_64.AppImage
          checksum: 564fe8b751b9ef7aa057e4d3d0b2878db24eaa0f6b1c855c82e699ab0913ae49
          to: ${INSTALL_PATH}/KeePassXC.AppImage
          timeout: 10m
        - type: portable
          title: Install KeePassXC
          from: ${INSTALL_PATH}/KeePassXC.AppImage
          to: ${INSTALL_PATH}/app
          timeout: 5m
    expose:
      desktop:
        - name: KeePassXC
          path: auto
          categories: [Utility, Security]
      cli:
        - name: keepassxc-cli
          path: ${INSTALL_PATH}/app/KeePassXC/usr/bin/keepassxc-cli

  # One DMG per processor; requires macOS 12 or later. `desktop` moves the
  # app to Applications; the CLI entry is relocated with it and links to the
  # keepassxc-cli inside the bundle.
  "darwin/*":
    requirements:
      cpu_cores: 1
      ram_gb: 1
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download KeePassXC
          url:
            darwin/arm64: https://github.com/keepassxreboot/keepassxc/releases/download/2.7.12/KeePassXC-2.7.12-arm64.dmg
            darwin/amd64: https://github.com/keepassxreboot/keepassxc/releases/download/2.7.12/KeePassXC-2.7.12-x86_64.dmg
          checksum:
            darwin/arm64: 65f4f63607180c0a15794b4a4068f85e99ed5391c87c1fb9312648f1b36fed40
            darwin/amd64: f55737bf759b7ea622967ae979e8fd0ef06a8133104124c24861fd11a3fe14b5
          to: ${INSTALL_PATH}/.keepassxc.download
          timeout: 10m
        - type: portable
          title: Install KeePassXC
          from: ${INSTALL_PATH}/.keepassxc.download
          to: ${INSTALL_PATH}/KeePassXC
          timeout: 5m
    expose:
      desktop:
        - name: KeePassXC
          path: auto
      cli:
        - name: keepassxc-cli
          path: ${INSTALL_PATH}/KeePassXC/KeePassXC.app/Contents/MacOS/keepassxc-cli

  # The portable ZIP (64-bit, Windows 10 / 11, needs the MSVC redistributable).
  # It unpacks into a KeePassXC-2.7.12-Win64 folder and carries a `.portable`
  # marker, so settings stay next to the program. Exposing keepassxc-cli.exe
  # puts its folder on the user Path.
  windows/amd64:
    requirements:
      cpu_cores: 1
      ram_gb: 1
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download KeePassXC
          url: https://github.com/keepassxreboot/keepassxc/releases/download/2.7.12/KeePassXC-2.7.12-Win64.zip
          checksum: 958234b0669d757b53eacf42bdd5de0fa1cc1ab7527709ddf4f7e29c06a8305f
          to: ${INSTALL_PATH}/.keepassxc.download
          timeout: 10m
        - type: portable
          title: Unpack KeePassXC
          from: ${INSTALL_PATH}/.keepassxc.download
          to: ${INSTALL_PATH}/KeePassXC
          timeout: 5m
    expose:
      desktop:
        - name: KeePassXC
          path: ${INSTALL_PATH}/KeePassXC/KeePassXC-2.7.12-Win64/KeePassXC.exe
      cli:
        - name: keepassxc-cli
          path: ${INSTALL_PATH}/KeePassXC/KeePassXC-2.7.12-Win64/keepassxc-cli.exe
```
