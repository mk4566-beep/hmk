from flask import Flask, request
from user_agents import parse
import sys

app = Flask(__name__)

@app.route('/')
def index():
    # ۱. گرفتن IP واقعی (همون که پیرمون کرد تا درست شد!)
    forwarded_for = request.headers.get('X-Forwarded-For')
    real_ip = forwarded_for.split(',')[0].strip() if forwarded_for else request.remote_addr

    # ۲. تحلیل مشخصات گوشی و سیستم عامل
    ua_string = request.headers.get('User-Agent')
    user_agent = parse(ua_string)
    
    # استخراج جزئیات
    device_model = user_agent.device.model # مدل گوشی (مثلاً iPhone یا SM-G998B)
    os_info = f"{user_agent.os.family} {user_agent.os.version_string}" # سیستم عامل
    browser_info = f"{user_agent.browser.family} {user_agent.browser.version_string}" # مرورگر

    # ۳. چاپ جزئیات در لاگ رندر (برای اینکه مچ طرف رو بگیری)
    print(f"\n🎯 TARGET SPOTTED!")
    print(f"IP: {real_ip}")
    print(f"DEVICE: {device_model}")
    print(f"OS: {os_info}")
    print(f"BROWSER: {browser_info}")
    print(f"------------------------------", file=sys.stdout, flush=True)

    # ۴. ظاهر صفحه برای نمایش به خودت (یا هر کسی که لینک رو باز میکنه)
    return f"""
    <html>
        <head>
            <title>Device Info</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body style="font-family: sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; background-color: #0e1111; color: white;">
            <div style="background: #1c1c1c; padding: 30px; border-radius: 20px; border: 1px solid #333; text-align: center; width: 80%; max-width: 400px;">
                <div style="color: #00ff00; font-size: 12px; margin-bottom: 20px;">[ SYSTEM SECURE ]</div>
                <div style="margin-bottom: 20px;">
                    <div style="font-size: 14px; color: #888;">Your IP</div>
                    <div style="font-size: 22px; font-weight: bold; color: #00d4ff;">{real_ip}</div>
                </div>
                <div style="border-top: 1px solid #333; pt: 20px; padding-top: 20px;">
                    <div style="font-size: 14px; color: #888;">Detected Device</div>
                    <div style="font-size: 18px; color: #ffca28;">{os_info}</div>
                    <div style="font-size: 16px; color: #aaa; margin-top: 5px;">{device_model if device_model else "Generic PC/Device"}</div>
                </div>
            </div>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
