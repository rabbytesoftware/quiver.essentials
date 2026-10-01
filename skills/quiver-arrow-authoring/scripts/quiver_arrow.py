#!/usr/bin/env python3
"""Helpers for authoring Quiver arrows: validate, inspect releases, test-install.

Standard library only (Python 3.9+). Talks to a quiver.core daemon over its
local Unix socket, or over HTTP when QUIVER_API is set.

    python3 quiver_arrow.py validate arrow.yaml
    python3 quiver_arrow.py validate --collection collection.yaml
    python3 quiver_arrow.py assets owner/repo [TAG]
    python3 quiver_arrow.py checksum URL
    python3 quiver_arrow.py media URL_OR_FILE [...]
    python3 quiver_arrow.py readme ARROW.md [--online]
    python3 quiver_arrow.py banner --icon URL_OR_FILE --name NAME --background '#RRGGBB' --out media/<auid>/banner.svg
    python3 quiver_arrow.py bundle > quiver-arrow-authoring.md
    python3 quiver_arrow.py sandbox up
    python3 quiver_arrow.py sandbox seed github.com/owner/repo@v1.2.3 arrow.yaml
    python3 quiver_arrow.py sandbox install github.com/owner/repo@v1.2.3 [KEY=VALUE ...]
    python3 quiver_arrow.py sandbox status github.com/owner/repo@v1.2.3
    python3 quiver_arrow.py sandbox uninstall github.com/owner/repo@v1.2.3
    python3 quiver_arrow.py sandbox remove github.com/owner/repo@v1.2.3
    python3 quiver_arrow.py sandbox down

Exit codes: 0 success, 1 the manifest or the run failed, 2 usage or
environment error (daemon unreachable, network error, missing binary).

Where it connects:
  QUIVER_API     http(s) base URL of a daemon (e.g. http://127.0.0.1:40257)
  QUIVER_TOKEN   device token sent as a bearer token with QUIVER_API
                 (TCP daemons require one; the `quiver` CLI keeps its own in
                 ~/.quiver/cli.yaml)
  QUIVER_SOCKET  path of a daemon's Unix socket
  (neither)      ~/.quiver/quiver.sock, the default local daemon (macOS/Linux;
                 local Windows daemons use a named pipe, which is unsupported)
`sandbox` subcommands always use their own isolated daemon, never these.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import http.client
import json
import os
import re
import shutil
import signal
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Callable, cast

VALIDATION_NAMESPACE = "example.com/validation/arrow@v0"
COLLECTION_NAMESPACE = "example.com/validation/collection@v0"
GITHUB_API = "https://api.github.com"
POLL_SECONDS = 1.0
INSTALL_TIMEOUT_SECONDS = 1800
SANDBOX_START_SECONDS = 30
EXECUTE_SETTLE_SECONDS = 3
ACTIVE_STATES = {"installing", "updating", "uninstalling", "stopping", "draining"}

JSONObject = dict[str, object]


class ToolError(Exception):
    """An environment or usage problem: exit code 2."""


# --- JSON narrowing ------------------------------------------------------------
# The daemon and GitHub answer with JSON whose shape Python cannot know
# statically. Everything read from it goes through these, so a field that is
# missing or of an unexpected type reads as empty instead of raising.


def as_object(value: object) -> JSONObject:
    return cast(JSONObject, value) if isinstance(value, dict) else {}


def as_list(value: object) -> list[object]:
    return cast(list[object], value) if isinstance(value, list) else []


def as_str(value: object) -> str:
    return value if isinstance(value, str) else ""


def error_text(payload: JSONObject) -> str:
    return as_str(payload.get("error")) or json.dumps(payload)


# --- transport -------------------------------------------------------------------


class Daemon:
    """One quiver.core daemon, reached over a Unix socket or HTTP."""

    def __init__(self, socket_path: str = "", base_url: str = "", token: str = "") -> None:
        self.socket_path: str = socket_path
        self.base_url: str = base_url.rstrip("/")
        self.token: str = token

    @classmethod
    def from_env(cls) -> Daemon:
        api = os.environ.get("QUIVER_API", "")
        if api:
            return cls(base_url=api, token=os.environ.get("QUIVER_TOKEN", ""))
        default = os.path.join(os.path.expanduser("~"), ".quiver", "quiver.sock")
        return cls(socket_path=os.environ.get("QUIVER_SOCKET") or default)

    def describe(self) -> str:
        return self.base_url or "unix://" + self.socket_path

    def _connection(self, timeout: float) -> tuple[http.client.HTTPConnection, str]:
        if self.base_url:
            parsed = urllib.parse.urlsplit(self.base_url)
            if parsed.scheme == "https":
                return http.client.HTTPSConnection(parsed.netloc, timeout=timeout), parsed.path
            return http.client.HTTPConnection(parsed.netloc, timeout=timeout), parsed.path
        if os.name == "nt":
            # The Windows daemon listens on a named pipe, which this helper
            # does not speak; a TCP daemon is the supported route there.
            raise ToolError("local Windows daemons use a named pipe; set QUIVER_API (and QUIVER_TOKEN) to a TCP daemon")
        if not os.path.exists(self.socket_path):
            raise ToolError("no daemon socket at %s" % self.socket_path)
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock.connect(self.socket_path)
        except OSError:
            sock.close()
            raise
        # http.client only dials when `sock` is unset, so a pre-connected Unix
        # socket makes a plain HTTPConnection speak HTTP over it.
        conn = http.client.HTTPConnection("localhost", timeout=timeout)
        conn.sock = sock
        return conn, ""

    def request(
        self,
        method: str,
        path: str,
        body: bytes | None = None,
        content_type: str = "",
        timeout: float = 60,
    ) -> tuple[int, JSONObject]:
        headers = {"Content-Type": content_type} if content_type else {}
        if self.token:
            headers["Authorization"] = "Bearer " + self.token
        try:
            conn, prefix = self._connection(timeout)
            conn.request(method, prefix + path, body=body, headers=headers)
            resp = conn.getresponse()
            raw = resp.read()
            status = resp.status
            conn.close()
        except (OSError, http.client.HTTPException) as err:
            raise ToolError("cannot reach the quiver daemon at %s: %s" % (self.describe(), err)) from err
        if not raw:
            return status, {}
        try:
            parsed = cast(object, json.loads(raw.decode("utf-8")))
        except ValueError:
            return status, {"raw": raw.decode("utf-8", "replace")}
        return status, as_object(parsed)

    def healthy(self) -> bool:
        try:
            status, _ = self.request("GET", "/v0/health", timeout=3)
        except ToolError:
            return False
        return status == 200


def encode_ns(namespace: str) -> str:
    return urllib.parse.quote(namespace, safe="")


def print_json(data: object) -> None:
    print(json.dumps(data, indent=2))


# --- arguments -------------------------------------------------------------------


class Args(argparse.Namespace):
    """Typed view of every subcommand's arguments; argparse fills in the ones it defines."""

    def __init__(self) -> None:
        super().__init__()
        self.func: Callable[[Args], int] = no_command
        self.files: list[str] = []
        self.collection: bool = False
        self.namespace: str = ""
        self.json: bool = False
        self.repo: str = ""
        self.tag: str = ""
        self.url: str = ""
        self.file: str = ""
        self.method: str = ""
        self.vars: list[str] = []
        self.icon: str = ""
        self.name: str = ""
        self.background: str = ""
        self.text_color: str = ""
        self.out: str = ""
        self.online: bool = False


