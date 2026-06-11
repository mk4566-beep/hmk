from flask import Flask, request
import re
from datetime import datetime

app = Flask(__name__)

# فانکشن برای استخراج مدل دستگاه
def get_device_model(user_agent):
    if 'Samsung' in user_agent:
        return 'Samsung'
    elif 'iPhone' in user_agent:
        return 'iPhone'
    elif 'Xiaomi' in user_agent:
        return 'Xiaomi'
    else:
        return 'Other'

# فانکشن برای استخراج نوع مرورگر
def get_browser_type(user_agent):
    browsers = {
        'Chrome': 'Google Chrome',
        'Firefox': 'Mozilla Firefox',
        'Safari': 'Apple Safari',
        'Edge': 'Microsoft Edge',
        'Opera': 'Opera',
        'IE': 'Internet Explorer'
    }
    for key, value in browsers.items():
        if key in user_agent:
            return value
    return 'Other Browser'

@app.route('/')
def index():
    # گرفتن آی‌پی کاربر
    remote_ip = request.remote_addr

    # گرفتن اطلاعات مرورگر (User-Agent)
    user_agent_string = request.headers.get('User-Agent', 'Unknown')

    # استخراج مدل دستگاه و نوع مرورگر
    device_model = get_device_model(user_agent_string)
    browser_type = get_browser_type(user_agent_string)

    # زمان فعلی برای ثبت در لاگ
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # ساختن پیام لاگ
    log_message = f"[{current_time}] IP: {remote_ip}, Device: {device_model}, Browser: {browser_type}\n"

    # --- تغییرات اعمال شده ---
    # لاگ رو به جای فایل، توی کنسول چاپ می‌کنیم
    print(log_message)

    # فقط پیام موفقیت رو برمی‌گردونیم
    return f"Hello! Your info has been logged. IP: {remote_ip}, Device: {device_model}, Browser: {browser_type}"
    # --- پایان تغییرات ---

if __name__ == '__main__':
    # برای اینکه بتونیم از بیرون هم بهش دسترسی داشته باشیم، روی 0.0.0.0 اجرا می‌کنیم
    # و پورت رو 5000 می‌ذاریم
    app.run(host='0.0.0.0', port=5000)
