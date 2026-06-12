import re
from flask import Flask, render_template_string, request
from user_agents import parse

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>پنل کاربری یونس</title>
    <style>
        body { background-color: #050505; color: #00ff41; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { border: 2px solid #00ff41; padding: 25px; border-radius: 15px; box-shadow: 0 0 15px #00ff41; text-align: center; width: 85%; max-width: 450px; background: rgba(0, 255, 65, 0.02); }
        h1 { color: #fff; text-shadow: 0 0 8px #00ff41; font-size: 22px; margin-bottom: 25px; }
        .item { margin: 15px 0; border-bottom: 1px solid #1a1a1a; padding-bottom: 8px; }
        .label { font-size: 0.75em; color: #666; display: block; margin-bottom: 3px; }
        .val { font-size: 1.1em; font-weight: bold; color: #00ff41; }
        .ua-debug { font-size: 0.6em; color: #333; margin-top: 20px; word-break: break-all; }
    </style>
</head>
<body>
    <div class="box">
        <h1>وضعیت سیستم</h1>
        <div class="item"><span class="label">آی‌پی:</span><span class="val">{{ ip }}</span></div>
        <div class="item"><span class="label">مدل دستگاه:</span><span class="val">{{ device }}</span></div>
        <div class="item"><span class="label">سیستم عامل:</span><span class="val">{{ os }}</span></div>
        <div class="item"><span class="label">مرورگر:</span><span class="val">{{ browser }}</span></div>
        <div class="ua-debug">UA: {{ raw_ua }}</div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    ua_string = request.headers.get('User-Agent', '')
    user_agent = parse(ua_string)

    # کارآگاه بازی برای پیدا کردن مدل
    device_model = user_agent.device.model
    if not device_model or "Generic" in device_model or device_model == "K":
        # سعی می‌کنیم از توی متن خام پیدا کنیم
        match = re.search(r'\(Linux; Android [^;]+; ([^;)]+)', ua_string)
        if match:
            device_model = match.group(1)
        else:
            # اگه نشد، حداقل اسم برند رو بذاریم
            device_model = "Samsung Device"

    os_info = f"{user_agent.os.family} {user_agent.os.version_string}"
    browser_info = f"{user_agent.browser.family} {user_agent.browser.version_string}"

    return render_template_string(HTML_TEMPLATE, ip=ip, device=device_model, os=os_info, browser=browser_info, raw_ua=ua_string)