def no_command(_args: Args) -> int:
    raise ToolError("no command given (see --help)")


# --- validate ----------------------------------------------------------------------


def validate_bytes(daemon: Daemon, data: bytes, collection: bool, namespace: str) -> JSONObject:
    kind = "collection" if collection else "arrow"
    status, payload = daemon.request(
        "POST",
        "/v0/%s/%s/manifest/validate" % (kind, encode_ns(namespace)),
        body=data,
        content_type="application/x-yaml",
    )
    if status not in (200, 422) or "data" not in payload:
        raise ToolError("unexpected daemon response (HTTP %d): %s" % (status, json.dumps(payload)))
    return as_object(payload["data"])


def report_validation(path: str, result: JSONObject) -> int:
    if result.get("valid") is True:
        print("VALID: %s" % path)
        supported = [as_str(p) for p in as_list(result.get("supported_platforms"))]
        unsupported = [as_str(p) for p in as_list(result.get("unsupported_platforms"))]
        if supported or unsupported:
            print("  supported:   %s" % (", ".join(supported) or "(none)"))
            print("  unsupported: %s" % (", ".join(unsupported) or "(none)"))
        return 0
    print("INVALID: %s" % path)
    for item in as_list(result.get("errors")):
        err = as_object(item)
        field = as_str(err.get("field")) or "(manifest)"
        print("  [%s] %s: %s" % (as_str(err.get("rule")) or "?", field, as_str(err.get("message"))))
    print("\nValidation runs in phases (schema/precompile -> target selection -> compiled rules):")
    print("later-phase errors only appear once earlier ones are fixed. Fix these and run again.")
    return 1


def cmd_validate(args: Args) -> int:
    daemon = Daemon.from_env()
    namespace = args.namespace or (COLLECTION_NAMESPACE if args.collection else VALIDATION_NAMESPACE)
    worst = 0
    for path in args.files:
        with open(path, "rb") as fh:
            data = fh.read()
        result = validate_bytes(daemon, data, args.collection, namespace)
        if args.json:
            print_json(result)
            code = 0 if result.get("valid") is True else 1
        else:
            code = report_validation(path, result)
        worst = max(worst, code)
    return worst


# --- release assets ------------------------------------------------------------------


def github_json(url: str) -> JSONObject:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "quiver-arrow-authoring"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, headers=headers)
    try:
        with cast(http.client.HTTPResponse, urllib.request.urlopen(req, timeout=30)) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as err:
        hint = " (set GITHUB_TOKEN to raise the rate limit)" if err.code in (403, 429) else ""
        raise ToolError("GitHub API %s -> HTTP %d%s" % (url, err.code, hint)) from err
    except urllib.error.URLError as err:
        raise ToolError("GitHub API %s: %s" % (url, err.reason)) from err
    parsed = cast(object, json.loads(raw.decode("utf-8")))
    return as_object(parsed)


def cmd_assets(args: Args) -> int:
    repo = args.repo.strip("/")
    if args.tag:
        url = "%s/repos/%s/releases/tags/%s" % (GITHUB_API, repo, urllib.parse.quote(args.tag, safe=""))
    else:
        url = "%s/repos/%s/releases/latest" % (GITHUB_API, repo)
    release = github_json(url)
    assets: list[JSONObject] = []
    for item in as_list(release.get("assets")):
        asset = as_object(item)
        digest = as_str(asset.get("digest"))
        sha = digest.split(":", 1)[1] if digest.lower().startswith("sha256:") else ""
        assets.append(
            {
                "name": as_str(asset.get("name")),
                "sha256": sha,
                "size": asset.get("size"),
                "url": as_str(asset.get("browser_download_url")),
            }
        )
    out: JSONObject = {
        "repo": repo,
        "tag": release.get("tag_name"),
        "prerelease": release.get("prerelease"),
        "published_at": release.get("published_at"),
        "assets": assets,
    }
    if args.json:
        print_json(out)
        return 0
    print("%s  tag=%s  prerelease=%s" % (repo, out["tag"], out["prerelease"]))
    for a in assets:
        sha = as_str(a["sha256"]) or "(none published -- use `checksum`)"
        print("%s\n  url:    %s\n  sha256: %s" % (a["name"], a["url"], sha))
    return 0


