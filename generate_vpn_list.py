#!/usr/bin/env python3
import requests
import json
import os
import re
from datetime import datetime, timezone

# =============================================================================
# توکن از environment variable خوانده می‌شود. برای استفاده لوکال می‌توانید
# متغیر GITHUB_TOKEN را ست کنید یا فایل را ویرایش و مقداردهی مستقیم کنید.
# =============================================================================
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

# =============================================================================
# لیست کامل کلاینت‌های VPN (با SlipNet، Happ، Husi و سایر موارد محبوب)
# =============================================================================
VPN_CLIENTS = [
    {
        "id": "v2rayng",
        "name": "v2rayNG",
        "desc": "کلاینت V2Ray/Xray برای اندروید",
        "platform": "Android",
        "repo": "2dust/v2rayNG",
        "asset_pattern": r".*\.apk$",
        "website": "https://github.com/2dust/v2rayNG"
    },
    {
        "id": "v2rayn",
        "name": "v2rayN",
        "desc": "کلاینت V2Ray/Xray/Sing-box برای ویندوز",
        "platform": "Windows",
        "repo": "2dust/v2rayN",
        "asset_pattern": r".*\.zip$",
        "website": "https://github.com/2dust/v2rayN"
    },
    {
        "id": "hiddify_next",
        "name": "Hiddify Next",
        "desc": "کلاینت مالتی‌پلتفرم مبتنی بر Sing-box",
        "platform": "Android/Windows/Linux/macOS",
        "repo": "hiddify/Hiddify-Next",
        "asset_pattern": None,
        "website": "https://github.com/hiddify/Hiddify-Next"
    },
    {
        "id": "hiddify_ng",
        "name": "HiddifyNG",
        "desc": "نسخه قدیمی اندروید",
        "platform": "Android",
        "repo": "hiddify/HiddifyNG",
        "asset_pattern": r".*\.apk$",
        "website": "https://github.com/hiddify/HiddifyNG"
    },
    {
        "id": "mahsang",
        "name": "MahsaNG",
        "desc": "وی‌پی‌ان غیرمتمرکز",
        "platform": "Android",
        "repo": "GFW-knocker/MahsaNG",
        "asset_pattern": r".*\.apk$",
        "website": "https://github.com/GFW-knocker/MahsaNG"
    },
    {
        "id": "nekobox_android",
        "name": "NekoBox for Android",
        "desc": "کلاینت پروکسی مدرن مبتنی بر Sing-box",
        "platform": "Android",
        "repo": "MatsuriDayo/NekoBoxForAndroid",
        "asset_pattern": r".*\.apk$",
        "website": "https://github.com/MatsuriDayo/NekoBoxForAndroid"
    },
    {
        "id": "matsuri",
        "name": "Matsuri",
        "desc": "فورک SagerNet",
        "platform": "Android",
        "repo": "MatsuriDayo/Matsuri",
        "asset_pattern": r".*\.apk$",
        "website": "https://github.com/MatsuriDayo/Matsuri"
    },
    {
        "id": "sagernet",
        "name": "SagerNet",
        "desc": "جعبه ابزار پروکسی جهانی",
        "platform": "Android",
        "repo": "SagerNet/SagerNet",
        "asset_pattern": r".*\.apk$",
        "website": "https://github.com/SagerNet/SagerNet"
    },
    {
        "id": "clash_meta_android",
        "name": "Clash Meta for Android",
        "desc": "کلاینت Clash.Meta",
        "platform": "Android",
        "repo": "MetaCubeX/ClashMetaForAndroid",
        "asset_pattern": r".*\.apk$",
        "website": "https://github.com/MetaCubeX/ClashMetaForAndroid"
    },
    {
        "id": "sing_box",
        "name": "Sing-Box",
        "desc": "پلتفرم پروکسی جهانی SagerNet",
        "platform": "Android/Windows/Linux/macOS/iOS",
        "repo": "SagerNet/sing-box",
        "asset_pattern": None,
        "website": "https://github.com/SagerNet/sing-box"
    },
    {
        "id": "hysteria",
        "name": "Hysteria",
        "desc": "پروکسی قدرتمند و مقاوم در برابر سانسور",
        "platform": "Android/Windows/Linux/macOS",
        "repo": "apernet/hysteria",
        "asset_pattern": None,
        "website": "https://github.com/apernet/hysteria"
    },
    {
        "id": "nekoray",
        "name": "Nekoray",
        "desc": "کلاینت دسکتاپ مبتنی بر Qt و Sing-box",
        "platform": "Windows/Linux",
        "repo": "MatsuriDayo/nekoray",
        "asset_pattern": r".*\.(zip|tar\.gz|AppImage|exe|deb|rpm)$",
        "website": "https://github.com/MatsuriDayo/nekoray"
    },
    {
        "id": "nekobox_desktop",
        "name": "NekoBox Desktop",
        "desc": "کلاینت Qt کراس‌پلتفرم مبتنی بر Sing-box",
        "platform": "Windows/Linux",
        "repo": "qr243vbi/nekobox",
        "asset_pattern": None,
        "website": "https://github.com/qr243vbi/nekobox"
    },
    {
        "id": "shadowsocks_android",
        "name": "Shadowsocks Android",
        "desc": "کلاینت رسمی Shadowsocks برای اندروید",
        "platform": "Android",
        "repo": "shadowsocks/shadowsocks-android",
        "asset_pattern": r".*\.apk$",
        "website": "https://github.com/shadowsocks/shadowsocks-android"
    },
    {
        "id": "v2fly_core",
        "name": "V2Fly (V2Ray Core)",
        "desc": "هسته اصلی V2Ray (برای کاربران حرفه‌ای)",
        "platform": "Windows/Linux/macOS",
        "repo": "v2fly/v2ray-core",
        "asset_pattern": r".*\.(zip|tar\.gz)$",
        "website": "https://github.com/v2fly/v2ray-core"
    },
    {
        "id": "xray_core",
        "name": "Xray-Core",
        "desc": "هسته Xray (فورک پیشرفته V2Ray از Project X)",
        "platform": "Android/Windows/Linux/macOS/iOS",
        "repo": "XTLS/Xray-core",
        "asset_pattern": r".*\.(zip|tar\.gz)$",
        "website": "https://github.com/XTLS/Xray-core"
    },
    {
        "id": "slipnet",
        "name": "SlipNet",
        "desc": "پلتفرم اشتراک‌گذاری پروکسی مبتنی بر Xray",
        "platform": "Android/Windows/Linux",
        "repo": "anonvector/SlipNet",
        "asset_pattern": None,
        "website": "https://github.com/anonvector/SlipNet"
    },
    {
        "id": "happ",
        "name": "Happ",
        "desc": "اپ مدیریت پروکسی با هسته Xray (مخصوص اندروید)",
        "platform": "Android",
        "repo": "Happ-proxy/happ-android",
        "asset_pattern": r".*\.apk$",
        "website": "https://github.com/Happ-proxy/happ-android"
    },
    {
        "id": "husi",
        "name": "Husi",
        "desc": "یکپارچه‌سازی غیرحرفه‌ای و تفریحی ابزارهای پروکسی",
        "platform": "Android",
        "repo": "xchacha20-poly1305/husi",
        "asset_pattern": r".*\.apk$",
        "website": "https://github.com/xchacha20-poly1305/husi"
    }
]

