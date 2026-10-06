Docker builds, runs and shares applications in containers. This arrow installs the most complete Docker each system allows without administrator rights: **Docker Desktop** on macOS and Windows, Docker's app that bundles the Docker Engine, the `docker` CLI, Docker Compose, Buildx and a dashboard in a virtual machine it manages for you; and on Linux, the **Docker Engine in rootless mode**, Docker's own way to run the full engine as your user, with the `docker` CLI, Compose and Buildx, so you never need `sudo` or the `docker` group.

![Docker Desktop's Containers view](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/docker/screenshots/containers.jpg)

## Features

- **Containers from your terminal**: build, run, stop and inspect containers, and manage images, volumes and networks with `docker`.
- **Docker Compose**: `docker compose` starts a whole application, with its services, networks and volumes, from one `compose.yaml`.
- **Docker Buildx**: `docker buildx` builds images with BuildKit, including multi-platform builds.
- **Contexts**: switch the CLI between engines (local, rootless, remote over SSH or TCP) with `docker context`.
- **Docker Desktop on macOS and Windows**: a dashboard to start, stop and inspect containers and browse images, volumes and builds; an optional single-node Kubernetes cluster; and extensions from its marketplace.

![Rootless Docker on Linux running hello-world, with Compose and Buildx](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/docker/screenshots/docker-run.svg)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | **Docker Desktop**: Docker's official DMG for your processor, as `Docker.app` in Applications. Requires macOS 14 or later and at least 4 GB of RAM. |
| Windows (x64 and ARM64) | **Docker Desktop**: Docker's official installer, run in per-user mode, which installs into `%LOCALAPPDATA%\Programs\DockerDesktop` without administrator rights. Requires Windows 10 22H2 or Windows 11 23H2 or later, WSL 2.1.5 or later, hardware virtualization and 8 GB of RAM. |
| Linux (x86_64 and ARM64) | **Docker Engine (rootless), CLI, Compose and Buildx**: Docker's official static binaries, unpacked into Quiver's folder and set up with Docker's own rootless setup tool. The engine runs as your user under a systemd user service, `docker` is linked into `~/.quiver/bin`, and Compose and Buildx are linked as CLI plugins. Docker Desktop for Linux ships only as distribution packages, which Quiver cannot install. |

Every download is pinned to an official release (Docker Desktop 4.93.0; on Linux, Docker 29.8.2, Docker Compose 5.6.0 and Docker Buildx 0.37.2) and verified against its SHA-256 checksum.

### On macOS and Windows (Docker Desktop)

- **Docker Desktop is free for personal use, education, non-commercial open source and small businesses**, and needs a paid subscription for larger companies: see [Docker's pricing](https://www.docker.com/pricing/). On Windows, Quiver accepts Docker's license during the silent install; by installing, you accept the [Docker Subscription Service Agreement](https://www.docker.com/legal/docker-subscription-service-agreement/).
- **On macOS, Docker Desktop asks for your password on first launch** to set up the privileged parts it needs.
- **On Windows, WSL 2 must be installed first.** Per-user mode is in beta at Docker.
- **Docker Desktop keeps itself up to date.** Quiver installs the release pinned here; from then on Docker's own updater installs new versions.
- **Your containers, images and volumes live outside Quiver's folder.** On Windows, uninstalling through Quiver runs Docker's own uninstaller, which deletes them. On macOS, uninstalling removes `Docker.app` and leaves Docker's data in place; to delete it too, use **Troubleshoot → Uninstall** in Docker Desktop first.
- **Already have Docker Desktop?** Quiver never replaces an app it did not install. If `Docker.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.

### On Linux (rootless Docker Engine)

Run `quiver path setup` once so your shell finds `~/.quiver/bin`, then:

```sh
docker run --rm hello-world
docker compose up -d
docker buildx build .
```

- **What the install sets up:** a systemd user service (`~/.config/systemd/user/docker.service`) that starts the engine whenever you log in, the `rootless` CLI context (selected for you, so `docker` talks to it), and the Compose and Buildx plugins in `~/.docker/cli-plugins`. Run `systemctl --user (start|stop|restart) docker` to control the engine.
- **One-time system prerequisites.** Rootless mode needs `newuidmap`/`newgidmap` (the `uidmap` package), `iptables`, and at least 65,536 subordinate IDs for your user in `/etc/subuid` and `/etc/subgid`, which most distributions set up already. On Ubuntu 24.04 and later it also needs an AppArmor profile. These need `sudo` once: if one is missing, the install stops and prints the exact commands to run, and you install again afterwards.
- **It needs a systemd user session**, as on any desktop login or SSH session of a systemd distribution. To keep the engine running after you log out, run `sudo loginctl enable-linger $USER` once.
- **Rootless differences:** publishing ports below 1024 needs `sudo sysctl net.ipv4.ip_unprivileged_port_start=0` (or a higher port), and CPU and memory limits need cgroup v2, the default on current distributions.
- **Already have Docker?** If a rootful Docker Engine is running, Docker's setup tool refuses to install alongside it. A rootless Docker you set up yourself is left untouched: the install stops instead of replacing it. Existing plugins in `~/.docker/cli-plugins` that Quiver did not link are kept.
- **Uninstalling** stops and removes the service, deletes the `rootless` context (the CLI goes back to `default`) and removes the plugin links. Your images and containers stay in `~/.local/share/docker`; delete them with `rootlesskit rm -rf ~/.local/share/docker` before uninstalling if you want them gone.
- **Updates come through Quiver.** Updating installs the new release and moves the service over to it.

## License and trademarks

Docker Desktop is proprietary software by Docker, Inc., licensed under the [Docker Subscription Service Agreement](https://www.docker.com/legal/docker-subscription-service-agreement/). The Docker Engine, CLI, Compose, Buildx and RootlessKit installed on Linux are free software released under the [Apache License 2.0](https://github.com/moby/moby/blob/master/LICENSE) by their authors and contributors. This arrow only downloads Docker's official builds. Docker and the Docker logo are trademarks of Docker, Inc.; the icon is the Docker mark from Docker's [logo kit](https://www.docker.com/company/newsroom/media-resources/), unmodified and placed on a square canvas, the banner is the social image from [docs.docker.com](https://docs.docker.com), the Docker Desktop screenshot comes from Docker's [Docker Desktop page](https://www.docker.com/products/docker-desktop/), and the terminal capture shows the real output of the rootless setup this arrow installs on Linux.

```arrow
schema: "arrow@v0"

metadata:
  name: Docker
  description: Docker Desktop on macOS and Windows, the rootless Docker Engine on Linux
  # Docker Desktop (macOS, Windows) is proprietary; the engine, CLI, Compose,
  # Buildx and RootlessKit installed on Linux are Apache-2.0.
  license: Proprietary AND Apache-2.0
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://www.docker.com
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Docker, Inc.
      url: https://www.docker.com
  media:
    icon: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/docker/icon.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/docker/banner.png
  tags:
    - containers
    - developer-tools
    - desktop
    - cli

# Each OS gets what Docker ships for it: Docker Desktop on macOS and Windows,
# whose own Linux build exists only as deb/rpm packages Quiver cannot install,
# and the static CLI with Compose on Linux. Requirements are Docker Desktop's
# published minimums where it has them, otherwise conservative estimates.
targets:
  # Docker Desktop 4.93.0 (build 240920), one DMG per processor, with the
  # SHA-256 from the checksums.txt Docker publishes next to each download;
  # requires macOS 14 or later. `portable` moves Docker.app to Applications,
  # so the app is gone by the time an `uninstall` could run Docker's own
  # uninstaller: there is none, and Docker's data stays (documented in the
  # readme). Docker Desktop updates itself after install.
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 4
    lifecycle:
      install:
        - type: fetch
          title: Download Docker Desktop
          url:
            darwin/arm64: https://desktop.docker.com/mac/main/arm64/240920/Docker.dmg
            darwin/amd64: https://desktop.docker.com/mac/main/amd64/240920/Docker.dmg
          checksum:
            darwin/arm64: bf062f45334c711bd2fc2ed47a5588d050fbb950be3ae3aa4ac9826f04ad4dba
            darwin/amd64: 14b07180f629dd7c16707b371038b30cbf1c8f8f525a1bcd28707b99f9600b20
          to: ${INSTALL_PATH}/.docker.download
          timeout: 30m
        - type: portable
          title: Install Docker Desktop
          from: ${INSTALL_PATH}/.docker.download
          to: ${INSTALL_PATH}/Docker
          timeout: 15m
    expose:
      desktop:
        - name: Docker
          path: auto

  # Docker Desktop 4.93.0 in per-user mode (--user): no administrator rights,
  # installs into %LOCALAPPDATA%\Programs\DockerDesktop with its own Start
  # Menu shortcut, so there is no `expose` here. `start /w` waits for the
  # installer, as Docker's documentation does. Requires WSL 2, hardware
  # virtualization and 8 GB of RAM.
  "windows/*":
    requirements:
      cpu_cores: 2
      ram_gb: 8
      disk_gb: 4
    lifecycle:
      install:
        - type: fetch
          title: Download Docker Desktop
          url:
            windows/amd64: https://desktop.docker.com/win/main/amd64/240920/Docker%20Desktop%20Installer.exe
            windows/arm64: https://desktop.docker.com/win/main/arm64/240920/Docker%20Desktop%20Installer.exe
          checksum:
            windows/amd64: c139124c9cf71477dc565c3c0ea5a18f90b93d68ebe9aaa848a065960416c0bc
            windows/arm64: d1b281009f289c3c163db65e28b93c9637465c075ddd6b6fb097a7d2a18ae24a
          to: ${INSTALL_PATH}/DockerDesktopInstaller.exe
          timeout: 30m
        - type: run
          title: Install Docker Desktop
          command: 'start /w "" .\DockerDesktopInstaller.exe install --user --quiet --accept-license'
          timeout: 20m
      uninstall:
        - type: run
          title: Uninstall Docker Desktop
          command: 'start /w "" "%LOCALAPPDATA%\Programs\DockerDesktop\Docker Desktop Installer.exe" uninstall'
          timeout: 15m
          exit_on_failure: false

  # Linux: Docker Engine in rootless mode, the most complete Docker that needs
  # no root (Docker Desktop for Linux and the rootful engine both need
  # packages or root). Docker 29.8.2 static binaries (CLI, dockerd,
  # containerd, runc) plus the rootless extras (rootlesskit,
  # dockerd-rootless.sh and Docker's own dockerd-rootless-setuptool.sh), with
  # Compose and Buildx as CLI plugins. download.docker.com publishes no
  # checksums for the static archives, so their digests were computed from
  # the downloaded files; Compose's and Buildx's come from their GitHub
  # releases.
  #
  # Install runs Docker's setup tool, which writes a systemd user unit
  # (~/.config/systemd/user/docker.service) that starts dockerd from this
  # workdir, and creates and selects the "rootless" CLI context. The tool
  # checks the system prerequisites (newuidmap, /etc/subuid, AppArmor) and
  # prints the one-time sudo commands when one is missing. A unit that does
  # not point into a Quiver workdir of this arrow is someone else's rootless
  # Docker and is left alone; one that does (an older release, during an
  # update reinstall) is uninstalled first, so the unit never points at a
  # workdir Quiver has removed. Plugin links in ~/.docker/cli-plugins are
  # only replaced when missing or already Quiver's. Uninstall undoes the unit,
  # the context and the plugin links only when they belong to this workdir;
  # images and containers in ~/.local/share/docker stay.
  "linux/*":
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 4
    lifecycle:
      install:
        - type: fetch
          title: Download Docker
          url:
            linux/amd64: https://download.docker.com/linux/static/stable/x86_64/docker-29.8.2.tgz
            linux/arm64: https://download.docker.com/linux/static/stable/aarch64/docker-29.8.2.tgz
          checksum:
            linux/amd64: 995d1ef289677f74fd58d8d2c35727b6a4ee389c69db8638a3e42d0487aa5b0f
            linux/arm64: 76a624e4a8e5da654d1150e808175125efb5a6f1b6aa1cbd9caee18f51047a50
          to: ${INSTALL_PATH}/.docker.download
          timeout: 10m
        - type: extract
          title: Unpack Docker
          from: ${INSTALL_PATH}/.docker.download
          to: ${INSTALL_PATH}
          timeout: 5m
        - type: fetch
          title: Download the rootless extras
          url:
            linux/amd64: https://download.docker.com/linux/static/stable/x86_64/docker-rootless-extras-29.8.2.tgz
            linux/arm64: https://download.docker.com/linux/static/stable/aarch64/docker-rootless-extras-29.8.2.tgz
          checksum:
            linux/amd64: 707ebf6a5afd88104086e7b6749997b2366e816aeaf2c3ef2305b08fde9ee007
            linux/arm64: f8f759dfeecb5bbe2c963232a1b9380e133f677dc0579263e4ca04c69f40aa47
          to: ${INSTALL_PATH}/.docker-rootless.download
          timeout: 10m
        - type: extract
          title: Unpack the rootless extras
          from: ${INSTALL_PATH}/.docker-rootless.download
          to: ${INSTALL_PATH}
          timeout: 5m
        - type: fetch
          title: Download Docker Compose
          url:
            linux/amd64: https://github.com/docker/compose/releases/download/v5.6.0/docker-compose-linux-x86_64
            linux/arm64: https://github.com/docker/compose/releases/download/v5.6.0/docker-compose-linux-aarch64
          checksum:
            linux/amd64: 40343e21ca777173e69cff5dbafeb37c6f81f3b0d57d9e597f036e95eb63e76a
            linux/arm64: 733ec76717ceb59052a9609b9dadfb523b2df8eab57a54212872d10a58078ea2
          to: ${INSTALL_PATH}/.docker-compose.download
          timeout: 10m
        - type: portable
          title: Install Docker Compose
          from: ${INSTALL_PATH}/.docker-compose.download
          to: ${INSTALL_PATH}/compose
          name: docker-compose
          timeout: 1m
        - type: fetch
          title: Download Docker Buildx
          url:
            linux/amd64: https://github.com/docker/buildx/releases/download/v0.37.2/buildx-v0.37.2.linux-amd64
            linux/arm64: https://github.com/docker/buildx/releases/download/v0.37.2/buildx-v0.37.2.linux-arm64
          checksum:
            linux/amd64: 982ca20490b45ed1ec8d99795974d3d874a358f75938c9c237305010e6b7e548
            linux/arm64: efa38cb7aa7db2dbb9ad049b00b0a9737f66f033626177b5a4e845184ad7ab29
          to: ${INSTALL_PATH}/.docker-buildx.download
          timeout: 10m
        - type: portable
          title: Install Docker Buildx
          from: ${INSTALL_PATH}/.docker-buildx.download
          to: ${INSTALL_PATH}/buildx
          name: docker-buildx
          timeout: 1m
        - type: run
          title: Set up rootless Docker
          command: |
            set -e
            unit="$HOME/.config/systemd/user/docker.service"
            if [ -f "$unit" ] && ! grep -q "/quiver.essentials/docker@" "$unit"; then
              echo "A rootless Docker that Quiver did not install is already set up ($unit); leaving it alone." >&2
              exit 1
            fi
            if ! systemctl --user show-environment > /dev/null 2>&1; then
              echo "Rootless Docker needs a systemd user session (systemctl --user)." >&2
              exit 1
            fi
            mv docker-rootless-extras/* docker/
            rmdir docker-rootless-extras
            PATH="$PWD/docker:$PATH"
            export PATH
            if [ -f "$unit" ]; then
              dockerd-rootless-setuptool.sh uninstall
            fi
            dockerd-rootless-setuptool.sh install
            mkdir -p "$HOME/.docker/cli-plugins"
            for plugin in compose/docker-compose buildx/docker-buildx; do
              link="$HOME/.docker/cli-plugins/$(basename "$plugin")"
              if [ -e "$link" ] || [ -L "$link" ]; then
                case "$(readlink "$link")" in
                  */quiver.essentials/docker@*) ;;
                  *) echo "Keeping the existing $link" >&2; continue ;;
                esac
              fi
              ln -sfn "$PWD/$plugin" "$link"
            done
          timeout: 10m
      uninstall:
        - type: run
          title: Remove rootless Docker
          command: |
            PATH="$PWD/docker:$PATH"
            export PATH
            unit="$HOME/.config/systemd/user/docker.service"
            if [ -f "$unit" ] && grep -q "$PWD/docker" "$unit"; then
              dockerd-rootless-setuptool.sh uninstall
            fi
            for name in docker-compose docker-buildx; do
              link="$HOME/.docker/cli-plugins/$name"
              case "$(readlink "$link")" in
                "$PWD"/*) rm -f "$link" ;;
              esac
            done
          timeout: 5m
          exit_on_failure: false
    expose:
      cli:
        - name: docker
          path: ${INSTALL_PATH}/docker/docker
        - name: docker-compose
          path: ${INSTALL_PATH}/compose/docker-compose
```
