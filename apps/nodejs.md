Node.js is a JavaScript runtime built on Chrome's V8 engine for running JavaScript outside the browser. Its event-driven, non-blocking I/O handles many connections at once without threads, which makes it a common choice for web servers, APIs, command-line tools and build tooling. It ships with npm, the package manager for the JavaScript ecosystem.

![Checking Node.js and npm, then running a script](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/nodejs/screenshots/node-run.svg)

## Features

- **Asynchronous by design**: an event loop and non-blocking I/O let one process serve many connections concurrently.
- **HTTP as a first-class citizen**: build servers and clients with the built-in `http` modules, designed for streaming and low latency.
- **npm included**: install packages from the npm registry and run project scripts with `npm` and `npx`.
- **Multi-core when you need it**: spread work across processes with `child_process` and the `cluster` module.
- **Long-term support**: this arrow installs the current LTS line, which receives fixes and security updates for an extended period.

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | The official Node.js LTS build for your processor, unpacked into Quiver's folder, with `node`, `npm` and `npx` linked into `~/.quiver/bin`. |
| Linux (x86_64 and ARM64) | The official Node.js LTS build for your processor, unpacked into Quiver's folder, with `node`, `npm` and `npx` linked into `~/.quiver/bin`. |
| Windows (x64 and ARM64) | The official Node.js LTS build for your processor, unpacked into Quiver's folder; its folder is added to your user `Path`. |

