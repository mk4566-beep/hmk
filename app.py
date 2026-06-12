from flask import Flask, request, render_template_string
from user_agents import parse
import re

app = Flask(__name__)

# این همون ظاهر سایتته که ریختمش داخل یک متغیر که نیازی به فایل اضافه نباشه
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>پنل هوشمند یونس</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background: #0a0a0a; color: #00ff41; text-align: center; padding-top: 50px; }
        .box { border: 2px solid #00ff41; background: #111; display: inline-block; padding: 30px; border-radius: 20px; box-shadow: 0 0 30px #00ff4144; border-style: double; }
        h1 { color: #fff; text-shadow: 2px 2px #ff0000; }
        .data { font-size: 1.2rem; margin: 15px 0; border-bottom: 1px solid #222; padding-bottom: 8px; }
        span { color: #00fbff; font-weight: bold; }
        .js-box { color: #ffca28; margin-top: 20px; font-family: monospace; border: 1px dashed #555; padding: 10px; }
    </style>
</head>
<body>
    <div class="box">
        <h1>🕵️‍♂️ سیستم جاسوسی یونس!</h1>
        <div class="data">🌐 آی‌پی واقعی شما: <span>{{ ip }}</span></div>
        <div class="data">📱 مدل شناسایی شده: <span>{{ device }}</span></div>
        <div class="data">💻 سیستم عامل: <span>{{ os }}</span></div>
        <div class="data">🌍 مرورگر: <span>{{ browser }}</span></div>
        
        <div class="js-box" id="js-extra">
            در حال آنالیز سخت‌افزار...
        </div>
    </div>

    <script>
        // مچ‌گیری از کسایی که با کامپیوتر میان ولی ادای گوشی رو در میارن
        const jsExtra = document.getElementById('js-extra');
        const isTouch = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);
        const screenRes = window.screen.width + "x" + window.screen.height;
        
        jsExtra.innerHTML = "🛠 اطلاعات سخت‌افزاری:<br>" +
                           "رزولوشن نمایشگر: " + screenRes + "<br>" +
                           (isTouch ? "✅ تایید فنی: صفحه لمسی (موبایل)" : "❌ تایید فنی: ماوس و کیبورد (دسکتاپ)");
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    # پیدا کردن آی‌پی واقعی
    ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip_addr and ',' in ip_addr:
        ip_addr = ip_addr.split(',')[0]

    # تحلیل مشخصات دستگاه
    ua_string = request.headers.get('User-Agent', '')
    user_agent = parse(ua_string)
    
    brand = user_agent.device.brand if user_agent.device.brand else ""
    model = user_agent.device.model if user_agent.device.model else ""
    
    # مچ‌گیری از مدل‌های سامسونگ مثل گوشی تو (A72)
    if not model or model == 'Generic Smartphone':
        match = re.search(r'\(([^;]+); ([^;]+); ([^\)]+)\)', ua_string)
        if match:
            model = match.group(3).split('Build')[0].strip()

    device_info = f"{brand} {model}".strip() if (brand or model) else "ناشناس"
    os_info = f"{user_agent.os.family} {user_agent.os.version_string}"
    browser_info = f"{user_agent.browser.family} {user_agent.browser.version_string}"

    # ارسال مستقیم کد HTML به مرورگر
    return render_template_string(HTML_TEMPLATE, 
                                 ip=ip_addr, 
                                 device=device_info, 
                                 os=os_info, 
                                 browser=browser_info)

# اینم برای اینکه رندر نگه کد زود بسته شد
if __name__ == "__main__":
    app.run()
