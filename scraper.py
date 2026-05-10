#!/usr/bin/env python3
"""
SHΞN™ VPN Client Release Aggregator
Collects latest release assets from curated GitHub repos
Generates ☬SHΞN™.json
"""

import os
import re
import json
import requests
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Token (from env var SHEN_GITHUB_TOKEN, or anonymous)
# ---------------------------------------------------------------------------
TOKEN = os.environ.get("SHEN_GITHUB_TOKEN", "")

HEADERS = {"Accept": "application/vnd.github.v3+json"}
if TOKEN:
    HEADERS["Authorization"] = f"token {TOKEN}"

# ---------------------------------------------------------------------------
# Client definitions
# ---------------------------------------------------------------------------
CLIENTS = [
    {
        "id": "v2rayng",
        "name": "v2rayNG",
        "desc": "V2Ray/Xray client for Android",
        "platform": "Android",
        "repo": "2dust/v2rayNG",
        "pattern": r"\.apk$",
        "website": "https://github.com/2dust/v2rayNG"
    },
    {
        "id": "v2rayn",
        "name": "v2rayN",
        "desc": "V2Ray/Xray/Sing-box client for Windows",
        "platform": "Windows",
        "repo": "2dust/v2rayN",
        "pattern": r"\.zip$",
        "website": "https://github.com/2dust/v2rayN"
    },
    {
        "id": "hiddify_next",
        "name": "Hiddify Next",
        "desc": "Multi-platform Sing-box client",
        "platform": "Android/Windows/Linux/macOS",
        "repo": "hiddify/Hiddify-Next",
        "pattern": None,
        "website": "https://github.com/hiddify/Hiddify-Next"
    },
    {
        "id": "hiddify_ng",
        "name": "HiddifyNG",
        "desc": "Legacy Xray-based client for Android",
        "platform": "Android",
        "repo": "hiddify/HiddifyNG",
        "pattern": r"\.apk$",
        "website": "https://github.com/hiddify/HiddifyNG"
    },
    {
        "id": "mahsang",
        "name": "MahsaNG",
        "desc": "Decentralised VPN with special protocols",
        "platform": "Android",
        "repo": "GFW-knocker/MahsaNG",
        "pattern": r"\.apk$",
        "website": "https://github.com/GFW-knocker/MahsaNG"
    },
    {
        "id": "nekobox_android",
        "name": "NekoBox for Android",
        "desc": "Modern proxy client based on Sing-box",
        "platform": "Android",
        "repo": "MatsuriDayo/NekoBoxForAndroid",
        "pattern": r"\.apk$",
        "website": "https://github.com/MatsuriDayo/NekoBoxForAndroid"
    },
    {
        "id": "matsuri",
        "name": "Matsuri",
        "desc": "SagerNet fork with enhanced protocol support",
        "platform": "Android",
        "repo": "MatsuriDayo/Matsuri",
        "pattern": r"\.apk$",
        "website": "https://github.com/MatsuriDayo/Matsuri"
    },
    {
        "id": "sagernet",
        "name": "SagerNet",
        "desc": "Universal proxy toolchain for Android",
        "platform": "Android",
        "repo": "SagerNet/SagerNet",
        "pattern": r"\.apk$",
        "website": "https://github.com/SagerNet/SagerNet"
    },
    {
        "id": "clash_meta_android",
        "name": "Clash Meta for Android",
        "desc": "Clash.Meta based proxy client",
        "platform": "Android",
        "repo": "MetaCubeX/ClashMetaForAndroid",
        "pattern": r"\.apk$",
        "website": "https://github.com/MetaCubeX/ClashMetaForAndroid"
    },
    {
        "id": "sing_box",
        "name": "Sing-Box",
        "desc": "Universal proxy platform",
        "platform": "Android/Windows/Linux/macOS/iOS",
        "repo": "SagerNet/sing-box",
        "pattern": None,
        "website": "https://github.com/SagerNet/sing-box"
    },
    {
        "id": "hysteria",
        "name": "Hysteria",
        "desc": "Powerful, censorship-resistant proxy",
        "platform": "Android/Windows/Linux/macOS",
        "repo": "apernet/hysteria",
        "pattern": None,
        "website": "https://github.com/apernet/hysteria"
    },
    {
        "id": "nekoray",
        "name": "Nekoray",
        "desc": "Qt-based desktop client with Sing-box",
        "platform": "Windows/Linux",
        "repo": "MatsuriDayo/nekoray",
        "pattern": r"\.(zip|tar\.gz|AppImage|exe|deb|rpm)$",
        "website": "https://github.com/MatsuriDayo/nekoray"
    },
    {
        "id": "nekobox_desktop",
        "name": "NekoBox Desktop",
        "desc": "Cross-platform Qt client based on Sing-box",
        "platform": "Windows/Linux",
        "repo": "qr243vbi/nekobox",
        "pattern": None,
        "website": "https://github.com/qr243vbi/nekobox"
    },
    {
        "id": "shadowsocks_android",
        "name": "Shadowsocks Android",
        "desc": "Official Shadowsocks client for Android",
        "platform": "Android",
        "repo": "shadowsocks/shadowsocks-android",
        "pattern": r"\.apk$",
        "website": "https://github.com/shadowsocks/shadowsocks-android"
    },
    {
        "id": "v2fly_core",
        "name": "V2Fly Core",
        "desc": "V2Ray core (advanced users)",
        "platform": "Windows/Linux/macOS",
        "repo": "v2fly/v2ray-core",
        "pattern": r"\.(zip|tar\.gz)$",
        "website": "https://github.com/v2fly/v2ray-core"
    },
    {
        "id": "xray_core",
        "name": "Xray-Core",
        "desc": "Xray core (Project X, V2Ray fork)",
        "platform": "Android/Windows/Linux/macOS/iOS",
        "repo": "XTLS/Xray-core",
        "pattern": r"\.(zip|tar\.gz)$",
        "website": "https://github.com/XTLS/Xray-core"
    },
    {
        "id": "slipnet",
        "name": "SlipNet",
        "desc": "Xray-based proxy sharing platform",
        "platform": "Android/Windows/Linux",
        "repo": "anonvector/SlipNet",
        "pattern": None,
        "website": "https://github.com/anonvector/SlipNet"
    },
    {
        "id": "happ",
        "name": "Happ",
        "desc": "Proxy manager with Xray core (Android)",
        "platform": "Android",
        "repo": "Happ-proxy/happ-android",
        "pattern": r"\.apk$",
        "website": "https://github.com/Happ-proxy/happ-android"
    },
    {
        "id": "husi",
        "name": "Husi",
        "desc": "Amateurish proxy tool integration",
        "platform": "Android",
        "repo": "xchacha20-poly1305/husi",
        "pattern": r"\.apk$",
        "website": "https://github.com/xchacha20-poly1305/husi"
    },
    {
        "id": "thefeed",
        "name": "Thefeed",
        "desc": "Android VPN client",
        "platform": "Android",
        "repo": "sartoopjj/thefeed",
        "pattern": r"\.apk$",
        "website": "https://github.com/sartoopjj/thefeed"
    },
    {
        "id": "masterdns",
        "name": "Master DNS VPN",
        "desc": "DNS changer & filtering bypass for Android",
        "platform": "Android",
        "repo": "Hidden-Node/MasterDnsVPN-AndroidClient",
        "pattern": r"\.apk$",
        "website": "https://github.com/Hidden-Node/MasterDnsVPN-AndroidClient"
    },
]

