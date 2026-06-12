from flask import Flask, request, render_template_string
from user_agents import parse
import re

app = Flask(__name__)

# قالب نئونی و خفن برای داشبورد یونس
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>داشبورد شناسایی یونس</title>
    <style>
        body { background-color: #0a0a0a; color: #00ff99; font-family: Tahoma, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: #1a1a1a; padding: 2rem; border-radius: 15px; border: 1px solid #00ff99; box-shadow: 0 0 20px rgba(0, 255, 153, 0.2); width: 300px; }
        h2 { text-align: center; color: #fff; text-shadow: 0 0 10px #00ff99; }
        .info { margin-bottom: 1rem; border-bottom: 1px solid #333; padding-bottom: 5px; }
        .label { color: #888; font-size: 0.8rem; }
        .value { font-weight: bold; font-size: 1.1rem; display: block; }
    </style>
</head>
<body>
    <div class="card">
        <h2>وضعیت سیستم</h2>
        <div class="info"><span class="label">آی‌پی شما:</span> <span class="value">{{ ip }}</span></div>
        <div class="info"><span class="label">مدل دستگاه:</span> <span class="value">{{ device }}</span></div>
        <div class="info"><span class="label">سیستم عامل:</span> <span class="value">{{ os }}</span></div>
        <div class="info"><span class="label">مرورگر:</span> <span class="value">{{ browser }}</span></div>
        <p style="font-size: 10px; text-align: center; color: #444;">طراحی شده برای یونس</p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    # پیدا کردن آی‌پی واقعی (حتی پشت VPN)
    ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip_addr and ',' in ip_addr:
        ip_addr = ip_addr.split(',')[0]

    # تحلیل مشخصات دستگاه
    ua_string = request.headers.get('User-Agent', '')
    user_agent = parse(ua_string)

    brand = user_agent.device.brand if user_agent.device.brand else ""
    model = user_agent.device.model if user_agent.device.model else ""

    # مچ‌گیری از مدل‌های سامسونگ (مثل A72 تو) اگه User-Agent ناقص بود
    if not model or model == 'Generic Smartphone':
        match = re.search(r'\(([^;]+); ([^;]+); ([^\)]+)\)', ua_string)
        if match:
            model = match.group(3).split('Build')[0].strip()

    device_info = f"{brand} {model}".strip() if (brand or model) else "ناشناس"
    os_info = f"{user_agent.os.family} {user_agent.os.version_string}"
    browser_info = f"{user_agent.browser.family} {user_agent.browser.version_string}"

    return render_template_string(HTML_TEMPLATE, ip=ip_addr, device=device_info, os=os_info, browser=browser_info)

# دقت کن یونس: اینجا دیگه app.run() نداریم! گانیکورن خودش ردیفش می‌کنه.
