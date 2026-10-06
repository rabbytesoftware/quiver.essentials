Google Chrome is Google's web browser. It signs in with a Google account to sync bookmarks, passwords and tabs between devices, runs the extensions in the Chrome Web Store, and keeps separate profiles for work, home or anyone else who shares the computer.

![Chrome with themes, profiles and a new tab page](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/google-chrome/screenshots/themes-and-profiles.png)

## Features

- **Sync**: sign in with a Google account to carry bookmarks, history, passwords and open tabs across your computers and phone.
- **Extensions and themes**: add-ons from the Chrome Web Store, and themes that restyle the browser and its new tab page.
- **Profiles**: separate sets of bookmarks, extensions, settings and sign-ins, so work and personal browsing stay apart.
- **Password Manager**: offers to save logins and fills them in on the sites you use.
- **Safety Check and Privacy Guide**: built-in pages that review your passwords, extensions, updates and privacy settings.
- **Tab management**: tab groups, and an energy-saver mode that reduces what the browser does in the background.

![Chrome's new tab page in a dark theme](https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/google-chrome/screenshots/new-tab.png)

## Installing with Quiver

| Platform | What Quiver installs |
|---|---|
| macOS (Apple silicon and Intel) | Google's official universal DMG, as `Google Chrome.app` in Applications. Requires macOS 13 or later. |
| Windows (x64 and ARM64) | Google's official full installer for the current stable release, found through Google's update service and verified against its SHA-256, run for your user (no administrator rights). Chrome installs into your user profile and adds its own shortcuts. Requires Windows 10 or later. |

Not supported: **Linux**. Google publishes Chrome for Linux only as `.deb` and `.rpm` packages, with no AppImage or tarball that Quiver can unpack on every distribution, so this arrow does not support Linux.

Quiver installs the current stable Chrome and pins nothing, so the install always fetches the latest release and can never point at a build Google has removed. On Windows it asks Google's update service (the one Chrome updates itself from) for the current installer and the SHA-256 it reports, then verifies the download against it. On macOS it downloads Google's "current" DMG over HTTPS; Google publishes no checksum for that file, so it is **not checksum-verified**.

This is Google Chrome itself, not Chrome for Testing: that is a separate build meant for test automation, with no auto-update and a different name and profile.

### Good to know

- **On macOS and Windows, Chrome keeps itself up to date.** Quiver installs the current release at the time you install; from then on Chrome's own updater installs new versions.
- **Your profile lives outside Quiver's folder** (`~/Library/Application Support/Google/Chrome` on macOS, `%LOCALAPPDATA%\Google\Chrome\User Data` on Windows), so uninstalling keeps your bookmarks and settings. Delete it to remove everything.
- **On Windows, Chrome installs into your user profile**, not into Quiver's folder, together with Google's per-user updater. Uninstalling through Quiver runs Chrome's own uninstaller. The installer is about 500 MB; Quiver deletes it after installing.
- **The macOS download is not checksum-verified.** It comes over HTTPS from Google's servers, but it is a "current" link, so no fixed checksum can be pinned. The Windows download is verified.
- **Already have Chrome?** Quiver never replaces an app it did not install. If `Google Chrome.app` is already in your Applications folder, Quiver leaves it untouched and reports that it could not place its own copy there.
- **Using Chrome is subject to Google's terms.** Chrome is not open source and Quiver does not redistribute it: it downloads Google's files straight from Google's servers onto your machine.

## License and trademarks

Google Chrome is proprietary software by Google LLC, free to use under the [Google Chrome Terms of Service](https://www.google.com/chrome/terms/); it is built on the open-source Chromium project. This arrow only downloads Google's official builds from Google's own servers. The Google Chrome name and logo are trademarks of Google LLC; the icon is the logo published on [google.com/chrome](https://www.google.com/chrome/), the banner and screenshots are Google's official images from that page (the banner is its homepage image, cropped to 2:1).

```arrow
schema: "arrow@v0"

metadata:
  name: Google Chrome
  description: Google's web browser, with sync, extensions and profiles
  license: Proprietary
  quiver: github.com/rabbytesoftware/quiver.essentials
  url: https://www.google.com/chrome/
  maintainers:
    - name: Rabbyte Software
      url: https://github.com/rabbytesoftware
  credits:
    - name: Google LLC
      url: https://www.google.com/chrome/
  media:
    icon: https://www.google.com/chrome/static/images/chrome-logo-m100.svg
    banner: https://raw.githubusercontent.com/rabbytesoftware/quiver.essentials/master/media/google-chrome/banner.png
  tags:
    - browser
    - desktop

# Google keeps no permanent versioned download URLs for Chrome, so nothing is
# pinned: macOS uses Google's stable "current" DMG address (no checksum, Google
# publishes none for a rolling file); Windows asks Google's update service at
# install time for the current installer and its SHA-256, and verifies it.
#  - Linux is not supported: Google ships it only as .deb/.rpm.
# Requirements are conservative estimates: Google publishes OS versions but
# no hardware minimums.
targets:

  # One universal DMG (Intel and Apple silicon); requires macOS 13 or later.
  "darwin/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: fetch
          title: Download Chrome
          url: https://dl.google.com/chrome/mac/universal/stable/GGRO/googlechrome.dmg
          to: ${INSTALL_PATH}/.chrome.download
          timeout: 30m
        - type: portable
          title: Install Chrome
          from: ${INSTALL_PATH}/.chrome.download
          to: ${INSTALL_PATH}/Chrome
          timeout: 10m
    expose:
      desktop:
        - name: Chrome
          path: auto

  # Google's update service (Omaha protocol 3.1, the one Chrome's own updater
  # speaks) names the current stable full installer for this architecture, with
  # its SHA-256; the first step asks it, downloads the file over HTTPS and
  # verifies the hash, so nothing is pinned and the download is still checked.
  # (Google's tagged "standalone" installer was tried and installs nothing when
  # run silently.) The PowerShell is passed with -EncodedCommand (UTF-16LE
  # base64) to avoid cmd.exe quoting; its readable source is:
  #   $ErrorActionPreference='Stop';$ProgressPreference='SilentlyContinue'
  #   [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12
  #   $arm=($env:PROCESSOR_ARCHITECTURE -eq 'ARM64') -or ($env:PROCESSOR_ARCHITEW6432 -eq 'ARM64')
  #   if($arm){$ap='arm64-stable-statsdef_1';$arch='arm64';$oa='arm64'}else{$ap='x64-stable-statsdef_1';$arch='x64';$oa='x86_64'}
  #   $app=@{appid='{8A69D345-D564-463C-AFF1-A69D9E530F96}';ap=$ap;version='';updatecheck=@{}}
  #   $req=@{request=@{'@os'='win';'@updater'='chrome';acceptformat='download';app=@($app);arch=$arch;os=@{platform='Windows';arch=$oa;version='10.0.19045'};protocol='3.1';updater=@{name='chrome';version='1.0'}}}
  #   $body=$req|ConvertTo-Json -Depth 8 -Compress
  #   $r=Invoke-WebRequest -UseBasicParsing -Method Post -ContentType 'application/json' -Body $body -Uri 'https://update.googleapis.com/service/update2/json'
  #   $j=($r.Content -replace "^\)\]\}'",'')|ConvertFrom-Json
  #   $u=$j.response.app[0].updatecheck
  #   if($u.status -ne 'ok'){throw 'no Chrome release offered'}
  #   $base=($u.urls.url|Where-Object{$_.codebase -like 'https://*'}|Select-Object -First 1).codebase
  #   $pkg=@($u.manifest.packages.package)[0]
  #   $out=Join-Path (Get-Location).Path 'ChromeSetup.exe';(New-Object Net.WebClient).DownloadFile($base+$pkg.name,$out)
  #   $h=(Get-FileHash -Algorithm SHA256 -Path $out).Hash
  #   if($h -ne $pkg.hash_sha256){Remove-Item $out;throw 'SHA-256 mismatch'}
  # The second step runs the full installer per user (no --system-level), into
  # %LOCALAPPDATA%\Google\Chrome outside the workdir, with its own shortcuts: there
  # is no `expose`. The ~500 MB installer is deleted afterwards. `uninstall` runs
  # the setup.exe Chrome registers for the user under the "Google Chrome"
  # uninstall key (it moves with Chrome's own updates); --force-uninstall skips
  # the confirmation dialog. Requires Windows 10 or later.
  "windows/*":
    requirements:
      cpu_cores: 2
      ram_gb: 4
      disk_gb: 2
    lifecycle:
      install:
        - type: run
          title: Download the current Chrome installer
          command: 'powershell -NoProfile -ExecutionPolicy Bypass -EncodedCommand JABFAHIAcgBvAHIAQQBjAHQAaQBvAG4AUAByAGUAZgBlAHIAZQBuAGMAZQA9ACcAUwB0AG8AcAAnADsAJABQAHIAbwBnAHIAZQBzAHMAUAByAGUAZgBlAHIAZQBuAGMAZQA9ACcAUwBpAGwAZQBuAHQAbAB5AEMAbwBuAHQAaQBuAHUAZQAnAAoAWwBOAGUAdAAuAFMAZQByAHYAaQBjAGUAUABvAGkAbgB0AE0AYQBuAGEAZwBlAHIAXQA6ADoAUwBlAGMAdQByAGkAdAB5AFAAcgBvAHQAbwBjAG8AbAA9AFsATgBlAHQALgBTAGUAYwB1AHIAaQB0AHkAUAByAG8AdABvAGMAbwBsAFQAeQBwAGUAXQA6ADoAVABsAHMAMQAyAAoAJABhAHIAbQA9ACgAJABlAG4AdgA6AFAAUgBPAEMARQBTAFMATwBSAF8AQQBSAEMASABJAFQARQBDAFQAVQBSAEUAIAAtAGUAcQAgACcAQQBSAE0ANgA0ACcAKQAgAC0AbwByACAAKAAkAGUAbgB2ADoAUABSAE8AQwBFAFMAUwBPAFIAXwBBAFIAQwBIAEkAVABFAFcANgA0ADMAMgAgAC0AZQBxACAAJwBBAFIATQA2ADQAJwApAAoAaQBmACgAJABhAHIAbQApAHsAJABhAHAAPQAnAGEAcgBtADYANAAtAHMAdABhAGIAbABlAC0AcwB0AGEAdABzAGQAZQBmAF8AMQAnADsAJABhAHIAYwBoAD0AJwBhAHIAbQA2ADQAJwA7ACQAbwBhAD0AJwBhAHIAbQA2ADQAJwB9AGUAbABzAGUAewAkAGEAcAA9ACcAeAA2ADQALQBzAHQAYQBiAGwAZQAtAHMAdABhAHQAcwBkAGUAZgBfADEAJwA7ACQAYQByAGMAaAA9ACcAeAA2ADQAJwA7ACQAbwBhAD0AJwB4ADgANgBfADYANAAnAH0ACgAkAGEAcABwAD0AQAB7AGEAcABwAGkAZAA9ACcAewA4AEEANgA5AEQAMwA0ADUALQBEADUANgA0AC0ANAA2ADMAQwAtAEEARgBGADEALQBBADYAOQBEADkARQA1ADMAMABGADkANgB9ACcAOwBhAHAAPQAkAGEAcAA7AHYAZQByAHMAaQBvAG4APQAnACcAOwB1AHAAZABhAHQAZQBjAGgAZQBjAGsAPQBAAHsAfQB9AAoAJAByAGUAcQA9AEAAewByAGUAcQB1AGUAcwB0AD0AQAB7ACcAQABvAHMAJwA9ACcAdwBpAG4AJwA7ACcAQAB1AHAAZABhAHQAZQByACcAPQAnAGMAaAByAG8AbQBlACcAOwBhAGMAYwBlAHAAdABmAG8AcgBtAGEAdAA9ACcAZABvAHcAbgBsAG8AYQBkACcAOwBhAHAAcAA9AEAAKAAkAGEAcABwACkAOwBhAHIAYwBoAD0AJABhAHIAYwBoADsAbwBzAD0AQAB7AHAAbABhAHQAZgBvAHIAbQA9ACcAVwBpAG4AZABvAHcAcwAnADsAYQByAGMAaAA9ACQAbwBhADsAdgBlAHIAcwBpAG8AbgA9ACcAMQAwAC4AMAAuADEAOQAwADQANQAnAH0AOwBwAHIAbwB0AG8AYwBvAGwAPQAnADMALgAxACcAOwB1AHAAZABhAHQAZQByAD0AQAB7AG4AYQBtAGUAPQAnAGMAaAByAG8AbQBlACcAOwB2AGUAcgBzAGkAbwBuAD0AJwAxAC4AMAAnAH0AfQB9AAoAJABiAG8AZAB5AD0AJAByAGUAcQB8AEMAbwBuAHYAZQByAHQAVABvAC0ASgBzAG8AbgAgAC0ARABlAHAAdABoACAAOAAgAC0AQwBvAG0AcAByAGUAcwBzAAoAJAByAD0ASQBuAHYAbwBrAGUALQBXAGUAYgBSAGUAcQB1AGUAcwB0ACAALQBVAHMAZQBCAGEAcwBpAGMAUABhAHIAcwBpAG4AZwAgAC0ATQBlAHQAaABvAGQAIABQAG8AcwB0ACAALQBDAG8AbgB0AGUAbgB0AFQAeQBwAGUAIAAnAGEAcABwAGwAaQBjAGEAdABpAG8AbgAvAGoAcwBvAG4AJwAgAC0AQgBvAGQAeQAgACQAYgBvAGQAeQAgAC0AVQByAGkAIAAnAGgAdAB0AHAAcwA6AC8ALwB1AHAAZABhAHQAZQAuAGcAbwBvAGcAbABlAGEAcABpAHMALgBjAG8AbQAvAHMAZQByAHYAaQBjAGUALwB1AHAAZABhAHQAZQAyAC8AagBzAG8AbgAnAAoAJABqAD0AKAAkAHIALgBDAG8AbgB0AGUAbgB0ACAALQByAGUAcABsAGEAYwBlACAAIgBeAFwAKQBcAF0AXAB9ACcAIgAsACcAJwApAHwAQwBvAG4AdgBlAHIAdABGAHIAbwBtAC0ASgBzAG8AbgAKACQAdQA9ACQAagAuAHIAZQBzAHAAbwBuAHMAZQAuAGEAcABwAFsAMABdAC4AdQBwAGQAYQB0AGUAYwBoAGUAYwBrAAoAaQBmACgAJAB1AC4AcwB0AGEAdAB1AHMAIAAtAG4AZQAgACcAbwBrACcAKQB7AHQAaAByAG8AdwAgACcAbgBvACAAQwBoAHIAbwBtAGUAIAByAGUAbABlAGEAcwBlACAAbwBmAGYAZQByAGUAZAAnAH0ACgAkAGIAYQBzAGUAPQAoACQAdQAuAHUAcgBsAHMALgB1AHIAbAB8AFcAaABlAHIAZQAtAE8AYgBqAGUAYwB0AHsAJABfAC4AYwBvAGQAZQBiAGEAcwBlACAALQBsAGkAawBlACAAJwBoAHQAdABwAHMAOgAvAC8AKgAnAH0AfABTAGUAbABlAGMAdAAtAE8AYgBqAGUAYwB0ACAALQBGAGkAcgBzAHQAIAAxACkALgBjAG8AZABlAGIAYQBzAGUACgAkAHAAawBnAD0AQAAoACQAdQAuAG0AYQBuAGkAZgBlAHMAdAAuAHAAYQBjAGsAYQBnAGUAcwAuAHAAYQBjAGsAYQBnAGUAKQBbADAAXQAKACQAbwB1AHQAPQBKAG8AaQBuAC0AUABhAHQAaAAgACgARwBlAHQALQBMAG8AYwBhAHQAaQBvAG4AKQAuAFAAYQB0AGgAIAAnAEMAaAByAG8AbQBlAFMAZQB0AHUAcAAuAGUAeABlACcAOwAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQARgBpAGwAZQAoACQAYgBhAHMAZQArACQAcABrAGcALgBuAGEAbQBlACwAJABvAHUAdAApAAoAJABoAD0AKABHAGUAdAAtAEYAaQBsAGUASABhAHMAaAAgAC0AQQBsAGcAbwByAGkAdABoAG0AIABTAEgAQQAyADUANgAgAC0AUABhAHQAaAAgACQAbwB1AHQAKQAuAEgAYQBzAGgACgBpAGYAKAAkAGgAIAAtAG4AZQAgACQAcABrAGcALgBoAGEAcwBoAF8AcwBoAGEAMgA1ADYAKQB7AFIAZQBtAG8AdgBlAC0ASQB0AGUAbQAgACQAbwB1AHQAOwB0AGgAcgBvAHcAIAAnAFMASABBAC0AMgA1ADYAIABtAGkAcwBtAGEAdABjAGgAJwB9AAoA'
          timeout: 40m
        - type: run
          title: Install Chrome
          command: '.\ChromeSetup.exe --do-not-launch-chrome --channel=stable >nul 2>&1 <nul && del /q ChromeSetup.exe'
          timeout: 15m
      uninstall:
        - type: run
          title: Uninstall Chrome
          command: 'for /f "tokens=2,*" %a in (''reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome" /v UninstallString ^| findstr REG_SZ'') do %b --uninstall --channel=stable --force-uninstall'
          timeout: 10m
          exit_on_failure: false
```
