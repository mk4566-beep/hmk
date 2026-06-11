from flask import Flask, request
from datetime import datetime

try:
    from user_agents import parse
except ImportError:
    parse = None

app = Flask(__name__)

@app.route('/')
def index():
    # زمان دقیق
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # گرفتن IP واقعی کاربر
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        ip = forwarded_for.split(',')[0].strip()
    else:
        ip = request.remote_addr

    # گرفتن User-Agent
    ua_string = request.headers.get('User-Agent', 'Unknown')

    # مقادیر پیش‌فرض
    device = "Unknown Device"
    browser = "Unknown Browser"

    # اگر کتابخانه نصب بود، اطلاعات دقیق‌تر بده
    if parse:
        ua = parse(ua_string)
        device = f"{ua.device.family} / {ua.os.family} {ua.os.version_string}".strip()
        browser = f"{ua.browser.family} {ua.browser.version_string}".strip()
    else:
        browser = ua_string

    # لاگ در کنسول Render
    print("\n" + "=" * 40)
    print(f"🚀 TARGET SPOTTED AT: {now}")
    print(f"🌐 REAL IP: {ip}")
    print(f"📱 DEVICE: {device}")
    print(f"🌍 BROWSER: {browser}")
    print("=" * 40 + "\n")

    # پاسخ ساده برای جلوگیری از صفحه سفید
    return "System Status: Online"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
