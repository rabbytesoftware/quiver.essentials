WhatsApp for Mac brings your chats and calls to the desktop: message friends, family and groups with a full keyboard, share files and photos straight from your Mac, and make voice and video calls without reaching for your phone. Personal messages and calls are end-to-end encrypted, so no one outside the conversation, not even WhatsApp, can read or listen to them.

![WhatsApp group video call on desktop](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/whatsapp/screenshots/group-video-call.jpg)

## Features

- **Chats and groups**: one-to-one and group conversations, with photos, videos, documents, voice messages and reactions.
- **Voice and video calls**: one-to-one and group calls from the desktop, with screen sharing.
- **In sync with your phone**: your account and chats are the same on your phone and your Mac, and your Mac keeps working when your phone is offline.
- **Private by default**: end-to-end encryption for personal messages and calls.
- **Free**: no subscription; only your internet connection is needed.

![A WhatsApp chat with a call in progress](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/whatsapp/screenshots/chat-and-call.jpg)

## Installing with Quiver

| Platform | Available | Why |
|---|---|---|
| macOS (Apple silicon and Intel) | Yes | WhatsApp's official universal DMG, installed as `WhatsApp.app` in Applications. Requires macOS 12.1 or later. |
| Windows | No | WhatsApp distributes its Windows app only through the Microsoft Store. Install it from there. |
| Linux | No | There is no official WhatsApp client for Linux. |

### Good to know

- **You need WhatsApp on your phone first.** The desktop app is linked to an existing account: on first launch it shows a QR code that you scan from WhatsApp on your phone (Settings → Linked devices).
- **The download is not checksum-verified.** WhatsApp only offers its Mac app through a link that always points to the latest build, behind a temporary, signed download address. Quiver therefore cannot pin a version or check a published checksum: each install gets whatever WhatsApp currently serves, over HTTPS, directly from WhatsApp.
- **WhatsApp keeps itself up to date** after it is installed.
- **Already have WhatsApp?** Quiver never replaces an app it did not install. If `WhatsApp.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.

## License and trademarks

WhatsApp is proprietary software by WhatsApp LLC (Meta), free to use under its [Terms of Service](https://www.whatsapp.com/legal/terms-of-service). This arrow only downloads WhatsApp's official build from WhatsApp's own servers. The WhatsApp name and logo are trademarks of WhatsApp LLC, used as published in Meta's [WhatsApp brand resources](https://about.meta.com/brand/resources/whatsapp/whatsapp-brand/); the banner is WhatsApp's own artwork from its [download page](https://www.whatsapp.com/download), cropped to 2:1, and the screenshots come from WhatsApp's official Microsoft Store listing (the Windows app shares the Mac app's design).

```arrow
schema: "arrow@v0"

metadata:
  name: WhatsApp
  description: Private messaging and calls, on your Mac
  license: Proprietary
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://www.whatsapp.com/download
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: WhatsApp LLC
      url: https://www.whatsapp.com
  media:
    icon: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/whatsapp/icon.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/whatsapp/banner.png
  tags:
    - chat
    - messaging
    - desktop

# macOS only. WhatsApp publishes Windows exclusively through the Microsoft
# Store and has no Linux client, so neither can be installed from a download
# Quiver can verify.
targets:
  # One universal (x86_64 + arm64) DMG; requires macOS 12.1 or later.
  # Requirements are conservative estimates: WhatsApp publishes no hardware
  # minimums.
  #
  # The download is UNVERIFIED: WhatsApp serves the DMG only through this
  # endpoint, which redirects to a signed, short-lived CDN URL for whatever the
  # current version is, so no fixed URL or checksum exists. Each install gets
  # the latest build, which then updates itself.
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 1
    lifecycle:
      install:
        - type: fetch
          title: Download WhatsApp
          url: https://web.whatsapp.com/desktop/mac_native/release/?configuration=Release
          to: ${INSTALL_PATH}/.whatsapp.download
          timeout: 15m
        - type: portable
          title: Install WhatsApp
          from: ${INSTALL_PATH}/.whatsapp.download
          to: ${INSTALL_PATH}/WhatsApp
          timeout: 10m
    expose:
      desktop:
        - name: WhatsApp
          path: auto
```