OUTPUT_FILE = "vpn_clients_data.json"

# =============================================================================
# توابع کمکی
# =============================================================================

def fetch_latest_release(repo_full):
    url = f"https://api.github.com/repos/{repo_full}/releases/latest"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 404:
            return None
        if not resp.ok:
            return None
        return resp.json()
    except:
        return None

def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} بایت"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} کیلوبایت"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} مگابایت"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} گیگابایت"

def parse_date(date_str):
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return date_str

def matches_pattern(filename, pattern):
    if pattern is None:
        return True
    return re.search(pattern, filename, re.IGNORECASE) is not None

# =============================================================================
# اجرای اصلی
# =============================================================================

def main():
    print(f"تعداد کلاینت‌ها: {len(VPN_CLIENTS)}")
    all_clients = []
    successful = 0
    failed = 0

    for client in VPN_CLIENTS:
        print(f"دریافت {client['name']} ... ", end="")
        release = fetch_latest_release(client['repo'])
        if not release:
            print("ناموفق")
            failed += 1
            continue

        tag = release.get('tag_name', 'N/A')
        name = release.get('name', tag)
        date = release.get('published_at', 'N/A')
        url = release.get('html_url', '')
        body = release.get('body', '')[:500]
        assets = []
        for a in release.get('assets', []):
            if matches_pattern(a['name'], client['asset_pattern']):
                assets.append({
                    "filename": a['name'],
                    "size": a['size'],
                    "size_formatted": format_size(a['size']),
                    "download_url": a['browser_download_url'],
                    "downloads": a['download_count']
                })

        all_clients.append({
            "id": client['id'],
            "name": client['name'],
            "desc": client['desc'],
            "platform": client['platform'],
            "repo": client['repo'],
            "website": client['website'],
            "latest_version": {
                "tag": tag,
                "name": name,
                "release_date_raw": date,
                "release_date": parse_date(date),
                "release_url": url,
                "changelog_preview": body,
                "assets": assets
            }
        })
        print(f"نسخه {tag} - {len(assets)} فایل")
        successful += 1

    output = {
        "meta": {
            "generated_at_utc": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            "generator": "VPN Clients Link Collector v2.0",
            "total_clients": len(VPN_CLIENTS),
            "successful": successful,
            "failed": failed,
        },
        "clients": all_clients
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"\n✅ تمام شد. {successful} موفق، {failed} ناموفق. خروجی: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
