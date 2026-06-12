# app.py (تغییرات لازم رو اعمال می‌کنیم)

import re
from flask import Flask, render_template_string, request
from user_agents import parse
import time # برای شبیه‌سازی تاخیر

app = Flask(__name__)

# قالب HTML رو گسترش میدیم
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>اسکنر امنیتی یونس</title>
    <style>
        body {
            background-color: #0a0a0a; /* زمینه تیره‌تر */
            color: #00ff41; /* سبز نئونی */
            font-family: 'Consolas', 'Monaco', 'Andale Mono', 'Ubuntu Mono', monospace; /* فونت ترمینالی */
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh; /* حداقل ارتفاع صفحه */
            margin: 0;
            overflow: hidden; /* جلوگیری از اسکرول ناخواسته */
            flex-direction: column; /* چیدمان عمودی برای اطلاعات و ترمینال */
            padding: 20px;
            box-sizing: border-box;
        }
        .container {
            display: flex;
            flex-direction: column; /* اول اطلاعات، بعد ترمینال */
            align-items: center;
            width: 100%;
            max-width: 900px; /* عرض کلی صفحه */
        }
        .info-box {
            border: 2px solid #00ff41;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.5);
            text-align: center;
            width: 90%;
            max-width: 450px;
            background: rgba(0, 255, 65, 0.03);
            margin-bottom: 30px; /* فاصله با ترمینال */
        }
        .info-box h1 {
            color: #fff;
            text-shadow: 0 0 8px #00ff41;
            font-size: 24px;
            margin-bottom: 20px;
        }
        .info-item { margin: 12px 0; border-bottom: 1px solid #1a1a1a; padding-bottom: 6px; }
        .label { font-size: 0.7em; color: #777; display: block; margin-bottom: 2px; }
        .val { font-size: 1em; font-weight: bold; color: #00ff41; }
        .ua-debug { font-size: 0.5em; color: #444; margin-top: 15px; word-break: break-all; text-align: left; }

        /* استایل ترمینال */
        .terminal {
            width: 90%;
            max-width: 850px;
            height: 400px; /* ارتفاع ترمینال */
            background-color: #000;
            border: 2px solid #00ff41;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.6);
            overflow-y: scroll; /* اسکرول عمودی */
            padding: 15px;
            box-sizing: border-box;
            font-size: 14px;
            white-space: pre-wrap; /* حفظ فاصله و خطوط */
            position: relative; /* برای افکت ها */
        }
        .terminal::before { /* افکت سوسو زدن */
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(rgba(0, 255, 65, 0.1) 1px, transparent 1px);
            background-size: 100% 20px; /* خطوط افقی */
            opacity: 0.5;
            animation: blink 1s steps(1) infinite;
        }
        @keyframes blink { 50% { opacity: 0.7; } }

        .terminal p { margin: 5px 0; line-height: 1.4; }
        .command { color: #00ffff; } /* رنگ دستورات */
        .output { color: #eee; } /* رنگ خروجی */
        .error { color: #ff4136; } /* رنگ خطا */
        .info-msg { color: #ffdd57; } /* رنگ پیام های اطلاعاتی */
        .highlight { color: #ff8533; font-weight: bold;} /* رنگ هایلایت */

        /* انیمیشن تایپ شدن */
        .typing-effect {
            display: inline-block;
            overflow: hidden;
            white-space: nowrap;
            margin: 0 auto;
            letter-spacing: .1em;
            animation:
                typing 3.5s steps(40, end), /* تعداد steps رو تنظیم کنید */
                blink-caret .75s step-end infinite;
        }
        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }
        @keyframes blink-caret {
            from, to { color: transparent }
            50% { color: #00ff41; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="info-box">
            <h1>وضعیت سیستم یونس</h1>
            <div class="info-item"><span class="label">آی‌پی شما:</span><span class="val">{{ ip }}</span></div>
            <div class="info-item"><span class="label">مدل دستگاه:</span><span class="val">{{ device }}</span></div>
            <div class="info-item"><span class="label">سیستم عامل:</span><span class="val">{{ os }}</span></div>
            <div class="info-item"><span class="label">مرورگر:</span><span class="val">{{ browser }}</span></div>
            <div class="ua-debug">Raw UA: {{ raw_ua }}</div>
        </div>

        <div class="terminal">
            <p class="info-msg typing-effect">در حال بارگذاری سیستم اسکن امنیتی...</p>
            <p class="info-msg typing-effect">تلاش برای اتصال به شبکه فرضی...</p>
            <p class="output typing-effect" style="animation-delay: 1.5s;">شبکه فرضی شناسایی شد: 10.0.0.0/8</p>
            <p class="output typing-effect" style="animation-delay: 2.5s;">در حال اسکن دستگاه‌ها...</p>
            <!-- اینجا اطلاعات شبکه واقعی در ادامه اضافه خواهد شد -->
        </div>
    </div>

    <script>
        // تابع کمکی برای اضافه کردن خطوط با افکت تایپ
        function addTerminalLine(text, type = 'output', delay = 0) {
            const terminal = document.querySelector('.terminal');
            setTimeout(() => {
                const p = document.createElement('p');
                p.className = type;
                p.textContent = text;
                // برای افکت تایپ، باید متن رو در یک تگ span قرار بدیم
                if (type !== 'error' && type !== 'info-msg') { // افکت تایپ برای خروجی عادی
                    p.innerHTML = '<span class="typing-effect">' + text + '</span>';
                }
                terminal.appendChild(p);
                // اسکرول خودکار به پایین
                terminal.scrollTop = terminal.scrollHeight;
            }, delay * 1000); // تاخیر بر حسب ثانیه
        }

        // شبیه‌سازی بارگذاری و اسکن
        setTimeout(() => {
            addTerminalLine("شروع اسکن پورت بر روی webserver-01 (10.0.0.10)...");
        }, 3500); // بعد از پیام "در حال اسکن دستگاه‌ها..."

        setTimeout(() => {
            addTerminalLine("پورت 80 (HTTP) باز است.", 'output');
        }, 5000);

        setTimeout(() => {
            addTerminalLine("پورت 443 (HTTPS) باز است.", 'output');
        }, 6000);

        setTimeout(() => {
            addTerminalLine("تلاش برای یافتن آسیب‌پذیری در وب‌سرور...", 'info-msg');
        }, 7000);

        setTimeout(() => {
            addTerminalLine("آسیب‌پذیری SMB در دستگاه file-server (10.0.0.20) شناسایی شد!", 'highlight');
        }, 8500);

        setTimeout(() => {
            addTerminalLine("تلاش برای دسترسی به سیستم فایل...", 'info-msg');
        }, 9500);

        setTimeout(() => {
            addTerminalLine("دسترسی به فایل‌های حساس برقرار شد!", 'highlight');
        }, 11000);

        setTimeout(() => {
            addTerminalLine("انتقال داده‌ها آغاز شد...", 'output');
        }, 12000);

         setTimeout(() => {
            addTerminalLine("فایروال شبکه شناسایی شد. در حال تلاش برای دور زدن...", 'info-msg');
        }, 13000);

         setTimeout(() => {
            addTerminalLine("اتصال ناامن شناسایی شد! ممکن است ترافیک شما شنود شود.", 'error');
        }, 14500);

         setTimeout(() => {
            addTerminalLine("عملیات شبیه‌سازی اسکن و نفوذ به پایان رسید.", 'info-msg');
        }, 16000);


    </script>
</body>
</html>
"""

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    ua_string = request.headers.get('User-Agent', '')
    user_agent = parse(ua_string)

    device_model = user_agent.device.model
    if not device_model or "Generic" in device_model or device_model == "K":
        match = re.search(r'\(Linux; Android [^;]+; ([^;)]+)', ua_string)
        if match:
            device_model = match.group(1).replace('_', ' ') # جایگزینی آندر اسکور با فاصله
        else:
            device_model = "دستگاه اندروید ناشناس" # پیام فارسی

    os_info = f"{user_agent.os.family} {user_agent.os.version_string}"
    browser_info = f"{user_agent.browser.family} {user_agent.browser.version_string}"

    return render_template_string(HTML_TEMPLATE, ip=ip, device=device_model, os=os_info, browser=browser_info, raw_ua=ua_string)

if __name__ == '__main__':
    # برای اجرای محلی، دیباگ رو روشن کنید
    # app.run(debug=True)
    # برای اجرا روی Render، از gunicorn استفاده کنید
    # برای تست سریع، می‌تونید پورت رو هم مشخص کنید
    app.run(host='0.0.0.0', port=8080)
