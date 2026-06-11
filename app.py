from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    # 1. لیست تمام جاهایی که ممکنه IP توش باشه رو چک می‌کنیم
    # رندر معمولاً IP واقعی رو توی X-Forwarded-For می‌ذاره
    headers = request.headers
    
    x_forwarded_for = headers.get('X-Forwarded-For')
    if x_forwarded_for:
        # اولین IP در لیست معمولاً IP اصلی کاربره
        real_ip = x_forwarded_for.split(',')[0].strip()
    else:
        # اگه اون نبود، اینا رو چک کن
        real_ip = headers.get('CF-Connecting-IP') or \
                  headers.get('X-Real-IP') or \
                  request.remote_addr

    # 2. نمایش مستقیم در صفحه سایت
    return f"""
    <html>
        <head><title>IP Checker for Younes</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h1 style="color: #ff4757;">سلام یونس!</h1>
            <h2 style="background: #f1f2f6; padding: 20px; display: inline-block; border-radius: 10px;">
                Your Real IP: <span style="color: blue;">{real_ip}</span>
            </h2>
            <p style="margin-top: 20px; color: #7f8c8d;">
                Internal Remote Addr (Just for Debug): {request.remote_addr}
            </p>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
