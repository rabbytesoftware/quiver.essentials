Steam is Valve's game store and library: buy, download and update games, keep your library in one place, play with friends, and sync saves through the cloud. The Steam client is also where you chat, join communities, and use Remote Play and Big Picture mode on a TV.

![Steam's library home, with recent games and news](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/steam/screenshots/home.jpg)

## Features

- **Store and library**: browse and buy games, and keep every title you own in one library with automatic installs and updates.
- **Collections**: sort the library into your own collections, such as favourites or "night games".
- **Friends and community**: chat, see what friends play, and join game communities and forums.
- **Cloud saves and Remote Play**: carry saves between computers, and stream a game running on one machine to another.
- **Big Picture mode**: a controller-friendly full-screen interface for the living room.

![Organising games into collections](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/steam/screenshots/collections.jpg)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | Steam's official DMG, as `Steam.app` in Applications. The app is Intel-only, so Apple silicon Macs run it through Rosetta 2. |
| Linux (x86_64) | Valve's official Steam launcher package (the same files as its `.deb`, unpacked in your user folder) and a desktop menu entry. Needs the usual 32-bit system libraries, see below. |
| Windows (x64) | Steam's official installer, run silently. **It asks for administrator approval** (a Windows UAC prompt) and installs Steam to `Program Files (x86)`. |

Not supported: Linux on ARM and Windows on ARM, where Valve publishes no Steam client of its own.

The Linux package is pinned to Valve's numbered release 1.0.0.87 and verified against the SHA-256 Valve signs for it. The Windows and macOS installers are the current ones Valve serves, downloaded over HTTPS from Valve and not checksum-verified, because Valve publishes no fixed version or checksum for them.

### Good to know

- **Steam updates itself.** What Quiver pins is only the small launcher or installer. On first launch Steam downloads its current client, then keeps it updated on its own, so after the first run you are no longer on the pinned version, as with a normal Steam install.
- **The Windows and macOS installers are not checksum-verified.** Valve serves `SteamSetup.exe` and `steam.dmg` from fixed addresses that it replaces in place, so Quiver always gets the current installer, over HTTPS from Valve, with no digest to compare it against. The Linux package is a numbered release and is verified.
- **Linux stores Steam outside Quiver's folder.** On first launch the launcher unpacks the client into `~/.local/share/Steam` and links it from `~/.steam`; your games and sign-in live there. Removing the arrow deletes the launcher but leaves that folder, so delete it yourself to remove everything. The launcher may also ask for your password to install missing 32-bit system packages (it uses `pkexec` or `sudo` on Debian and Ubuntu); on other distributions install your distribution's `steam` dependencies yourself.
- **Windows needs administrator approval.** Steam's installer requires elevation, which Quiver cannot grant. Quiver starts it through PowerShell, and Windows shows the approval prompt; if you decline, the install fails. Uninstalling asks for approval too. This path was not tested on real Windows when the arrow was written.
- **macOS keeps data in** `~/Library/Application Support/Steam`, outside the app.
- **Already have Steam?** Quiver never replaces an app it did not install. If `Steam.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.
- **The screenshots come from Valve's own package metadata** and show an older design of the client.

## License and trademarks

Steam is proprietary software by Valve Corporation, used under the [Steam Subscriber Agreement](https://store.steampowered.com/subscriber_agreement/); the launcher's own scripts are Valve's too. This arrow only downloads Valve's official builds from Valve's servers. The Steam name and logo are trademarks of Valve Corporation; the icon is Valve's own Steam share image, unmodified, and the banner is Valve's own social image from the [Steam About page](https://store.steampowered.com/about/), cropped to 2:1.

```arrow
schema: "arrow@v0"

metadata:
  name: Steam
  description: Valve's game store, library and community client
  license: Proprietary
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://store.steampowered.com
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Valve Corporation
      url: https://www.valvesoftware.com
  media:
    icon: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/steam/icon.png
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/steam/banner.jpg
  tags:
    - games
    - store
    - desktop

# Steam updates itself after the first launch on every platform, so what is
# installed here is only the launcher/installer. The Linux package is a
# numbered release in Valve's apt archive, which still serves releases back to
# 2020 (1.0.0.66, 1.0.0.75 and 1.0.0.85 all answer 200), so it stays pinned with
# the checksum Valve signs in its .dsc. The Windows and macOS installers exist
# only at rolling addresses, so they carry no checksum. Requirements are conservative
# estimates (Valve publishes no hardware minimums for the client itself; games
# need more disk, which is the user's to provide).
targets:
  # Valve's launcher package steam_1.0.0.87 (the .deb's source tarball from
  # repo.steampowered.com, version 1.0.0.87, 2026-06-26). Its SHA-256 is the one
  # Valve signs in steam_1.0.0.87.dsc. `bin_steam.sh` is the real script behind
  # the `steam` symlink and runs fine from the unpacked folder: on first launch
  # it unpacks bootstraplinux_ubuntu12_32.tar.xz into ~/.local/share/Steam
  # (outside the workdir, kept on uninstall), links ~/.steam, and runs
  # steamdeps, which may ask pkexec/sudo to install missing 32-bit libraries.
  # Valve ships no arm64 client.
  linux/amd64:
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download the Steam launcher
          url: https://repo.steampowered.com/steam/archive/stable/steam_1.0.0.87.tar.gz
          checksum: 649375d2f9377f8009aaf3e2ff09978041eb9114897d9c5a3886f1d82e27ba1f
          to: ${INSTALL_PATH}/.steam.download
          timeout: 10m
        - type: extract
          title: Unpack the Steam launcher
          from: ${INSTALL_PATH}/.steam.download
          to: ${INSTALL_PATH}/app
          timeout: 5m
    expose:
      desktop:
        - name: Steam
          path: ${INSTALL_PATH}/app/steam-launcher/bin_steam.sh
          icon: ${INSTALL_PATH}/app/steam-launcher/icons/256/steam.png
          categories: [Game, Network]

  # steam.dmg holds Steam.app, an x86_64-only bundle (its Info.plist asks for
  # macOS 10.13 or later); Apple silicon runs it under Rosetta 2. Valve serves
  # it from a fixed address it replaces in place, so there is no stable
  # checksum: the download is NOT checksum-verified (HTTPS from Valve only).
  # Steam updates itself after the first launch anyway.
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download Steam
          url: https://cdn.fastly.steamstatic.com/client/installer/steam.dmg
          to: ${INSTALL_PATH}/.steam.download
          timeout: 10m
        - type: portable
          title: Install Steam
          from: ${INSTALL_PATH}/.steam.download
          to: ${INSTALL_PATH}/Steam
          timeout: 10m
    expose:
      desktop:
        - name: Steam
          path: auto

  # SteamSetup.exe (NSIS, 32-bit; a fixed address Valve replaces in place, so
  # it is NOT checksum-verified, HTTPS from Valve only) declares requireAdministrator in its manifest, so
  # it cannot run from Quiver's unelevated process: it is started through
  # PowerShell's Start-Process -Verb RunAs, which shows the UAC prompt, with
  # NSIS's /S for a silent install into Program Files (x86)\Steam. It creates
  # its own Start Menu shortcut, so there is no `expose`. Valve ships no arm64
  # build. NOT TESTED on Windows.
  windows/amd64:
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download the Steam installer
          url: https://cdn.fastly.steamstatic.com/client/installer/SteamSetup.exe
          to: ${INSTALL_PATH}/SteamSetup.exe
          timeout: 10m
        - type: run
          title: Install Steam
          command: >-
            powershell -NoProfile -Command "$p = Start-Process -FilePath '${INSTALL_PATH}\SteamSetup.exe' -ArgumentList '/S' -Verb RunAs -Wait -PassThru; exit $p.ExitCode"
          timeout: 15m
      uninstall:
        - type: run
          title: Uninstall Steam
          command: >-
            powershell -NoProfile -Command "$d = [Environment]::GetEnvironmentVariable('ProgramFiles(x86)'); $u = Join-Path $d 'Steam\uninstall.exe'; if (Test-Path $u) { Start-Process -FilePath $u -ArgumentList '/S' -Verb RunAs -Wait }"
          timeout: 10m
          exit_on_failure: false
```
