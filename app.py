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
    <title>وضعیت سیستم یونس</title>
    <style>
        body { background-color: #0d0d0d; color: #00ff41; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { border: 2px solid #00ff41; padding: 30px; border-radius: 15px; box-shadow: 0 0 20px #00ff41; text-align: center; width: 90%; max-width: 400px; background: rgba(0, 255, 65, 0.05); }
        h1 { color: #fff; text-shadow: 0 0 10px #00ff41; margin-bottom: 30px; font-size: 24px; }
        .info { margin: 20px 0; border-bottom: 1px solid #333; padding-bottom: 10px; }
        .label { display: block; font-size: 0.8em; color: #888; margin-bottom: 5px; }
        .value { font-size: 1.2em; font-weight: bold; color: #00ff41; word-break: break-all; }
        .footer { margin-top: 20px; font-size: 0.7em; color: #444; }
    </style>
</head>
<body>
    <div class="container">
        <h1>وضعیت سیستم</h1>
        
        <div class="info">
            <span class="label">آی‌پی شما:</span>
            <span class="value">{{ ip }}</span>
        </div>

        <div class="info">
            <span class="label">مدل دستگاه:</span>
            <span class="value">{{ device }}</span>
        </div>

        <div class="info">
            <span class="label">سیستم عامل:</span>
            <span class="value">{{ os }}</span>
        </div>

        <div class="info">
            <span class="label">مرورگر:</span>
            <span class="value">{{ browser }}</span>
        </div>

        <div class="footer">طراحی شده برای یونس</div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    # گرفتن آی‌پی واقعی پشت پروکسی رندر
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    
    ua_string = request.headers.get('User-Agent', '')
    user_agent = parse(ua_string)

    # استخراج هوشمند مدل دستگاه
    device_model = user_agent.device.model
    
    # اگر مدل پیدا نشد یا Generic بود، با Regex دنبال کد مدل بگرد
    if not device_model or "Generic" in device_model or device_model == "K":
        # جستجو برای کدهایی مثل SM-A725F یا کلمات مدل در پرانتز
        match = re.search(r'\(([^;]+);[^;]+; ([^;)]+)', ua_string)
        if match:
            device_model = match.group(2)
        else:
            # تلاش ثانویه برای پیدا کردن کدهای سامسونگ
            sm_match = re.search(r'(SM-[A-Z0-9]+)', ua_string)
            if sm_match:
                device_model = sm_match.group(1)

    device_brand = user_agent.device.brand if user_agent.device.brand else ""
    full_device = f"{device_brand} {device_model}".strip() or "نامشخص"
    
    os_info = f"{user_agent.os.family} {user_agent.os.version_string}"
    browser_info = f"{user_agent.browser.family} {user_agent.browser.version_string}"

    return render_template_string(HTML_TEMPLATE, ip=ip, device=full_device, os=os_info, browser=browser_info)

# توجه: دستور app.run حذف شد تا تداخلی با Gunicorn نداشته باشد.
