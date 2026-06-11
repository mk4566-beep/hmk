from flask import Flask, request
import sys

app = Flask(__name__)

@app.route('/')
def index():
    # ۱. استخراج IP واقعی
    headers = request.headers
    x_forwarded_for = headers.get('X-Forwarded-For')
    
    if x_forwarded_for:
        real_ip = x_forwarded_for.split(',')[0].strip()
    else:
        real_ip = request.remote_addr

    # ۲. چاپ کردن در لاگ به صورت دستی (این رو حتماً توی لاگ خواهی دید)
    # ما از flush=True استفاده می‌کنیم که رندر سریع نشونش بده
    print(f">>> NEW VISITOR | REAL IP: {real_ip} | UA: {request.headers.get('User-Agent')}", file=sys.stderr, flush=True)

    # ۳. نمایش در صفحه (همون ظاهر شیکی که پسندیدی)
    return f"""
    <html>
        <body style="font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f0f2f5;">
            <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
                <h3 style="color: #65676b; margin-bottom: 10px;">Connection Info</h3>
                <div style="font-size: 1.5rem; font-weight: bold; color: #1c1e21;">{real_ip}</div>
                <div style="margin-top: 15px; font-size: 0.8rem; color: #8a8d91;">Status: Verified</div>
            </div>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
