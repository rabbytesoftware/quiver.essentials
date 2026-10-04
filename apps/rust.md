Rust is a programming language for building reliable and efficient software. It has no garbage collector and no runtime, so it fits performance-critical services and embedded devices, and its type system and ownership model rule out whole classes of memory and threading bugs at compile time. This arrow installs Rust the way the Rust project recommends: through rustup, the official toolchain installer, with the current stable toolchain.

![Creating and running a first Rust program with Cargo](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/rust/screenshots/cargo-run.svg)

## Features

- **Memory safety without a garbage collector**: ownership and borrowing are checked by the compiler, so memory and thread-safety bugs are caught before the program runs.
- **Fast and lean**: compiled to native code, with no runtime to ship.
- **Cargo**: one tool to create projects, build them, run tests, and fetch dependencies from crates.io.
- **A friendly compiler**: error messages that point at the problem and often suggest the fix.
- **Tooling included**: `rustfmt` formats code, Clippy lints it, and rust-analyzer powers editor support.
- **rustup**: switch between stable, beta and nightly, add targets for cross-compiling, and update everything with `rustup update`.

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | rustup and the stable toolchain, in `~/.cargo` and `~/.rustup`. |
| Linux (x86_64 and ARM64) | rustup and the stable toolchain, in `~/.cargo` and `~/.rustup`. |
| Windows (x64 and ARM64) | rustup and the stable MSVC toolchain, in `%USERPROFILE%\.cargo` and `%USERPROFILE%\.rustup`. |

Quiver downloads the official rustup installer pinned here and verifies it against its published SHA-256 checksum; rustup then downloads the current stable toolchain from the Rust project's servers and verifies it itself.

### Usage

Open a new terminal after installing, then:

```sh
rustc --version
cargo new hello
cd hello
cargo run
```

### Good to know

- **Rust lives where rustup puts it**, in `~/.cargo` and `~/.rustup` (`%USERPROFILE%\.cargo` and `%USERPROFILE%\.rustup` on Windows), not in Quiver's folder, and rustup adds `~/.cargo/bin` to your `PATH` itself: in your shell profiles on macOS and Linux, in your user `Path` on Windows.
- **You need a linker.** On macOS, install the Xcode Command Line Tools (`xcode-select --install`); on Linux, a C compiler such as GCC or Clang; on Windows, the Visual Studio C++ Build Tools. rustup warns when they are missing.
- **Updating runs `rustup update`**, which updates rustup and every installed toolchain in place.
- **Uninstalling runs `rustup self uninstall`**, which deletes `~/.cargo` and `~/.rustup` entirely, including the toolchains, the crates cache and every program installed with `cargo install`, and undoes its `PATH` changes.
- **Already have rustup?** Quiver will not install over it, so uninstalling through Quiver never removes a Rust you set up yourself. Keep using `rustup update`.

## License and trademarks

