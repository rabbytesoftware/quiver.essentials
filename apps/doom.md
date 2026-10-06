DOOM, id Software's 1993 first-person shooter, played in its own window inside Quiver. You are a lone space marine on a Mars moon base overrun by demons, fighting through Episode 1, "Knee-Deep in the Dead": nine levels of corridors, keycard doors, secrets and monsters, in the original engine.

This is the **shareware Episode 1** that id Software released free of charge, not the full game. It runs as a WebAssembly build of the DOOM engine, so it behaves the same on every operating system and processor, and nothing needs to be installed on your system.

![The DOOM title screen](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/doom/screenshots/title.jpg)

## Features

- **The original game**: the DOOM engine from id Software's GPL source release, running the shareware Episode 1 content (the first episode of the original game).
- **Runs anywhere Quiver does**: one WebAssembly module, shown by Quiver's desktop shell, on Windows, macOS and Linux, on x86-64 and ARM alike.
- **Nothing to set up**: no emulator, no game files to find. The shareware data is inside the pinned build.
- **Offline**: everything is stored in Quiver's folder. The game never contacts the internet.

![Fighting an imp in Episode 1](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/doom/screenshots/imp-fight.jpg)

![Exploring E1M1](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/doom/screenshots/e1m1.jpg)

## Controls

Click the game once so it has keyboard focus, then play with the original DOOM keys:

| Key | Action |
|---|---|
| Arrow keys | Move forward and back, turn |
| `,` and `.` | Strafe left and right |
| `Ctrl` | Fire |
| `Space` | Open doors, flip switches |
| `Shift` | Run |
| `1` to `7` | Choose a weapon |
| `Esc`, `Enter` | Menu |

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS, Linux and Windows (x64 and ARM64) | A pinned build of the DOOM WebAssembly module and its web page. Quiver serves them to its own window while the arrow runs. |

The game module is pinned to release `v0.1.0` of [jacobenget/doom.wasm](https://github.com/jacobenget/doom.wasm). The page is that project's own browser example with small changes to fit the window and keep keyboard focus, kept in this repository. Both files are verified against their SHA-256 checksums.

### Good to know

- **Start it with Run, close it with Stop.** The game exists while the arrow runs; stopping the arrow closes the window. Nothing keeps running afterwards.
- **Shareware Episode 1 only.** The build always loads the shareware data. If you own the full game, you cannot use your own WAD with this arrow.
- **No sound or music, no mouse, no saved games.** Upstream has not implemented them yet. You play with the keyboard, and progress is lost when you stop.
- **The screen-melt transition freezes** for a moment while it plays in the browser, a limitation upstream documents.
- **Nothing is written outside Quiver's folder**, so removing the arrow removes everything.
- **Needs Quiver's desktop app**, in a version whose arrow-app security policy allows WebAssembly. The interface is shown by the desktop shell; there is no command-line way to play.

## License and trademarks

The DOOM engine source is released by id Software under the GNU General Public License, version 2, and this WebAssembly build is published by jacobenget under the same license, derived from [doomgeneric](https://github.com/ozkl/doomgeneric), fbDoom, Frosted Doom and Chocolate Doom. The shareware game data is copyrighted by id Software and freely redistributable in unmodified form. DOOM is a trademark of id Software LLC. The banner combines the original DOOM cover painting and the DOOM logo, both as published by Bethesda in the Steam store listing for DOOM + DOOM II; the icon (the status-bar face) is the game's own graphic, enlarged on a plain background; and the screenshots were taken from this build.

```arrow
schema: "arrow@v0"

metadata:
  name: DOOM
  description: The original 1993 DOOM, shareware Episode 1, in a Quiver window
  license: GPL-2.0
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://github.com/jacobenget/doom.wasm
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: id Software
      url: https://www.idsoftware.com
    - name: jacobenget (doom.wasm)
      url: https://github.com/jacobenget/doom.wasm
  media:
    icon: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/doom/icon.png
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/doom/banner.png
  tags:
    - game
    - fps
    - retro

# One portable target: the game is a WebAssembly module that the Quiver shell
# renders, so it is the same on every OS and CPU. Both downloads come from
# jacobenget/doom.wasm at tag v0.1.0 (commit 24bb772): the release's
# doom-v0.1.0.wasm (it embeds the shareware doom1.wad), and the page, which is
# the project's examples/browser/doom.html with small Quiver changes (window
# fitting and keyboard focus; see apps-assets/doom/index.html). The page loads
# assets/doom.wasm by a relative path and becomes the served index.html. It is
# fetched from this repository's master by raw URL, so its checksum must be
# updated whenever that file changes (pin the URL to a commit once merged). Nothing is built or written outside the
# workdir; `uninstall` only undoes the mkdir. Requirements are estimates: upstream
# states about 16 MB of module memory.
targets:
  "*":
    requirements:
      cpu_cores: 1
      ram_gb: 1
      disk_gb: 1
    lifecycle:
      install:
        # `fetch` does not create parent folders, so make the served folder.
        - type: run
          title: Create the DOOM folder
          command:
            windows/*: if not exist ui\assets mkdir ui\assets
            default: mkdir -p ui/assets
          timeout: 1m
        - type: fetch
          title: Download the DOOM page
          url: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/apps-assets/doom/index.html
          checksum: 41a4cdfa48d62c68cff5bf1e1d9c1dea5a21d7b48a4fcc50aabc45c1ca981ff2
          to: ${INSTALL_PATH}/ui/index.html
          timeout: 2m
        - type: fetch
          title: Download DOOM
          url: https://github.com/jacobenget/doom.wasm/releases/download/v0.1.0/doom-v0.1.0.wasm
          checksum: 8edfe49a7583fd975199969302d8e9adcf8e714d0af72bf3e672f991fd810faa
          to: ${INSTALL_PATH}/ui/assets/doom.wasm
          timeout: 5m
      uninstall:
        - type: run
          title: Remove the DOOM folder
          command:
            windows/*: if exist ui rmdir /s /q ui
            default: rm -rf ui
          timeout: 1m
          exit_on_failure: false
      # The interface is the static folder above, shown while this run lives,
      # so the run only has to stay alive: `tail -f /dev/null` on Unix and an
      # endless ping (no stdin needed, unlike `timeout`) on Windows.
      execute:
        - type: run
          title: Start DOOM
          command:
            windows/*: ping -t 127.0.0.1 > nul
            default: tail -f /dev/null
          ui:
            title: DOOM
            static: ui
      stop:
        - type: signal
          title: Stop DOOM
          signal: graceful
          exit_on_failure: false
```
