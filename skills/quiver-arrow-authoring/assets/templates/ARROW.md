# My Tool

One or two paragraphs for humans: what the software is and what installing it
through Quiver gives you. Everything outside the fenced block below is served
as the arrow's readme (`GET /v0/arrow/{ns}/readme`) and shown on its details
page. Only the FIRST block fenced as ```arrow is the manifest.

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

Notes for the author (delete this section):

- `${REF}` in the URL is the git ref Quiver read this file at. It only works
  when the arrow ships in the same repository as the releases it downloads,
  and when release tags are named exactly like the ref.
- Add the per-platform `checksum` map (see assets/examples/archive-cli.yaml).
  With `${REF}` URLs the digests change every release, so they must be
  updated in the same commit that gets tagged (ideally by the release
  pipeline); this template leaves them out only because it has no real
  release to take them from.