Rust and rustup are free software, dual-licensed under the [MIT](https://github.com/rust-lang/rust/blob/master/LICENSE-MIT) and [Apache 2.0](https://github.com/rust-lang/rust/blob/master/LICENSE-APACHE) licenses by the Rust Project Developers. This arrow only downloads the official rustup installer from static.rust-lang.org. Rust and the Rust logo are trademarks of the Rust Foundation; the icon comes from the Rust Project's [rust-artwork](https://github.com/rust-lang/rust-artwork) repository (licensed under CC BY 4.0), the banner is the Rust website's social image, and the terminal capture shows the real output of a Rust installed with this arrow. This arrow is not an official Rust project distribution and is not endorsed by the Rust project.

```arrow
schema: "arrow@v0"

metadata:
  name: Rust
  description: The Rust programming language, installed with rustup
  license: MIT OR Apache-2.0
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://www.rust-lang.org
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: The Rust Project Developers
      url: https://www.rust-lang.org
  media:
    icon: https://raw.githubusercontent.com/rust-lang/rust-artwork/7b54b6689dc310db2f301d7bcda847f016bd447c/logo/rust-logo-white-outline.svg
    banner: https://raw.githubusercontent.com/rust-lang/www.rust-lang.org/74c84e2dda2b337f4de2de8d8ea4368ab458fc35/static/images/rust-social-wide.jpg
  tags:
    - rust
    - programming-language
    - cli

# rustup is Rust's official installer, and what the Rust project tells every
# platform to use. It installs into ~/.cargo and ~/.rustup (outside the
# workdir) and puts ~/.cargo/bin on PATH itself, so there is no `expose` here:
# its proxies (rustc, cargo, ...) need RUSTUP_HOME and only find it at its
# default location. rustup-init 1.29.1 is pinned and verified; the toolchain
# it installs is the current stable, which rustup verifies against the
# channel manifest.
#
# Install refuses to run over an existing rustup, so `uninstall` (rustup self
# uninstall, which removes ~/.cargo and ~/.rustup) only ever undoes what this
# arrow installed. `update` runs `rustup update` in place: a reinstall would
# stop at that same guard. Requirements are conservative estimates: Rust
# publishes none.
targets:
  _unix:
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download rustup
          url:
            linux/amd64: https://static.rust-lang.org/rustup/archive/1.29.1/x86_64-unknown-linux-gnu/rustup-init
            linux/arm64: https://static.rust-lang.org/rustup/archive/1.29.1/aarch64-unknown-linux-gnu/rustup-init
            darwin/arm64: https://static.rust-lang.org/rustup/archive/1.29.1/aarch64-apple-darwin/rustup-init
            darwin/amd64: https://static.rust-lang.org/rustup/archive/1.29.1/x86_64-apple-darwin/rustup-init
          checksum:
            linux/amd64: dda7234360b7f578ca8b0ddcb80145646fa61a67c1720a5abc7051b35c9fcb71
            linux/arm64: 15f6e4ce9f583b929c996c91562bad6d4454f3281de858b02cdfdef615fac433
            darwin/arm64: ec1b9233e7f72990ecd8e62063fa7f6c3dfc2bec8e97f88bff165f9100ac696a
            darwin/amd64: 259e2b84274434085163fe8d556510571772cda2aa6d87ca6aa664f57bc644e3
          to: ${INSTALL_PATH}/.rustup-init.download
          timeout: 5m
        - type: portable
          title: Prepare rustup
          from: ${INSTALL_PATH}/.rustup-init.download
          to: ${INSTALL_PATH}/bin
          name: rustup-init
          timeout: 1m
        - type: run
          title: Install Rust
          command: 'if [ -e "$HOME/.rustup" ] || [ -e "$HOME/.cargo/bin/rustup" ]; then echo "rustup is already installed in $HOME; update it with rustup update" >&2; exit 1; fi; ./bin/rustup-init -y --default-toolchain stable --profile default'
          timeout: 30m
      update:
        - type: run
          title: Update Rust
          command: '"$HOME/.cargo/bin/rustup" update'
          timeout: 30m
      uninstall:
        - type: run
          title: Uninstall Rust
          command: '"$HOME/.cargo/bin/rustup" self uninstall -y'
          timeout: 10m
          exit_on_failure: false

  "linux/*":
    base: _unix

  "darwin/*":
    base: _unix

  # rustup-init.exe defaults to the MSVC toolchain; with -y it installs even
  # when the Visual Studio C++ Build Tools are missing, and only warns.
  "windows/*":
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download rustup
          url:
            windows/amd64: https://static.rust-lang.org/rustup/archive/1.29.1/x86_64-pc-windows-msvc/rustup-init.exe
            windows/arm64: https://static.rust-lang.org/rustup/archive/1.29.1/aarch64-pc-windows-msvc/rustup-init.exe
          checksum:
            windows/amd64: 6f4bef66261261fcb43131be8720bab817d403a09edec7455c371974b90bdb7e
            windows/arm64: 01aa49cf9574a8bd0ae52005d7de2590e8f27181ded6748236e702c92aef826d
          to: ${INSTALL_PATH}/rustup-init.exe
          timeout: 5m
        - type: run
          title: Install Rust
          command: 'if exist "%USERPROFILE%\.rustup" (echo rustup is already installed in %USERPROFILE%; update it with rustup update 1>&2 & exit 1) else (.\rustup-init.exe -y --default-toolchain stable --profile default)'
          timeout: 30m
      update:
        - type: run
          title: Update Rust
          command: '"%USERPROFILE%\.cargo\bin\rustup.exe" update'
          timeout: 30m
      uninstall:
        - type: run
          title: Uninstall Rust
          command: '"%USERPROFILE%\.cargo\bin\rustup.exe" self uninstall -y'
          timeout: 10m
          exit_on_failure: false
```
