One to four sentences on what My App is, who it is for and what sets it apart. This paragraph opens the Overview page in Quiver Desktop, right under the hero that already shows the name, icon, banner and description, so there is no title here.

![My App's main window](https://raw.githubusercontent.com/OWNER/COLLECTION/master/media/my-app/screenshots/main-window.jpg)

## Features

- **First feature**: one line on what it does for the user.
- **Second feature**: one line.
- **Third feature**: one line.

![Another view of My App](https://raw.githubusercontent.com/OWNER/COLLECTION/master/media/my-app/screenshots/another-view.jpg)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | The official universal DMG, as `My App.app` in Applications. |
| Linux (x86_64) | The official AppImage and a desktop menu entry. No ARM build is published. |
| Windows | Not available: say why (no official build, Store-only, ...). |

### Good to know

- What the user needs first (an account, a companion device, a licence key).
- Where the app keeps its data, and whether uninstalling removes it.
- Whether the app updates itself, and anything that is not checksum-verified.
- Published hardware minimums, if any.

## License and trademarks

My App is released under the [MIT License](https://example.com/LICENSE) by Its Author. The name and logo belong to their owner; the icon comes from the project's own repository and the screenshots from its website.

<!--
Template notes (delete this comment):
- File: <path>.md in the collection repository, e.g. apps/my-app.md; the
  collection entry keeps `path: apps/my-app` (Quiver tries .md before .yaml).
- Everything outside the ```arrow fence below is the readme. Keep the fence
  last and exactly ```arrow.
- Screenshots: absolute https URLs only; host them under media/<auid>/screenshots/.
- Guidance: references/readme.md. Check with: quiver_arrow.py readme <file>.
-->

```arrow
schema: "arrow@v0"

metadata:
  name: My App
  description: One-line description shown in the page hero
  license: MIT
  quiver: github.com/OWNER/COLLECTION
  url: https://example.com
  maintainers:
    - name: OWNER
      url: https://github.com/OWNER
  credits:
    - name: Its Author
      url: https://example.com
  media:
    icon: https://raw.githubusercontent.com/OWNER/COLLECTION/master/media/my-app/icon.svg
    banner: https://raw.githubusercontent.com/OWNER/COLLECTION/master/media/my-app/banner.svg
  tags:
    - desktop

targets:
  linux/amd64:
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download My App
          url: https://example.com/releases/1.0.0/my-app-x86_64.AppImage
          checksum: 0000000000000000000000000000000000000000000000000000000000000000
          to: ${INSTALL_PATH}/.my-app.download
          timeout: 10m
        - type: portable
          title: Install My App
          from: ${INSTALL_PATH}/.my-app.download
          to: ${INSTALL_PATH}/MyApp
          timeout: 10m
    expose:
      desktop:
        - name: MyApp
          path: auto

  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 2
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download My App
          url: https://example.com/releases/1.0.0/MyApp.dmg
          checksum: 0000000000000000000000000000000000000000000000000000000000000000
          to: ${INSTALL_PATH}/.my-app.download
          timeout: 10m
        - type: portable
          title: Install My App
          from: ${INSTALL_PATH}/.my-app.download
          to: ${INSTALL_PATH}/MyApp
          timeout: 10m
    expose:
      desktop:
        - name: MyApp
          path: auto
```