Every download is pinned to an official Node.js release from [nodejs.org/dist](https://nodejs.org/dist/) and verified against the SHA-256 checksum published in its `SHASUMS256.txt`.

### Usage

On macOS and Linux, run `quiver path setup` once so your shell finds `~/.quiver/bin`; on Windows, open a new terminal after installing. Then:

```sh
node --version
npm --version
npx --yes cowsay "hello"
```

### Good to know

- **Global packages need a home of their own.** Out of the box, `npm install -g` writes into Quiver's folder on macOS and Linux, where the commands it installs are not on your `PATH` and do not survive an update. Point npm at a folder of yours (`npm config set prefix ~/.npm-global`, then add `~/.npm-global/bin` to your `PATH`), or run tools with `npx`. On Windows, npm installs global packages into `%APPDATA%\npm`; add that folder to your `Path` to run them.
- **Your projects and npm's cache live outside Quiver's folder** (`~/.npm`, or `%LOCALAPPDATA%\npm-cache` on Windows), so uninstalling leaves them alone.
- **Another Node.js already on your `PATH`?** Whichever comes first answers to `node`; `node --version` and `which node` (`where node` on Windows) tell you which one you are running.
- **Updates come through Quiver.** These builds do not update themselves; a newer LTS release comes with a newer version of this arrow.

## License and trademarks

Node.js is free software released under the [MIT License](https://github.com/nodejs/node/blob/main/LICENSE) by the OpenJS Foundation and Node.js contributors; npm and the other bundled components carry their own licenses, listed in that file. This arrow only downloads official builds from nodejs.org. Node.js and the Node.js logo are trademarks of the OpenJS Foundation; the icon comes from the [nodejs.org repository](https://github.com/nodejs/nodejs.org), the banner is the official Node.js logo from the same repository on a dark green background, and the terminal capture shows the real output of a Node.js installed with this arrow.

```arrow
schema: "arrow@v0"

metadata:
  name: Node.js
  description: The JavaScript runtime, with npm (LTS)
  license: MIT
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://nodejs.org
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: OpenJS Foundation and Node.js contributors
      url: https://nodejs.org
  media:
    icon: https://raw.githubusercontent.com/nodejs/nodejs.org/4ffcf0386a1c09e7656c29efe6f66dd9ec153a35/apps/site/public/static/logos/nodejsHex.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/nodejs/banner.svg
  tags:
    - javascript
    - runtime
    - cli

# Node.js v24.21.0 (LTS "Krypton"), with the digests from that release's
# SHASUMS256.txt. Each archive unpacks into one node-v24.21.0-<os>-<arch>
# folder whose name differs per platform, so every concrete target spells out
# its own `expose` paths and inherits the download from its OS family's
# abstract base. Requirements are conservative estimates: Node.js publishes
# none.
targets:
  _unix:
    requirements:
      cpu_cores: 1
      ram_gb: 1
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download Node.js
          url:
            linux/amd64: https://nodejs.org/dist/v24.21.0/node-v24.21.0-linux-x64.tar.xz
            linux/arm64: https://nodejs.org/dist/v24.21.0/node-v24.21.0-linux-arm64.tar.xz
            darwin/arm64: https://nodejs.org/dist/v24.21.0/node-v24.21.0-darwin-arm64.tar.gz
            darwin/amd64: https://nodejs.org/dist/v24.21.0/node-v24.21.0-darwin-x64.tar.gz
          checksum:
            linux/amd64: fd8e59d5a511510f6a298afb548f18c7d2b1be404d8b4a27d94fbe49f56cb2d6
            linux/arm64: 6ad1325edbdb5649c379b75a237147a666c95d4f9ae8d340fef2d1575d289ad2
            darwin/arm64: bed7eea5325e1108f32ce5228ddd6a5f0f08a499ee42aa7442aea583702f6057
            darwin/amd64: 1462cb3b3046b815cf8ea436d3da450ec1a9f11dac7e5a46b0ada5305d7e8097
          to: ${INSTALL_PATH}/.nodejs.download
          timeout: 10m
        - type: extract
          title: Unpack Node.js
          from: ${INSTALL_PATH}/.nodejs.download
          to: ${INSTALL_PATH}
          timeout: 5m

  linux/amd64:
    base: _unix
    expose:
      cli:
        - name: node
          path: ${INSTALL_PATH}/node-v24.21.0-linux-x64/bin/node
        - name: npm
          path: ${INSTALL_PATH}/node-v24.21.0-linux-x64/bin/npm
        - name: npx
          path: ${INSTALL_PATH}/node-v24.21.0-linux-x64/bin/npx

  linux/arm64:
    base: _unix
    expose:
      cli:
        - name: node
          path: ${INSTALL_PATH}/node-v24.21.0-linux-arm64/bin/node
        - name: npm
          path: ${INSTALL_PATH}/node-v24.21.0-linux-arm64/bin/npm
        - name: npx
          path: ${INSTALL_PATH}/node-v24.21.0-linux-arm64/bin/npx

  darwin/arm64:
    base: _unix
    expose:
      cli:
        - name: node
          path: ${INSTALL_PATH}/node-v24.21.0-darwin-arm64/bin/node
        - name: npm
          path: ${INSTALL_PATH}/node-v24.21.0-darwin-arm64/bin/npm
        - name: npx
          path: ${INSTALL_PATH}/node-v24.21.0-darwin-arm64/bin/npx

  darwin/amd64:
    base: _unix
    expose:
      cli:
        - name: node
          path: ${INSTALL_PATH}/node-v24.21.0-darwin-x64/bin/node
        - name: npm
          path: ${INSTALL_PATH}/node-v24.21.0-darwin-x64/bin/npm
        - name: npx
          path: ${INSTALL_PATH}/node-v24.21.0-darwin-x64/bin/npx

  # On Windows a cli entry adds the folder of its .exe to the user Path; npm
  # and npx are .cmd scripts in that same folder, so one entry brings all
  # three.
  _windows:
    requirements:
      cpu_cores: 1
      ram_gb: 1
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download Node.js
          url:
            windows/amd64: https://nodejs.org/dist/v24.21.0/node-v24.21.0-win-x64.zip
            windows/arm64: https://nodejs.org/dist/v24.21.0/node-v24.21.0-win-arm64.zip
          checksum:
            windows/amd64: 158f7685b44de51f6c0df1d153526cbcd3e1bc739a8dfc607721cef75de9e541
            windows/arm64: 8779b1bde1d39f8d420e3b57aa657b39891af434d3de44a919044cec06785921
          to: ${INSTALL_PATH}/.nodejs.download
          timeout: 10m
        - type: extract
          title: Unpack Node.js
          from: ${INSTALL_PATH}/.nodejs.download
          to: ${INSTALL_PATH}
          timeout: 5m

  windows/amd64:
    base: _windows
    expose:
      cli:
        - name: node
          path: ${INSTALL_PATH}/node-v24.21.0-win-x64/node.exe

  windows/arm64:
    base: _windows
    expose:
      cli:
        - name: node
          path: ${INSTALL_PATH}/node-v24.21.0-win-arm64/node.exe
```
