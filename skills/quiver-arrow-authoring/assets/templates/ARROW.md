One to four sentences on what My Tool is, who it is for and what sets it apart. This paragraph opens the Overview page in Quiver Desktop, right under the hero that already shows the name, icon, banner and description, so there is no title here.

![My Tool in a terminal](https://raw.githubusercontent.com/OWNER/mytool/main/docs/screenshot.png)

## Features

- **First feature**: one line on what it does for the user.
- **Second feature**: one line.

## Usage

```sh
mytool --help
```

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| Linux, macOS, Windows (x86_64 and ARM64) | The release archive for your platform; `mytool` is added to your PATH (run `quiver path setup` once). |

## License

My Tool is released under the [MIT License](https://github.com/OWNER/mytool/blob/main/LICENSE).

<!--
Template notes (delete this comment):
- Put this file at the root of the repository the arrow installs from, as
  ARROW.md. Everything outside the ```arrow fence below is the readme shown
  on the arrow's Overview page; the fence holds the manifest. See
  references/readme.md.
- The git ref Quiver reads this file at is the arrow's version: tag
  releases, never write a `version:` field.
- ${REF} in the URLs is that ref. It only works when the arrow ships in the
  same repository as the releases it downloads, with tags named like the
  release.
- Add the per-platform `checksum` map (see assets/examples/archive-cli.yaml):
  with ${REF} URLs the digests change every release, so update them in the
  commit that gets tagged (ideally from the release pipeline).
-->

```arrow is the manifest.

Put this file at the root of the repository the arrow is installed from, as
`ARROW.md` (or put the bare YAML in `arrow.yaml`). The git ref the manifest is
read at is the arrow's version: tag releases, never write a `version:` field.

```arrow
schema: "arrow@v0"

metadata:
  name: My Tool
  description: One-line description
  license: MIT
  url: https://github.com/OWNER/mytool
  maintainers:
    - name: OWNER
      url: https://github.com/OWNER
  tags:
    - cli

targets:
  "*":
    requirements:
      cpu_cores: 1
      ram_gb: 1
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download mytool
          url:
            linux/amd64: https://github.com/OWNER/mytool/releases/download/${REF}/mytool-linux-amd64.tar.gz
            linux/arm64: https://github.com/OWNER/mytool/releases/download/${REF}/mytool-linux-arm64.tar.gz
            darwin/amd64: https://github.com/OWNER/mytool/releases/download/${REF}/mytool-darwin-amd64.tar.gz
            darwin/arm64: https://github.com/OWNER/mytool/releases/download/${REF}/mytool-darwin-arm64.tar.gz
            windows/amd64: https://github.com/OWNER/mytool/releases/download/${REF}/mytool-windows-amd64.zip
            windows/arm64: https://github.com/OWNER/mytool/releases/download/${REF}/mytool-windows-arm64.zip
          to: ${INSTALL_PATH}/.mytool.download
          timeout: 5m
        - type: extract
          title: Unpack mytool
          from: ${INSTALL_PATH}/.mytool.download
          to: ${INSTALL_PATH}/bin
          timeout: 2m
    expose:
      cli:
        - name: mytool
          path: auto
```
