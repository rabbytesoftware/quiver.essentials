Discord is a place to talk, play and hang out: servers organised into text and voice channels, direct messages and group chats, voice and video calls, and screen sharing with low enough latency to watch or play something together. It is built around communities, from a handful of friends to servers with hundreds of thousands of members.

![Discord group chat, with custom emoji](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/discord/screenshots/group-chat.jpg)

## Features

- **Servers and channels**: text channels for conversation, voice channels people drop in and out of without calling anyone, and roles and permissions for running a community.
- **Voice, video and screen sharing**: one-to-one or group calls, and streaming a game, an app or the whole screen to friends.
- **Activities**: games and shared apps that run inside a voice call.
- **Make it yours**: custom emoji, stickers, soundboard sounds, avatars, statuses and profiles.
- **Everywhere**: the same account and conversations on desktop, web and mobile.

![Streaming and video in a Discord call](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/discord/screenshots/stream-together.jpg)

![Watching and playing together in a call](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/discord/screenshots/activities.jpg)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | Discord's universal DMG, as `Discord.app` in Applications. Requires macOS 12 or later. |
| Linux (x86_64) | Discord's official tarball and a desktop menu entry. Discord publishes no Linux build for ARM. |
| Windows (x64 and ARM64) | Discord's official installer, run silently. It installs Discord for your user and adds its own Start Menu shortcut. |

Every download is pinned to an official Discord build and verified against its SHA-256 checksum before it runs.

### Good to know

- **Discord keeps itself up to date.** Quiver installs the build pinned here; from then on Discord's own updater installs new versions, as it does when installed by hand.
- **Linux downloads the client on first launch.** The official Linux package is a small bootstrapper: the first time you open Discord it downloads the full client into `~/.config/discord`, where it also keeps your session. Uninstalling removes the menu entry, and removing Discord from your library deletes the files Quiver downloaded; `~/.config/discord` is left alone either way, so you stay signed in if you reinstall. Delete it to remove everything.
- **On Windows, Discord installs into your user profile** (`%LOCALAPPDATA%\Discord`), not into Quiver's folder. Uninstalling through Quiver runs Discord's own uninstaller.
- **Already have Discord?** Quiver never replaces an app it did not install. If `Discord.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.
- **Minimum hardware**: Discord lists 2 GB of memory and a 2 GHz processor.

## License and trademarks

Discord is proprietary software by Discord Inc., free to use under its [Terms of Service](https://discord.com/terms). This arrow only downloads Discord's official builds from Discord's own servers. The Discord name, logo and banner are trademarks of Discord Inc., used here as published in its [brand kit](https://discord.com/branding); the screenshots come from Discord's official Microsoft Store listing.

```arrow
schema: "arrow@v0"

metadata:
  name: Discord
  description: Voice, video and text chat for communities and friends
  license: Proprietary
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://discord.com
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Discord Inc.
      url: https://discord.com
  media:
    icon: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/discord/icon.png
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/discord/banner.png
  tags:
    - chat
    - voice
    - desktop

# Discord updates itself after install on every platform, so the pinned
# builds below are only what the first install fetches. Memory is Discord's
# published minimum (2 GB, Microsoft Store listing); cores and disk are
# conservative estimates, since Discord publishes neither.
targets:
  # Upstream ships Linux for x86_64 only. The archive is Discord's own
  # bootstrapper: on first launch it downloads the client into
  # ~/.config/discord, outside Quiver's workdir, and keeps it updated there.
  # That directory also holds the user's session, so uninstall leaves it.
  linux/amd64:
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download Discord
          url: https://stable.dl2.discordapp.net/apps/linux/1.0.160/discord-1.0.160.tar.gz
          checksum: 3c3c874c23143aed0127c0d7ccb9ae246a80fc3d9685a33832e0541e885cf4d4
          to: ${INSTALL_PATH}/.discord.download
          timeout: 5m
        - type: extract
          title: Unpack Discord
          from: ${INSTALL_PATH}/.discord.download
          to: ${INSTALL_PATH}/app
          timeout: 2m
    expose:
      desktop:
        - name: Discord
          path: ${INSTALL_PATH}/app/Discord/discord
          icon: ${INSTALL_PATH}/app/Discord/discord.png
          categories: [Network, InstantMessaging]

  # One universal (x86_64 + arm64) DMG; requires macOS 12 or later.
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download Discord
          url: https://stable.dl2.discordapp.net/apps/osx/0.0.414/Discord.dmg
          checksum: f9b76e7de1928de5aece6e9c51d2e0f2f8cfd9db590bb50dd324f476783f24fe
          to: ${INSTALL_PATH}/.discord.download
          timeout: 15m
        - type: portable
          title: Install Discord
          from: ${INSTALL_PATH}/.discord.download
          to: ${INSTALL_PATH}/Discord
          timeout: 10m
    expose:
      desktop:
        - name: Discord
          path: auto

  # The Windows installer is Squirrel: it installs per user into
  # %LOCALAPPDATA%\Discord, outside the workdir, and creates its own Start Menu
  # shortcut, so there is no `expose` here and `uninstall` runs Squirrel's own
  # uninstaller.
  "windows/*":
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download the Discord installer
          url:
            windows/amd64: https://stable.dl2.discordapp.net/distro/app/stable/win/x64/1.0.9260/DiscordSetup.exe
            windows/arm64: https://stable.dl2.discordapp.net/distro/app/stable/win/arm64/1.0.52/DiscordSetup.exe
          checksum:
            windows/amd64: be1dee4c52227f743bc277a33a47620b6ff119e1387fe899205a8fe5d6575a90
            windows/arm64: 67f731d4aa7dd8b407861b36decdf7e30bacee96428eda19249d2fbfd083182e
          to: ${INSTALL_PATH}/DiscordSetup.exe
          timeout: 15m
        - type: run
          title: Install Discord
          command: '.\DiscordSetup.exe --silent'
          timeout: 10m
      uninstall:
        - type: run
          title: Uninstall Discord
          command: '"%LOCALAPPDATA%\Discord\Update.exe" --uninstall -s'
          timeout: 5m
          exit_on_failure: false
```