def cmd_checksum(args: Args) -> int:
    digest = hashlib.sha256()
    req = urllib.request.Request(args.url, headers={"User-Agent": "quiver-arrow-authoring"})
    try:
        with cast(http.client.HTTPResponse, urllib.request.urlopen(req, timeout=120)) as resp:
            while True:
                chunk = resp.read(1 << 20)
                if not chunk:
                    break
                digest.update(chunk)
    except (urllib.error.URLError, OSError) as err:
        raise ToolError("download %s: %s" % (args.url, err)) from err
    print(digest.hexdigest())
    return 0


# --- media -------------------------------------------------------------------------------
# Quiver Desktop draws `media.banner` in a 2:1 box (the details hero contains
# it; search cards and collection heroes crop it with `cover`) and
# `media.icon` in small square avatars. SVG is preferred for both: it stays
# sharp at every size and any agent can write it. Raster images must be large
# enough to stay crisp on high-density screens.

MEDIA_MAX_BYTES = 10 * 1024 * 1024
ICON_GOOD_PX = 512
ICON_MIN_PX = 256
ICON_SQUARE_TOLERANCE = 0.02
BANNER_GOOD = (1200, 600)
BANNER_MIN = (800, 400)
BANNER_RATIO_TOLERANCE = 0.02
BANNER_MIN_RATIO = 1.5
BANNER_SIZE = (1200, 600)
EMBED_MAX_BYTES = 1024 * 1024

SVG_DIM = re.compile(r'\b(width|height)\s*=\s*"([0-9.]+)(?:px)?"')
SVG_VIEWBOX = re.compile(r'viewBox\s*=\s*"\s*[-0-9.]+[\s,]+[-0-9.]+[\s,]+([0-9.]+)[\s,]+([0-9.]+)\s*"')


class ImageInfo:
    """Format and pixel size of an image; size 0x0 when it could not be read."""

    def __init__(self, fmt: str, width: int = 0, height: int = 0) -> None:
        self.fmt: str = fmt
        self.width: int = width
        self.height: int = height

    @property
    def known(self) -> bool:
        return self.width > 0 and self.height > 0


