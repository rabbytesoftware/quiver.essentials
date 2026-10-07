Slack is a workspace for team communication: conversations are organised into channels, with direct messages, threads, huddles for quick audio and video calls, shared files and canvases, and integrations with the other tools a team uses.

![Slack on the desktop, showing a channel, a thread and the sidebar](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/slack/screenshots/workspace.jpg)

## Features

- **Channels and direct messages**: public and private channels for topics and projects, plus one-to-one and group messages.
- **Threads**: keep replies together so a busy channel stays readable.
- **Huddles**: drop into a lightweight audio or video call from any channel or message.
- **Canvases and files**: share documents, notes and files next to the conversation.
- **Apps and integrations**: connect calendars, ticketing and other tools so their updates arrive in Slack.
- **Search and activity**: find past messages and files, and catch up on mentions and unreads.

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | Slack's official universal DMG, as `Slack.app` in Applications. |
| Windows (x64) | Slack's official installer, run silently for your user. It installs into your user profile and adds its own Start Menu shortcut. |
| Windows (ARM64) | Slack's official native ARM64 MSIX package, installed for your user with `Add-AppxPackage`. It needs no administrator rights. |

Not supported: **Linux**. Slack publishes its Linux client only as `.deb` and `.rpm` packages, with no AppImage or tarball that Quiver can unpack on every distribution, so this arrow does not support Linux.

Every download is pinned to an official Slack build from Slack's own download servers and verified against its SHA-256 checksum. Slack publishes no checksums, so the digests were computed from the files at the time of writing.

### Good to know

- **Slack keeps itself up to date.** Quiver installs the build pinned here; from then on Slack's own updater applies.
- **On Windows x64, Slack installs into `%LOCALAPPDATA%\slack`**, not into Quiver's folder. Uninstalling through Quiver runs Slack's own uninstaller. Your sign-in and data are kept by Slack in your profile.
- **On Windows ARM64, Slack is a packaged (MSIX) app.** Windows must allow installing apps outside the Microsoft Store (the default on current Windows 11). Uninstalling through Quiver removes the package. Do not install both this and the Microsoft Store version.
- **Already have Slack?** Quiver never replaces an app it did not install. If `Slack.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.
- **Requirements**: Slack does not publish hardware minimums on its download pages; Quiver asks for 2 cores and 4 GB of memory as a conservative estimate.

## License and trademarks

Slack is proprietary software by Slack Technologies, LLC, a Salesforce company, free to download and used under Slack's [terms of service](https://slack.com/terms-of-service). This arrow only downloads Slack's official builds from Slack's own servers. The Slack name and logo are trademarks of Slack Technologies, LLC; the icon is the Slack logo as published on slack.com, the banner combines the Slack lockup (from its unfurl image on slack.com) with the app-window hero image from the slack.com homepage, and the screenshot comes from Slack's [download page](https://slack.com/downloads/mac).

```arrow
schema: "arrow@v0"

metadata:
  name: Slack
  description: Team messaging, huddles and file sharing in channels
  license: Proprietary
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://slack.com
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Slack Technologies, LLC
      url: https://slack.com
  media:
    icon: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/slack/icon.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/slack/banner.png
  tags:
    - chat
    - team
    - desktop

# Slack 4.52.178, the versioned URLs
# served by slack.com/api/desktop.latestRelease. Slack publishes no checksums,
# so every SHA-256 below was computed from the downloaded file. Slack
# publishes no hardware minimums; requirements are conservative estimates.
targets:

  # One universal (x86_64 + arm64) DMG.
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download Slack
          url: https://downloads.slack-edge.com/desktop-releases/mac/universal/4.52.178/Slack-4.52.178-macOS.dmg
          checksum: 8909c222b805552c18b3e86400dc6b9007f88b99adba10bc210d39d7767e116f
          to: ${INSTALL_PATH}/.slack.download
          timeout: 15m
        - type: portable
          title: Install Slack
          from: ${INSTALL_PATH}/.slack.download
          to: ${INSTALL_PATH}/Slack
          timeout: 10m
    expose:
      desktop:
        - name: Slack
          path: auto

  # SlackSetup.exe is a Squirrel installer for x64: it installs per user into
  # %LOCALAPPDATA%\slack, outside the workdir, and creates its own Start Menu
  # shortcut, so there is no `expose` and `uninstall` runs Squirrel's own
  # uninstaller. (Slack's installer has no ARM64 variant: asking for
  # arch=arm64&variant=exe returns desktop_variant_arch_mismatch.)
  windows/amd64:
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download the Slack installer
          url: https://downloads.slack-edge.com/desktop-releases/windows/x64/4.52.178/SlackSetup.exe
          checksum: edec34a6cd42a33da7556bac0ceb4046ae9e37ac0b1a4ae83a1b321c381ee062
          to: ${INSTALL_PATH}/SlackSetup.exe
          timeout: 15m
        - type: run
          title: Install Slack
          command: '.\SlackSetup.exe --silent >nul 2>&1 <nul'
          timeout: 10m
      uninstall:
        - type: run
          title: Uninstall Slack
          command: '"%LOCALAPPDATA%\slack\Update.exe" --uninstall -s'
          timeout: 5m
          exit_on_failure: false

  # Native ARM64 build, published only as an MSIX (signed by Slack, per-user
  # install, no administrator rights). The file name must end in .msix.
  windows/arm64:
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download the Slack package
          url: https://downloads.slack-edge.com/desktop-releases/windows/arm64/4.52.178/Slack.msix
          checksum: 6c764aa2816a1917d1f9aff9ff7868775d51c06378b0331a78389206091f8372
          to: ${INSTALL_PATH}/Slack.msix
          timeout: 15m
        - type: run
          title: Install Slack
          command: 'powershell -NoProfile -ExecutionPolicy Bypass -Command "Add-AppxPackage -Path (Resolve-Path .\Slack.msix).Path"'
          timeout: 10m
      uninstall:
        - type: run
          title: Uninstall Slack
          command: 'powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-AppxPackage -Name com.tinyspeck.slackdesktop | Remove-AppxPackage"'
          timeout: 5m
          exit_on_failure: false
```
