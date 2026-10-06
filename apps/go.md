Go is an open-source programming language from Google for building simple, reliable and efficient software. It is a small language that compiles fast into a single static binary, with concurrency built in and a standard library that covers networking, HTTP, encoding and testing. It is widely used for cloud and network services, command-line tools, web back ends and DevOps tooling.

![Checking the Go version and running a first program](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/go/screenshots/go-run.svg)

## Features

- **Fast builds, one binary**: programs compile quickly into a single static executable that is easy to ship and containerise.
- **Concurrency built in**: goroutines and channels make concurrent code part of the language.
- **A large standard library**: HTTP servers and clients, JSON, cryptography, testing and more, without extra packages.
- **Tooling included**: `go build`, `go test` (with benchmarks and profiling), `go fmt`, `go vet` and modules for dependencies, all in the one `go` command.
- **Cross-compilation**: build for another operating system or processor by setting `GOOS` and `GOARCH`.

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | The official Go distribution for your processor, unpacked into Quiver's folder, with `go` and `gofmt` linked into `~/.quiver/bin`. |
| Linux (x86_64 and ARM64) | The official Go distribution for your processor, unpacked into Quiver's folder, with `go` and `gofmt` linked into `~/.quiver/bin`. |
| Windows (x64 and ARM64) | The official Go distribution for your processor, unpacked into Quiver's folder; its `bin` folder is added to your user `Path`. |

Every download is pinned to an official Go release from [go.dev/dl](https://go.dev/dl/) and verified against the SHA-256 checksum published there.

### Usage

On macOS and Linux, run `quiver path setup` once so your shell finds `~/.quiver/bin`; on Windows, open a new terminal after installing. Then:

```sh
go version
go mod init example.com/hello
go run .
```

### Good to know

- **Everything Go needs is inside Quiver's folder.** `go` finds its standard library next to itself, so there is no `GOROOT` to set. If your environment already sets `GOROOT` (another Go version manager may), unset it, or `go` will build with that other standard library.
- **Your own Go files live elsewhere.** Modules Go downloads and programs you install with `go install` go to `~/go` (`%USERPROFILE%\go` on Windows), which uninstalling leaves alone. Add `~/go/bin` to your `PATH` to run programs installed with `go install`.
- **Another Go already on your `PATH`?** Whichever comes first on your `PATH` answers to `go`; `go version` tells you which one you are running. On Windows, Quiver appends to your user `Path`, so a Go installed system-wide comes first.
- **Updates come through Quiver.** This distribution does not update itself; a newer Go comes with a newer version of this arrow.

## License and trademarks

Go is free software released by the Go Authors under a [BSD-style license](https://go.dev/LICENSE). This arrow only downloads Go's official releases from go.dev. Go and the Go logo are trademarks of Google LLC. The icon is the gopher from [go.dev](https://go.dev) (the Go gopher was designed by Renée French and is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)); the banner sets that gopher beside the official Go logo from the same [go.dev repository](https://github.com/golang/website) on Go's blue, and the terminal capture shows the real output of a Go installed with this arrow.

```arrow
schema: "arrow@v0"

metadata:
  name: Go
  description: The Go programming language and its toolchain
  license: BSD-3-Clause
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://go.dev
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: The Go Authors
      url: https://go.dev
  media:
    icon: https://raw.githubusercontent.com/golang/website/32881aa55f0d81413cda4fe43e0236d0cae2b2ec/_content/images/favicon-gopher.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/go/banner.svg
  tags:
    - go
    - programming-language
    - cli

# Every archive is an official go1.27.1 release from go.dev/dl, with the
# SHA-256 go.dev publishes for it. Each holds a single top-level go/ tree;
# `go` locates its standard library from its own resolved path, so the
# symlinks in ~/.quiver/bin need no GOROOT. Requirements are conservative
# estimates: Go publishes none.
targets:
  _unix:
    requirements:
      cpu_cores: 1
      ram_gb: 1
      disk_gb: 1
    expose:
      cli:
        - name: go
          path: ${INSTALL_PATH}/go/bin/go
        - name: gofmt
          path: ${INSTALL_PATH}/go/bin/gofmt

  "linux/*":
    base: _unix
    lifecycle:
      install:
        - type: fetch
          title: Download Go
          url:
            linux/amd64: https://go.dev/dl/go1.27.1.linux-amd64.tar.gz
            linux/arm64: https://go.dev/dl/go1.27.1.linux-arm64.tar.gz
          checksum:
            linux/amd64: 63d339f0da5ab53635a56f2490a7984dfe12dfcff22ad749f63edaf590168445
            linux/arm64: 3450b45a3f9ee8568792736a5c5e70a1f2e9b36c35a8f74958c03e51d7d92bec
          to: ${INSTALL_PATH}/.go.download
          timeout: 10m
        - type: extract
          title: Unpack Go
          from: ${INSTALL_PATH}/.go.download
          to: ${INSTALL_PATH}
          timeout: 5m

  "darwin/*":
    base: _unix
    lifecycle:
      install:
        - type: fetch
          title: Download Go
          url:
            darwin/arm64: https://go.dev/dl/go1.27.1.darwin-arm64.tar.gz
            darwin/amd64: https://go.dev/dl/go1.27.1.darwin-amd64.tar.gz
          checksum:
            darwin/arm64: ee215d57e0ec269c60cc9ceca68e6bda321ba9ee5afe24f4b0988703c2d87d12
            darwin/amd64: 8f8f52c6649542cf027bbc9b9c68d1ec042f9f34808a40413f0b8b3f66f3caa4
          to: ${INSTALL_PATH}/.go.download
          timeout: 10m
        - type: extract
          title: Unpack Go
          from: ${INSTALL_PATH}/.go.download
          to: ${INSTALL_PATH}
          timeout: 5m

  # On Windows a cli entry adds the folder of its .exe to the user Path, so
  # one entry for go.exe also brings gofmt.exe from the same bin folder.
  "windows/*":
    requirements:
      cpu_cores: 1
      ram_gb: 1
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download Go
          url:
            windows/amd64: https://go.dev/dl/go1.27.1.windows-amd64.zip
            windows/arm64: https://go.dev/dl/go1.27.1.windows-arm64.zip
          checksum:
            windows/amd64: a3911b5e0e1b1053f25ed0675f4c1c6aad1e2bfcf253df2b9be4caabd2edd95d
            windows/arm64: 13b69b87bb0e83f96bc68560a8cace7f0343b1e03469f1110ea18d17e3234069
          to: ${INSTALL_PATH}/.go.download
          timeout: 10m
        - type: extract
          title: Unpack Go
          from: ${INSTALL_PATH}/.go.download
          to: ${INSTALL_PATH}
          timeout: 5m
    expose:
      cli:
        - name: go
          path: ${INSTALL_PATH}/go/bin/go.exe
```
