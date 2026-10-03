Docker Desktop is Docker's app for building, running and sharing containers on your own computer. It bundles the Docker Engine, the `docker` CLI, Docker Compose, Docker Build and an optional Kubernetes cluster, runs them in a lightweight virtual machine it manages for you, and adds a dashboard to see and control your containers, images and volumes.

![Docker Desktop's Containers view](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/docker-desktop/screenshots/containers.jpg)

## Features

- **Everything in one install**: Docker Engine, the `docker` CLI, Compose and Build, ready to use from your terminal.
- **A dashboard**: start, stop and inspect containers, and browse images, volumes and builds.
- **Kubernetes**: an optional single-node cluster for local testing.
- **Extensions**: add third-party tools to Docker Desktop from its marketplace.
- **Managed virtual machine**: Docker Desktop runs Linux containers in a VM it sets up for you.

## Installing with Quiver

| Platform | Available | What Quiver installs |
|---|---|---|
| macOS (Apple silicon and Intel) | Yes | Docker's official DMG for your processor, as `Docker.app` in Applications. Requires macOS 14 or later and at least 4 GB of RAM. |
| Windows (x64 and ARM64) | Yes | Docker's official installer, run in per-user mode, which installs into `%LOCALAPPDATA%\Programs\DockerDesktop` without administrator rights. Requires Windows 10 22H2 or Windows 11 23H2 or later, WSL 2.1.5 or later, hardware virtualization and 8 GB of RAM. |
| Linux | No | Docker Desktop for Linux ships only as distribution packages (deb, rpm), which Quiver cannot install. Use the Docker CLI arrow from this collection, or [Docker's own packages](https://docs.docker.com/desktop/setup/install/linux/). |

Every download is pinned to one Docker Desktop release (4.93.0) and verified against the SHA-256 checksum Docker publishes for it.

### Good to know

- **Docker Desktop is free for personal use, education, non-commercial open source and small businesses**, and needs a paid subscription for larger companies: see [Docker's pricing](https://www.docker.com/pricing/). On Windows, Quiver accepts Docker's license during the silent install; by installing, you accept the [Docker Subscription Service Agreement](https://www.docker.com/legal/docker-subscription-service-agreement/).
- **On macOS, Docker Desktop asks for your password on first launch** to set up the privileged parts it needs.
- **On Windows, WSL 2 must be installed first.** Per-user mode is in beta at Docker.
- **Docker Desktop keeps itself up to date.** Quiver installs the release pinned here; from then on Docker's own updater installs new versions.
- **Your containers, images and volumes live outside Quiver's folder.** On Windows, uninstalling through Quiver runs Docker's own uninstaller, which deletes them. On macOS, uninstalling removes `Docker.app` and leaves Docker's data in place; to delete it too, use **Troubleshoot → Uninstall** in Docker Desktop first.
- **Already have Docker Desktop?** Quiver never replaces an app it did not install. If `Docker.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.

## License and trademarks

Docker Desktop is proprietary software by Docker, Inc., licensed under the [Docker Subscription Service Agreement](https://www.docker.com/legal/docker-subscription-service-agreement/). This arrow only downloads Docker's official builds from Docker's own servers. Docker and the Docker logo are trademarks of Docker, Inc.; the icon is the Docker mark from Docker's [logo kit](https://www.docker.com/company/newsroom/media-resources/), unmodified and placed on a square canvas, the banner was generated from it, and the screenshot comes from Docker's [Docker Desktop page](https://www.docker.com/products/docker-desktop/).

```arrow
schema: "arrow@v0"

metadata:
  name: Docker Desktop
  description: Build, run and share containers on your Mac or PC
  license: Proprietary
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://www.docker.com/products/docker-desktop/
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Docker, Inc.
      url: https://www.docker.com
  media:
    icon: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/docker-desktop/icon.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/docker-desktop/banner.svg
  tags:
    - containers
    - developer-tools
    - desktop

# Docker Desktop 4.93.0 (build 240920), with the SHA-256 from the
# checksums.txt Docker publishes next to each download. Docker Desktop for
# Linux ships only as deb/rpm packages, which Quiver cannot install. Docker
# Desktop updates itself after install.
targets:
  # One DMG per processor; requires macOS 14 or later. `portable` moves
  # Docker.app to Applications, so the app is gone by the time an `uninstall`
  # could run Docker's own uninstaller: there is none, and Docker's data
  # stays (documented in the readme).
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
          to: ${INSTALL_PATH}/.docker-desktop.download
          timeout: 30m
        - type: portable
          title: Install Docker Desktop
          from: ${INSTALL_PATH}/.docker-desktop.download
          to: ${INSTALL_PATH}/Docker
          timeout: 15m
    expose:
      desktop:
        - name: Docker
          path: auto

  # The per-user install (--user) needs no administrator rights and installs
  # into %LOCALAPPDATA%\Programs\DockerDesktop with its own Start Menu
  # shortcut, so there is no `expose` here. `start /w` waits for the
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
```
