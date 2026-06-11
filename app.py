from flask import Flask, request
import sys

app = Flask(__name__)

@app.route('/')
def index():
    # ۱. استخراج IP واقعی از هدر پروکسی رندر
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        real_ip = forwarded_for.split(',')[0].strip()
    else:
        real_ip = request.remote_addr

    # ۲. چاپ IP واقعی در لاگ‌های رندر (با فلش که سریع نشون داده بشه)
    # این خط باعث میشه توی کنسول سیاه رنگ رندر، IP واقعی رو ببینی
    print(f"--- REAL USER CONNECTED: {real_ip} ---", file=sys.stdout, flush=True)

    # ۳. ظاهر ساده و شیک برای صفحه (بدون هیچ اسم و متن اضافه)
    return f"""
    <html>
        <head>
            <title>Status</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body style="font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f8f9fa;">
            <div style="background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: center;">
                <div style="color: #6c757d; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">Your IP Address</div>
                <div style="font-size: 28px; font-weight: 800; color: #212529;">{real_ip}</div>
                <div style="margin-top: 20px; color: #28a745; font-size: 13px; font-weight: bold;">● System Live</div>
            </div>
        </body>
    </html>
    """

if __name__ == '__main__':
    # اجرای مستقیم برای دیباگ یا محیط لوکال
    app.run(host='0.0.0.0', port=10000)
