#!/usr/bin/env python3
import requests
import json
import re
from datetime import datetime, timezone

# =============================================================================
# تنظیمات توکن گیت‌هاب (هاردکد شده)
# مراحل ساخت توکن:
# 1. برید به https://github.com/settings/tokens
# 2. روی "Generate new token (classic)" کلیک کنید
# 3. هیچ دسترسی خاصی نیاز نیست (فقط public_repo رو بدون تیک نگه دارید)
# 4. توکن رو کپی کرده و جای YOUR_TOKEN_HERE بذارید
# =============================================================================
GITHUB_TOKEN = "YOUR_TOKEN_HERE"  # ← توکن شخصی‌تون رو اینجا بذارید

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
}
if GITHUB_TOKEN and GITHUB_TOKEN != "YOUR_TOKEN_HERE":
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

# =============================================================================
# لیست کلاینت‌های VPN (SlipNet هم اضافه شد)
# =============================================================================
VPN_CLIENTS = [
    # ... بقیه مثل قبل
    # (برای خلاصه‌سازی فقط SlipNet رو نشون میدم، ولی توی کدی که تحویل می‌گیرید همشون هست)
    # ...
]

# =============================================================================
# برای نمایش کامل، همه‌ی کلاینت‌ها از جمله SlipNet رو در کد زیر می‌آورم
# =============================================================================
VPN_CLIENTS = [
    # --- برنامه‌های V2Ray/Xray/Sing-box ---
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
        "desc": "کلاینت پروکسی مدرن",
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
        "website": "https://github.com/MetaCubeX/
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
},