OUTPUT_FILE = "☬SHΞN™.json"

# ---------------------------------------------------------------------------
def fetch_latest_release(repo):
    """Return latest release data (prefers stable, falls back to any)."""
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            return resp.json()
        # If no stable release, grab the most recent release (including pre-release)
        first_page = f"https://api.github.com/repos/{repo}/releases?per_page=1"
        resp2 = requests.get(first_page, headers=HEADERS, timeout=15)
        if resp2.status_code == 200 and resp2.json():
            return resp2.json()[0]
    except Exception:
        pass
    return None

def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def matches_pattern(filename, pattern):
    if pattern is None:
        return True
    return re.search(pattern, filename, re.IGNORECASE) is not None

# ---------------------------------------------------------------------------
def main():
    clients_data = []
    ok = 0
    fail = 0

    for c in CLIENTS:
        print(f"Fetching {c['name']} ... ", end="")
        release = fetch_latest_release(c["repo"])
        if not release:
            print("FAIL")
            fail += 1
            continue

        tag = release.get("tag_name", "unknown")
        assets = []
        for a in release.get("assets", []):
            if matches_pattern(a["name"], c["pattern"]):
                assets.append({
                    "filename": a["name"],
                    "size": a["size"],
                    "size_formatted": format_size(a["size"]),
                    "download_url": a["browser_download_url"],
                    "downloads": a["download_count"],
                })

        clients_data.append({
            "id": c["id"],
            "name": c["name"],
            "desc": c["desc"],
            "platform": c["platform"],
            "repo": c["repo"],
            "website": c["website"],
            "latest_version": {
                "tag": tag,
                "name": release.get("name") or tag,
                "release_date": release.get("published_at"),
                "release_url": release.get("html_url"),
                "changelog_preview": (release.get("body") or "")[:500],
                "assets": assets,
            }
        })
        print(f"OK ({tag}, {len(assets)} assets)")
        ok += 1

    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_clients": len(CLIENTS),
        "successful": ok,
        "failed": fail,
        "clients": clients_data,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"\nDone. {ok} succeeded, {fail} failed → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
