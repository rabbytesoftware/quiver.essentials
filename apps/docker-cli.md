The Docker CLI is the `docker` command: it builds images, runs and manages containers, and pulls and pushes images to registries by talking to a Docker Engine. This arrow installs Docker's official static Linux build of the CLI together with Docker Compose, the tool for defining and running multi-container applications from a `compose.yaml` file.

![Running hello-world with the Docker CLI](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/docker-cli/screenshots/docker-run.svg)

## Features

- **`docker`**: build, run, stop and inspect containers, manage images, volumes and networks, and work with registries.
- **Contexts**: switch the CLI between engines (local, remote over SSH or TCP) with `docker context`.
- **`docker-compose`**: start a whole application, with its services, networks and volumes, from one `compose.yaml`.
- **Static binaries**: no packages or repositories to set up; everything sits in Quiver's folder.

## Installing with Quiver

| Platform | Available | Why |
|---|---|---|
| Linux (x86_64 and ARM64) | Yes | Docker's official static CLI build and the Docker Compose binary, unpacked into Quiver's folder, with `docker` and `docker-compose` linked into `~/.quiver/bin`. |
| macOS | No | Use the Docker Desktop arrow, which includes the CLI. |
| Windows | No | Use the Docker Desktop arrow, which includes the CLI. |

Every download is pinned to an official release: Docker 29.8.2 from [download.docker.com](https://download.docker.com/linux/static/stable/) and Docker Compose 5.6.0 from [its GitHub releases](https://github.com/docker/compose/releases), each verified against its SHA-256 checksum.

### Usage

Run `quiver path setup` once so your shell finds `~/.quiver/bin`, then:

```sh
docker --version
docker run --rm hello-world
docker-compose up -d
```

### Good to know

- **The CLI needs a Docker Engine to talk to.** This arrow installs the client, not the engine service. Use the Docker Engine of your distribution (or Docker's own packages), or point the CLI at another machine with `docker context create` or `DOCKER_HOST`. Talking to a local engine usually needs your user in the `docker` group.
- **Compose runs as `docker-compose`.** To also use it as `docker compose`, link it into `~/.docker/cli-plugins/docker-compose`.
- **Already have Docker installed?** Whichever `docker` comes first on your `PATH` answers; `which docker` tells you which one you are running.
- **Updates come through Quiver.** These binaries do not update themselves.

## License and trademarks

The Docker CLI and Docker Compose are free software released under the [Apache License 2.0](https://github.com/docker/cli/blob/master/LICENSE) by Docker, Inc. and their contributors; Docker's static archive also carries the engine binaries, under their own open-source licenses. This arrow only downloads Docker's official builds. Docker and the Docker logo are trademarks of Docker, Inc.; the icon is the Docker mark from Docker's [logo kit](https://www.docker.com/company/newsroom/media-resources/), unmodified and placed on a square canvas, the banner was generated from it, and the terminal capture shows the real output of the Linux binaries this arrow installs.

```arrow
schema: "arrow@v0"

metadata:
  name: Docker CLI
  description: The docker command and Docker Compose, for Linux
  license: Apache-2.0
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://docs.docker.com/reference/cli/docker/
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Docker, Inc.
      url: https://www.docker.com
  media:
    icon: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/docker-cli/icon.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/docker-cli/banner.svg
  tags:
    - containers
    - developer-tools
    - cli

# Linux only: macOS and Windows get the CLI with Docker Desktop. The static
# archive (Docker 29.8.2) unpacks into docker/ and also holds the engine
# binaries (dockerd, containerd, runc), which are not exposed: running an
# engine needs root. download.docker.com publishes no checksums for these
# archives, so the digests below were computed from the downloaded files;
# Compose's come from its GitHub release. Requirements are conservative
# estimates.
targets:
  "linux/*":
    requirements:
      cpu_cores: 1
      ram_gb: 1
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download the Docker CLI
          url:
            linux/amd64: https://download.docker.com/linux/static/stable/x86_64/docker-29.8.2.tgz
            linux/arm64: https://download.docker.com/linux/static/stable/aarch64/docker-29.8.2.tgz
          checksum:
            linux/amd64: 995d1ef289677f74fd58d8d2c35727b6a4ee389c69db8638a3e42d0487aa5b0f
            linux/arm64: 76a624e4a8e5da654d1150e808175125efb5a6f1b6aa1cbd9caee18f51047a50
          to: ${INSTALL_PATH}/.docker.download
          timeout: 10m
        - type: extract
          title: Unpack the Docker CLI
          from: ${INSTALL_PATH}/.docker.download
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
          to: ${INSTALL_PATH}/bin
          name: docker-compose
          timeout: 1m
    expose:
      cli:
        - name: docker
          path: ${INSTALL_PATH}/docker/docker
        - name: docker-compose
          path: ${INSTALL_PATH}/bin/docker-compose
```
