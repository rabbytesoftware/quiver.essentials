Git is the distributed version control system behind most software projects: it records every change to a set of files, lets many people work on branches in parallel and merges their work back together. Git for Windows brings the full Git toolset to Windows, together with Git Bash, a Unix-style shell to run it in, and graphical tools for committing and browsing history.

![Cloning a repository in Git Bash](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/git/screenshots/git-bash.png)

## Features

- **The `git` command**: the complete Git command line, available from any terminal once installed.
- **Git Bash**: a Bash environment with the usual Unix tools, for running Git and shell scripts the way you would on macOS or Linux.
- **Git GUI and gitk**: a graphical tool for staging and committing, and a history browser for branches and commits.
- **Git Credential Manager**: stores your credentials securely and signs in to GitHub, Azure Repos and other hosting services.

![Staging changes and writing a commit in Git GUI](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/git/screenshots/git-gui.png)

![Browsing history with gitk](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/git/screenshots/gitk.png)

## Installing with Quiver

| Platform | Available | Why |
|---|---|---|
| Windows (x64 and ARM64) | Yes | Git for Windows' official portable edition, unpacked into Quiver's folder. Quiver adds its `cmd` folder to your user `Path` and puts Git Bash and Git GUI in the Start Menu. |
| macOS | No | Git publishes no macOS binaries of its own. macOS offers Git with the Xcode Command Line Tools (run `xcode-select --install`). |
| Linux | No | Git publishes no Linux binaries of its own: install it with your distribution's package manager, for example `sudo apt install git`. |

The download is pinned to an official Git for Windows release and verified against the SHA-256 checksum published in its release notes.

### Good to know

- **Open a new terminal after installing.** Windows only gives the updated `Path` to programs started afterwards. Then `git --version` should answer.
- **An existing Git comes first.** Quiver appends to your user `Path`, so a Git already installed system-wide keeps answering to `git`; Git Bash and Git GUI from the Start Menu always run the copy Quiver installed.
- **Git Bash starts in Git's own folder** when opened from the Start Menu. Type `cd ~` to go to your home folder.
- **This is the portable edition.** It writes nothing to the registry, so it has no "Git Bash Here" entries in Explorer's right-click menu. Your settings (`~/.gitconfig`) live in your home folder and survive uninstalling.
- **Updates come through Quiver.** The portable edition does not update itself.

## License and trademarks

Git is free software released under the [GNU General Public License v2](https://github.com/git/git/blob/master/COPYING); Git for Windows is maintained by the [Git for Windows project](https://gitforwindows.org) under the same license. This arrow only downloads the official portable build from Git for Windows' GitHub releases. The Git logo by Jason Long is licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) and comes from [git-scm.com](https://git-scm.com/community/logos); the banner was generated from it, and the screenshots come from [gitforwindows.org](https://gitforwindows.org).

```arrow
schema: "arrow@v0"

metadata:
  name: Git
  description: The distributed version control system, with Git Bash and Git GUI
  license: GPL-2.0-only
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://gitforwindows.org
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: The Git Project
      url: https://git-scm.com
    - name: Git for Windows
      url: https://gitforwindows.org
  media:
    icon: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/git/icon.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/git/banner.svg
  tags:
    - git
    - vcs
    - cli

# Windows only: Git itself publishes source releases, and only Git for Windows
# ships official binaries. macOS gets Git from the Xcode Command Line Tools and
# Linux from distribution packages.
targets:
  # PortableGit is a 7-Zip self-extractor: -o picks the folder, -y skips its
  # dialog, and after unpacking it runs the post-install.bat it carries, which
  # the portable edition needs before Git works. Everything stays in the
  # workdir; `uninstall` removes the unpacked tree.
  #
  # The full Git-<ver>-*.tar.bz2 assets are not used: they hold symlinks to
  # /proc, which `extract` refuses as escaping the workdir.
  #
  # Requirements are conservative estimates: Git for Windows publishes none.
  "windows/*":
    requirements:
      cpu_cores: 1
      ram_gb: 1
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download Git for Windows
          url:
            windows/amd64: https://github.com/git-for-windows/git/releases/download/v2.56.0.windows.1/PortableGit-2.56.0-64-bit.7z.exe
            windows/arm64: https://github.com/git-for-windows/git/releases/download/v2.56.0.windows.1/PortableGit-2.56.0-arm64.7z.exe
          checksum:
            windows/amd64: eceb5e061aa90df2f69ddd3e90f0030e1b8037a7829934bc40e4be1caa1accc1
            windows/arm64: edd9bd32aefa5d2bd4b938c38c18ceca306a7f6b29a6951cd6a4bb16d9d28d8f
          to: ${INSTALL_PATH}/PortableGit.7z.exe
          timeout: 10m
        - type: run
          title: Unpack Git for Windows
          command: '.\PortableGit.7z.exe -o"%CD%\PortableGit" -y && del PortableGit.7z.exe'
          timeout: 10m
      uninstall:
        - type: run
          title: Remove Git for Windows
          command: 'rmdir /s /q PortableGit'
          timeout: 5m
          exit_on_failure: false
    expose:
      cli:
        - name: git
          path: ${INSTALL_PATH}/PortableGit/cmd/git.exe
      desktop:
        - name: GitBash
          path: ${INSTALL_PATH}/PortableGit/git-bash.exe
        - name: GitGUI
          path: ${INSTALL_PATH}/PortableGit/cmd/git-gui.exe
```