def read_media(source: str) -> bytes:
    if source.startswith(("http://", "https://")):
        req = urllib.request.Request(source, headers={"User-Agent": "quiver-arrow-authoring"})
        try:
            with cast(http.client.HTTPResponse, urllib.request.urlopen(req, timeout=60)) as resp:
                data = resp.read(MEDIA_MAX_BYTES + 1)
        except (urllib.error.URLError, OSError) as err:
            raise ToolError("download %s: %s" % (source, err)) from err
    else:
        with open(source, "rb") as fh:
            data = fh.read(MEDIA_MAX_BYTES + 1)
    if len(data) > MEDIA_MAX_BYTES:
        raise ToolError("%s is larger than %d MiB" % (source, MEDIA_MAX_BYTES // (1024 * 1024)))
    return data


def sniff_svg(data: bytes) -> ImageInfo:
    text = data.decode("utf-8", "replace")
    head = text[: text.find(">", text.find("<svg")) + 1] if "<svg" in text else text
    dims = {m.group(1): float(m.group(2)) for m in SVG_DIM.finditer(head)}
    if dims.get("width", 0) > 0 and dims.get("height", 0) > 0:
        return ImageInfo("svg", int(dims["width"]), int(dims["height"]))
    match = SVG_VIEWBOX.search(head)
    if match:
        return ImageInfo("svg", int(float(match.group(1))), int(float(match.group(2))))
    return ImageInfo("svg")


def sniff_jpeg(data: bytes) -> ImageInfo:
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            height, width = struct.unpack(">HH", data[i + 5 : i + 9])
            return ImageInfo("jpeg", width, height)
        length = int.from_bytes(data[i + 2 : i + 4], "big")
        i += 2 + length
    return ImageInfo("jpeg")


def sniff_webp(data: bytes) -> ImageInfo:
    chunk = data[12:16]
    if chunk == b"VP8X" and len(data) >= 30:
        return ImageInfo("webp", 1 + int.from_bytes(data[24:27], "little"), 1 + int.from_bytes(data[27:30], "little"))
    if chunk == b"VP8 " and len(data) >= 30:
        width, height = struct.unpack("<HH", data[26:30])
        return ImageInfo("webp", width & 0x3FFF, height & 0x3FFF)
    if chunk == b"VP8L" and len(data) >= 25:
        bits = int.from_bytes(data[21:25], "little")
        return ImageInfo("webp", (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1)
    return ImageInfo("webp")


def sniff_image(data: bytes) -> ImageInfo:
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        width, height = struct.unpack(">II", data[16:24])
        return ImageInfo("png", width, height)
    if data.startswith(b"\xff\xd8"):
        return sniff_jpeg(data)
    if data[:6] in (b"GIF87a", b"GIF89a") and len(data) >= 10:
        width, height = struct.unpack("<HH", data[6:10])
        return ImageInfo("gif", width, height)
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return sniff_webp(data)
    if b"<svg" in data[:4096]:
        return sniff_svg(data)
    return ImageInfo("unknown")


def icon_verdict(info: ImageInfo) -> tuple[str, str]:
    if info.fmt == "unknown":
        return "reject", "not an image format a webview displays"
    if not info.known:
        return "check", "size unknown: give the SVG a square viewBox or width/height"
    if abs(info.width - info.height) > ICON_SQUARE_TOLERANCE * max(info.width, info.height):
        return "reject", "not square (%dx%d); the avatar crops it" % (info.width, info.height)
    if info.fmt == "svg":
        return "good", "square SVG"
    if min(info.width, info.height) >= ICON_GOOD_PX:
        return "good", "square %s, %dpx" % (info.fmt, min(info.width, info.height))
    if min(info.width, info.height) >= ICON_MIN_PX:
        return "ok", "square %s, %dpx; look for an SVG or a %dpx+ version" % (info.fmt, info.width, ICON_GOOD_PX)
    return "reject", "%dpx is too small (minimum %dpx; prefer SVG)" % (info.width, ICON_MIN_PX)


def banner_verdict(info: ImageInfo) -> tuple[str, str]:
    if info.fmt == "unknown":
        return "reject", "not an image format a webview displays"
    if not info.known:
        return "check", "size unknown: give the SVG a 2:1 viewBox or width/height"
    ratio = info.width / info.height
    if ratio < BANNER_MIN_RATIO:
        return "reject", "%.2f:1 is not banner-shaped (banners are 2:1); generate one with `banner`" % ratio
    exact = abs(ratio - 2) <= 2 * BANNER_RATIO_TOLERANCE
    shape = "2:1" if exact else "%.2f:1, will be cropped or letterboxed in the 2:1 frame" % ratio
    if info.fmt == "svg":
        return ("good" if exact else "ok"), "SVG, " + shape
    if info.width >= BANNER_GOOD[0] and info.height >= BANNER_GOOD[1] // (1 if exact else 2):
        return ("good" if exact else "ok"), "%s %dx%d, %s" % (info.fmt, info.width, info.height, shape)
    if info.width >= BANNER_MIN[0] and info.height >= BANNER_MIN[1] // (1 if exact else 2):
        return "ok", "%s %dx%d is small; prefer SVG or %dx%d+ (%s)" % (
            info.fmt, info.width, info.height, BANNER_GOOD[0], BANNER_GOOD[1], shape)
    return "reject", "%dx%d is too small (minimum %dx%d; prefer SVG)" % (info.width, info.height, BANNER_MIN[0], BANNER_MIN[1])


def cmd_media(args: Args) -> int:
    worst = 0
    for source in args.files:
        info = sniff_image(read_media(source))
        size = "%dx%d" % (info.width, info.height) if info.known else "size unknown"
        print("%s\n  format: %s, %s" % (source, info.fmt, size))
        for role, verdict in (("icon", icon_verdict(info)), ("banner", banner_verdict(info))):
            print("  as %-6s %-6s %s" % (role + ":", verdict[0], verdict[1]))
        if icon_verdict(info)[0] == "reject" and banner_verdict(info)[0] == "reject":
            worst = 1
    return worst


def contrast_color(background: str) -> str:
    rgb = [int(background[i : i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    luminance = 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
    return "#111111" if luminance > 0.4 else "#FFFFFF"


def cmd_banner(args: Args) -> int:
    background = args.background.upper()
    if not re.fullmatch(r"#[0-9A-F]{6}", background):
        raise ToolError("--background must be a #RRGGBB colour, e.g. #1E3A8A")
    data = read_media(args.icon)
    info = sniff_image(data)
    verdict, why = icon_verdict(info)
    if verdict == "reject":
        raise ToolError("icon %s cannot be used: %s" % (args.icon, why))
    if len(data) > EMBED_MAX_BYTES:
        raise ToolError("icon is %d KiB; embed a file under %d KiB (an SVG, or a smaller PNG)" % (len(data) // 1024, EMBED_MAX_BYTES // 1024))
    mime = {"svg": "image/svg+xml", "png": "image/png", "jpeg": "image/jpeg", "gif": "image/gif", "webp": "image/webp"}[info.fmt]
    uri = "data:%s;base64,%s" % (mime, base64.b64encode(data).decode("ascii"))
    width, height = BANNER_SIZE
    icon_px, gap, margin = 300, 72, 90
    text_room = width - 2 * margin - icon_px - gap
    name = args.name.strip()
    font_px = max(40, min(112, int(text_room / max(1, len(name)) / 0.56)))
    # Centre icon + name as one group; the text width is an estimate (no font
    # metrics without a renderer), close enough for a bold sans-serif.
    group = icon_px + gap + min(text_room, int(len(name) * font_px * 0.56))
    icon_x = max(margin, (width - group) // 2)
    text_x = icon_x + icon_px + gap
    color = args.text_color.upper() or contrast_color(background)
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">\n'
        '  <rect width="%d" height="%d" fill="%s"/>\n'
        '  <image x="%d" y="%d" width="%d" height="%d" preserveAspectRatio="xMidYMid meet" href="%s"/>\n'
        '  <text x="%d" y="%d" fill="%s" font-family="system-ui, -apple-system, \'Segoe UI\', Roboto, sans-serif" '
        'font-size="%d" font-weight="700" dominant-baseline="middle">%s</text>\n'
        "</svg>\n"
    ) % (
        width, height, width, height,
        width, height, background,
        icon_x, (height - icon_px) // 2, icon_px, icon_px, uri,
        text_x, height // 2, color, font_px, html.escape(name),
    )
    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        _ = fh.write(svg)
    print("wrote %s (%dx%d SVG, icon %s: %s)" % (out, width, height, verdict, why))
    if len(name) * font_px * 0.56 > text_room:
        print("warning: the name may not fit; shorten --name")
    return 0


# --- readme -------------------------------------------------------------------------------
# Quiver serves everything outside an arrow's first ```arrow fence as its readme,
# and Quiver Desktop renders it in the Overview tab as sanitized GFM: images need
# absolute https:// (or data:) URLs, and iframes and scripts are dropped.

README_MIN_WORDS = 150
MD_IMAGE = re.compile(r"!\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
HTML_SRC = re.compile(r"<(img|video|source|audio|track)\b[^>]*?\bsrc\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)
FORBIDDEN_TAGS = re.compile(r"<\s*(iframe|script|style|object|embed)\b", re.IGNORECASE)


def split_markdown_arrow(text: str) -> tuple[str, str]:
    """Return (readme, manifest) the way Quiver splits ARROW.md / <path>.md."""
    lines = text.replace("\r", "").split("\n")
    start = next((i for i, line in enumerate(lines) if line == "```arrow"), -1)
    if start < 0:
        raise ToolError("no ```arrow fence: Quiver reads this file as plain YAML, with no readme")
    end = next((i for i in range(start + 1, len(lines)) if lines[i] == "```"), -1)
    if end < 0:
        raise ToolError("the ```arrow fence is never closed")
    readme = "\n".join(lines[:start] + lines[end + 1 :]).strip()
    return readme, "\n".join(lines[start + 1 : end])


def readme_images(readme: str) -> list[tuple[str, str, bool]]:
    """(alt, url, is_markdown) for every embedded image or media source."""
    found = [(m.group(1), m.group(2), True) for m in MD_IMAGE.finditer(readme)]
    found.extend(("", m.group(2), False) for m in HTML_SRC.finditer(readme))
    return found


def readme_problems(readme: str, online: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not readme:
        errors.append("no prose outside the ```arrow fence: Overview would show only the Details card")
        return errors, warnings
    words = len(re.findall(r"[A-Za-z0-9']+", re.sub(r"\(https?://[^)]*\)", "", readme)))
    if words < README_MIN_WORDS:
        warnings.append("only %d words; aim for a short but complete page (references/readme.md §4)" % words)
    if "```arrow" in readme.split("\n"):
        warnings.append("a second ```arrow fence: Quiver ignores it and shows it as code in the readme")
    if re.search(r"^# ", readme, re.MULTILINE):
        warnings.append("a top-level '# ' title: the page hero already shows the name")
    for match in FORBIDDEN_TAGS.finditer(readme):
        errors.append("<%s> is removed by the desktop's sanitizer" % match.group(1).lower())
    images = readme_images(readme)
    if not images:
        warnings.append("no images: add at least one screenshot of the software (references/readme.md §6)")
    for alt, url, is_markdown in images:
        if url.startswith("data:"):
            continue
        if not url.startswith("https://"):
            errors.append("image %s: needs an absolute https:// URL (relative paths do not render)" % url)
            continue
        if is_markdown and not alt.strip():
            warnings.append("image %s has no alt text" % url)
        if online:
            try:
                info = sniff_image(read_media(url))
            except ToolError as err:
                errors.append("image %s does not load: %s" % (url, err))
                continue
            size = "%dx%d" % (info.width, info.height) if info.known else "size unknown"
            if info.fmt == "unknown":
                errors.append("image %s is not an image format a webview displays" % url)
            else:
                print("  ok  %s (%s, %s)" % (url, info.fmt, size))
    return errors, warnings


def cmd_readme(args: Args) -> int:
    worst = 0
    for path in args.files:
        with open(path, encoding="utf-8") as fh:
            readme, _ = split_markdown_arrow(fh.read())
        print("%s: %d characters of readme" % (path, len(readme)))
        errors, warnings = readme_problems(readme, args.online)
        for message in errors:
            print("  error:   %s" % message)
        for message in warnings:
            print("  warning: %s" % message)
        if errors:
            worst = 1
        elif not warnings:
            print("  readme looks good")
    return worst


def sandbox_readme(args: Args) -> int:
    status, payload = sandbox_daemon().request("GET", "/v0/arrow/%s/readme" % encode_ns(args.namespace))
    if status == 404:
        print("%s has no readme (plain YAML, or no prose outside the ```arrow fence)" % args.namespace)
        return 1
    if status != 200:
        raise ToolError("GET readme %s -> HTTP %d: %s" % (args.namespace, status, error_text(payload)))
    readme = as_str(as_object(payload.get("data")).get("readme"))
    print("%s serves %d characters of readme:\n" % (args.namespace, len(readme)))
    print(readme[:600] + ("\n[...]" if len(readme) > 600 else ""))
    return 0


# --- sandbox -----------------------------------------------------------------------


def sandbox_dir() -> str:
    # Absolute from the start: the daemon is launched with the sandbox as its
    # working directory, where a relative path would point somewhere else.
    configured = os.environ.get("QUIVER_SANDBOX_DIR") or os.path.join(tempfile.gettempdir(), "quiver-arrow-sandbox")
    return os.path.realpath(configured)


def sandbox_socket() -> str:
    # Unix socket paths are capped near 104 bytes, so the socket cannot live
    # under a long sandbox directory. It is named after the sandbox directory
    # instead, so two sandboxes never share (or adopt) one another's daemon.
    explicit = os.environ.get("QUIVER_SANDBOX_SOCKET")
    if explicit:
        return os.path.abspath(explicit)
    uid = os.getuid() if hasattr(os, "getuid") else 0
    digest = hashlib.sha256(sandbox_dir().encode("utf-8")).hexdigest()[:12]
    return "/tmp/quiver-arrow-sandbox-%d-%s.sock" % (uid, digest)


def sandbox_daemon() -> Daemon:
    return Daemon(socket_path=sandbox_socket())


def find_quiver_binary() -> str:
    explicit = os.environ.get("QUIVER_BIN")
    if explicit:
        path = os.path.abspath(explicit)
        if not (os.path.isfile(path) and os.access(path, os.X_OK)):
            raise ToolError("QUIVER_BIN=%s is not an executable file" % explicit)
        return path
    candidates = [shutil.which("quiver") or "", os.path.join(os.path.expanduser("~"), ".quiver", "self", "quiver")]
    for candidate in candidates:
        if candidate and os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return os.path.abspath(candidate)
    raise ToolError("no quiver binary found: install quiver.core, or set QUIVER_BIN to its path")


def pid_file() -> str:
    return os.path.join(sandbox_dir(), "daemon.pid")


def read_pid() -> int | None:
    try:
        with open(pid_file()) as fh:
            return int(fh.read().strip())
    except (OSError, ValueError):
        return None


def remove_pid_file() -> None:
    try:
        os.remove(pid_file())
    except OSError:
        pass


def process_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def is_sandbox_daemon(pid: int) -> bool:
    # A pid file can outlive its process and the pid be reused, so a pid is
    # only signalled when that process's command line names this sandbox's
    # own socket. Anything unverifiable is treated as not ours.
    try:
        out = subprocess.run(
            ["ps", "-p", str(pid), "-o", "command="],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return out.returncode == 0 and ("unix://" + sandbox_socket()) in out.stdout


def wait_gone(pid: int, seconds: float) -> bool:
    deadline = time.time() + seconds
    while time.time() < deadline:
        if not process_alive(pid):
            return True
        time.sleep(0.25)
    return not process_alive(pid)


def sandbox_start(_args: Args) -> int:
    if os.name == "nt":
        raise ToolError("the sandbox needs Unix sockets; on Windows run it under WSL, or point QUIVER_API at a test daemon")
    daemon = sandbox_daemon()
    if daemon.healthy():
        print("sandbox already running at %s" % daemon.describe())
        return 0
    binary = find_quiver_binary()
    home = os.path.join(sandbox_dir(), "home")
    os.makedirs(home, exist_ok=True)
    log_path = os.path.join(sandbox_dir(), "daemon.log")
    env = dict(os.environ, QUIVER_HOME=home)
    with open(log_path, "ab") as log:
        proc = subprocess.Popen(
            [binary, "daemon", "--host", "unix://" + daemon.socket_path],
            env=env,
            cwd=sandbox_dir(),
            stdout=log,
            stderr=log,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
    with open(pid_file(), "w") as fh:
        _ = fh.write(str(proc.pid))
    deadline = time.time() + SANDBOX_START_SECONDS
    while time.time() < deadline:
        if proc.poll() is not None:
            remove_pid_file()
            raise ToolError("sandbox daemon exited with %s; see %s" % (proc.returncode, log_path))
        if daemon.healthy():
            print("sandbox running: %s  (QUIVER_HOME=%s, binary=%s)" % (daemon.describe(), home, binary))
            return 0
        time.sleep(0.5)
    proc.terminate()
    try:
        _ = proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
    remove_pid_file()
    raise ToolError("sandbox daemon did not become healthy in %ds; stopped it; see %s" % (SANDBOX_START_SECONDS, log_path))


def sandbox_stop(_args: Args) -> int:
    pid = read_pid()
    if pid is None:
        print("sandbox not running")
        return 0
    if not process_alive(pid):
        remove_pid_file()
        print("sandbox not running (removed a stale pid file)")
        return 0
    if not is_sandbox_daemon(pid):
        remove_pid_file()
        raise ToolError(
            "pid %d is not this sandbox's daemon (stale pid file, now removed); nothing was signalled" % pid
        )
    os.kill(pid, signal.SIGTERM)
    if not wait_gone(pid, 15):
        raise ToolError("sandbox daemon (pid %d) did not stop within 15s; it is still running" % pid)
    remove_pid_file()
    print("sandbox stopped (data kept in %s; delete it for a clean slate)" % sandbox_dir())
    return 0


def require_ref(namespace: str) -> None:
    if "@" not in namespace:
        raise ToolError("namespace %r needs an explicit @ref (seeding never resolves a ref)" % namespace)


def bare_namespace(namespace: str) -> str:
    return namespace.split("@", 1)[0]


def sandbox_seed(args: Args) -> int:
    require_ref(args.namespace)
    with open(args.file, "rb") as fh:
        data = fh.read()
    daemon = sandbox_daemon()
    result = validate_bytes(daemon, data, False, args.namespace)
    if result.get("valid") is not True:
        return report_validation(args.file, result)
    status, payload = daemon.request(
        "POST", "/v0/arrow/%s/manifest" % encode_ns(args.namespace), body=data, content_type="application/x-yaml"
    )
    if status >= 300:
        print("seed failed (HTTP %d): %s" % (status, error_text(payload)))
        return 1
    print("seeded %s" % args.namespace)
    return 0


def parse_vars(pairs: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise ToolError("variable %r must be KEY=VALUE" % pair)
        key, value = pair.split("=", 1)
        out[key] = value
    return out


def arrow_detail_or_none(daemon: Daemon, namespace: str) -> JSONObject | None:
    status, payload = daemon.request("GET", "/v0/arrow/%s" % encode_ns(namespace))
    if status == 404:
        return None
    if status != 200:
        raise ToolError("GET arrow %s -> HTTP %d: %s" % (namespace, status, error_text(payload)))
    return as_object(payload.get("data"))


def arrow_detail(daemon: Daemon, namespace: str) -> JSONObject:
    detail = arrow_detail_or_none(daemon, namespace)
    if detail is None:
        raise ToolError("arrow %s is not in the sandbox catalog (seed it first)" % namespace)
    return detail


def desktop_risk(daemon: Daemon, namespace: str) -> str:
    """Why installing namespace may write desktop entries, or "" when it cannot."""
    status, payload = daemon.request("GET", "/v0/arrow/%s/manifest" % encode_ns(namespace))
    if status != 200:
        return "its compiled manifest could not be read (HTTP %d)" % status
    targets = as_object(as_object(payload.get("data")).get("targets"))
    for platform, raw in targets.items():
        target = as_object(raw)
        if as_list(as_object(target.get("expose")).get("desktop")):
            return "it declares desktop entries (%s)" % platform
        if as_list(target.get("tools")) or as_list(target.get("services")):
            return "it has dependencies (%s), whose desktop entries cannot be checked in advance" % platform
    return ""


def guard_desktop(daemon: Daemon, namespace: str) -> None:
    if os.environ.get("QUIVER_SANDBOX_ALLOW_DESKTOP") == "1":
        return
    reason = desktop_risk(daemon, namespace)
    if reason:
        raise ToolError(
            "not installing %s: %s.\n" % (namespace, reason)
            + "The sandbox isolates Quiver's data and ~/.quiver/bin, but desktop entries are always written to\n"
            + "the real system (Applications, ~/.local/share/applications, the Start Menu). Ask the user first,\n"
            + "then re-run with QUIVER_SANDBOX_ALLOW_DESKTOP=1."
        )


def print_run(detail: JSONObject) -> None:
    print("state: %s" % as_str(detail.get("state")))
    active = as_object(detail.get("active_run"))
    run = active or as_object(detail.get("last_return"))
    if not run:
        return
    label = "active run" if active else "last run"
    outcome = as_str(run.get("outcome"))
    print("%s: %s%s" % (label, as_str(run.get("method")), " -> " + outcome if outcome else ""))
    for item in as_list(run.get("steps")):
        step = as_object(item)
        line = "  %-9s %s" % (as_str(step.get("status")), as_str(step.get("title")) or as_str(step.get("type")))
        error = as_str(step.get("error"))
        if error:
            line += "\n            error: %s" % error
        print(line)


def return_marker(detail: JSONObject) -> str:
    # The daemon keeps the previous run's `last_return` while a new run is
    # active, so "finished" means: nothing active, and a return that differs
    # from the one recorded before the request was sent.
    return json.dumps(detail.get("last_return"), sort_keys=True)


def followed_update(daemon: Daemon, namespace: str) -> str:
    # An update without an `update:` hook reinstalls: the arrow moves to a new
    # namespace@ref and the old one leaves the catalog.
    status, payload = daemon.request("GET", "/v0/arrow")
    if status != 200:
        return ""
    old_ref = namespace.split("@", 1)[1] if "@" in namespace else ""
    for item in as_list(payload.get("data")):
        entry = as_object(item)
        if as_str(entry.get("namespace")) != bare_namespace(namespace):
            continue
        for raw in as_list(entry.get("versions")):
            ref = as_str(as_object(raw).get("ref"))
            if ref and ref != old_ref:
                return bare_namespace(namespace) + "@" + ref
    return ""


def await_run(daemon: Daemon, namespace: str, method: str, before: str) -> tuple[str, JSONObject | None]:
    """Poll until the requested run ends (or, for execute, keeps running)."""
    deadline = time.time() + INSTALL_TIMEOUT_SECONDS
    running_since = 0.0
    while time.time() < deadline:
        detail = arrow_detail_or_none(daemon, namespace)
        if detail is None:
            moved = followed_update(daemon, namespace) if method == "update" else ""
            if not moved:
                raise ToolError("arrow %s disappeared from the catalog during %s" % (namespace, method))
            print("update moved the arrow to %s" % moved)
            namespace, before = moved, "null"
            time.sleep(POLL_SECONDS)
            continue
        active = as_object(detail.get("active_run"))
        if method == "execute" and as_str(active.get("method")) == "_execute":
            running_since = running_since or time.time()
            if time.time() - running_since >= EXECUTE_SETTLE_SECONDS:
                return "running", detail
        elif not active and as_str(detail.get("state")) not in ACTIVE_STATES and return_marker(detail) != before:
            return "finished", detail
        time.sleep(POLL_SECONDS)
    return "timeout", arrow_detail_or_none(daemon, namespace)


def run_method(daemon: Daemon, namespace: str, method: str, variables: dict[str, str]) -> int:
    if method in ("install", "update"):
        guard_desktop(daemon, namespace)
    before = return_marker(arrow_detail(daemon, namespace))
    body = json.dumps({"variables": variables}).encode("utf-8")
    status, payload = daemon.request(
        "POST", "/v0/runtime/%s/%s" % (encode_ns(namespace), method), body=body, content_type="application/json"
    )
    if status >= 300:
        print("%s refused (HTTP %d): %s" % (method, status, error_text(payload)))
        return 1
    if status == 200:
        # 200 instead of 202: the daemon had nothing to do (already installed).
        print("%s: nothing to do" % method)
        print_run(arrow_detail(daemon, namespace))
        return 0
    result, detail = await_run(daemon, namespace, method, before)
    if detail is not None:
        print_run(detail)
    if result == "running":
        print("still running after %ds: the service started. Probe it, then `sandbox stop`." % EXECUTE_SETTLE_SECONDS)
        return 0
    if result == "timeout":
        print("gave up waiting after %ds; the run may still be active (`sandbox status`)." % INSTALL_TIMEOUT_SECONDS)
        return 1
    last = as_object((detail or {}).get("last_return"))
    return 0 if as_str(last.get("outcome")) == "success" else 1


def sandbox_method(method: str) -> Callable[[Args], int]:
    def handler(args: Args) -> int:
        return run_method(sandbox_daemon(), args.namespace, method, parse_vars(args.vars))

    return handler


def sandbox_custom_method(args: Args) -> int:
    return run_method(sandbox_daemon(), args.namespace, args.method, parse_vars(args.vars))


def sandbox_status(args: Args) -> int:
    print_run(arrow_detail(sandbox_daemon(), args.namespace))
    return 0


def sandbox_remove(args: Args) -> int:
    # Uninstall runs the arrow's `uninstall:` steps and removes its exposed
    # entries; only removing the arrow from the catalog deletes its workdir.
    # Removing without uninstalling first leaves its ~/.quiver/bin links
    # dangling, so an installed arrow is uninstalled before it is removed.
    daemon = sandbox_daemon()
    state = as_str(arrow_detail(daemon, args.namespace).get("state"))
    if state == "running":
        _ = run_method(daemon, args.namespace, "stop", {})
        state = as_str(arrow_detail(daemon, args.namespace).get("state"))
    if state != "absent" and run_method(daemon, args.namespace, "uninstall", {}) != 0:
        print("uninstall failed; not removing %s" % args.namespace)
        return 1
    status, payload = daemon.request("DELETE", "/v0/arrow/%s" % encode_ns(args.namespace))
    if status >= 300:
        print("remove refused (HTTP %d): %s" % (status, error_text(payload)))
        return 1
    print("removed %s (catalog entry and workdir)" % args.namespace)
    return 0


# --- bundle ----------------------------------------------------------------------------


def cmd_bundle(_args: Args) -> int:
    # One Markdown document for assistants that cannot load a skill folder:
    # SKILL.md first, then every reference, example and template, each under
    # a heading naming the path the rest of the text refers to it by.
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parts = [os.path.join(root, "SKILL.md")]
    for sub in ("references", "assets/examples", "assets/templates"):
        folder = os.path.join(root, sub)
        parts.extend(os.path.join(folder, name) for name in sorted(os.listdir(folder)))
    out = sys.stdout
    _ = out.write(
        "<!-- Generated by scripts/quiver_arrow.py bundle. The scripts are not included:\n"
        + "     without a shell, validate by hand with references/validation-and-testing.md section 6. -->\n\n"
    )
    for path in parts:
        rel = os.path.relpath(path, root)
        with open(path, encoding="utf-8") as fh:
            body = fh.read().rstrip() + "\n"
        if rel == "SKILL.md":
            _ = out.write(body + "\n")
        elif rel.startswith("references/"):
            _ = out.write("\n---\n\n# File: %s\n\n%s\n" % (rel, body))
        else:
            fence = "````" if "```" in body else "```"
            lang = "yaml" if rel.endswith(".yaml") else "markdown"
            _ = out.write("\n---\n\n# File: %s\n\n%s%s\n%s%s\n" % (rel, fence, lang, body, fence))
    return 0


# --- entry point -------------------------------------------------------------------------


def add_sandbox_parsers(sandbox: argparse.ArgumentParser) -> None:
    sb = sandbox.add_subparsers(dest="action", required=True)
    _ = sb.add_parser("up", help="start the isolated sandbox daemon").set_defaults(func=sandbox_start)
    _ = sb.add_parser("down", help="stop the sandbox daemon").set_defaults(func=sandbox_stop)

    p = sb.add_parser("seed", help="validate and register a manifest (namespace needs an @ref)")
    _ = p.add_argument("namespace")
    _ = p.add_argument("file")
    p.set_defaults(func=sandbox_seed)

    for method in ("install", "execute", "update", "uninstall"):
        p = sb.add_parser(method, help="run the arrow's %s lifecycle" % method)
        _ = p.add_argument("namespace")
        _ = p.add_argument("vars", nargs="*", metavar="KEY=VALUE")
        p.set_defaults(func=sandbox_method(method))

    # The daemon ignores variables on stop, so none are accepted here.
    p = sb.add_parser("stop", help="run the arrow's stop lifecycle")
    _ = p.add_argument("namespace")
    p.set_defaults(func=sandbox_method("stop"))

    p = sb.add_parser("run", help="run a custom manifest method")
    _ = p.add_argument("namespace")
    _ = p.add_argument("method")
    _ = p.add_argument("vars", nargs="*", metavar="KEY=VALUE")
    p.set_defaults(func=sandbox_custom_method)

    p = sb.add_parser("status", help="show the arrow's state and last run")
    _ = p.add_argument("namespace")
    p.set_defaults(func=sandbox_status)

    p = sb.add_parser("readme", help="print the readme the daemon serves for an arrow")
    _ = p.add_argument("namespace")
    p.set_defaults(func=sandbox_readme)

    p = sb.add_parser("remove", help="uninstall, remove from the catalog and delete the workdir")
    _ = p.add_argument("namespace")
    p.set_defaults(func=sandbox_remove)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate, inspect and test-install Quiver arrows.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("validate", help="validate manifests against a quiver daemon")
    _ = p.add_argument("files", nargs="+")
    _ = p.add_argument("--collection", action="store_true", help="validate collection@v0 manifests")
    _ = p.add_argument("--namespace", default="", help="namespace to validate under (only needs to be well-formed)")
    _ = p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("assets", help="list a GitHub release's assets with their sha256 digests")
    _ = p.add_argument("repo", help="owner/repo")
    _ = p.add_argument("tag", nargs="?", default="", help="release tag (default: latest stable release)")
    _ = p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_assets)

    p = sub.add_parser("checksum", help="download a URL and print its sha256")
    _ = p.add_argument("url")
    p.set_defaults(func=cmd_checksum)

    p = sub.add_parser("media", help="check whether images (URLs or files) fit as icon / banner")
    _ = p.add_argument("files", nargs="+", metavar="URL_OR_FILE")
    p.set_defaults(func=cmd_media)

    p = sub.add_parser("banner", help="generate a 2:1 SVG banner around an official icon")
    _ = p.add_argument("--icon", required=True, help="official icon, URL or file (SVG preferred)")
    _ = p.add_argument("--name", required=True, help="display name written on the banner")
    _ = p.add_argument("--background", required=True, help="brand colour as #RRGGBB")
    _ = p.add_argument("--text-color", default="", help="#RRGGBB; default: black or white for contrast")
    _ = p.add_argument("--out", required=True, help="output path, e.g. media/<auid>/banner.svg")
    p.set_defaults(func=cmd_banner)

    p = sub.add_parser("readme", help="check the readme an ARROW.md / <path>.md would serve")
    _ = p.add_argument("files", nargs="+")
    _ = p.add_argument("--online", action="store_true", help="also fetch every image and check it loads")
    p.set_defaults(func=cmd_readme)

    p = sub.add_parser("bundle", help="print the whole skill as one Markdown file, for chat assistants")
    p.set_defaults(func=cmd_bundle)

    add_sandbox_parsers(sub.add_parser("sandbox", help="isolated daemon for test installs"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv, namespace=Args())
    try:
        return args.func(args)
    except (ToolError, OSError) as err:
        print("error: %s" % err, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
