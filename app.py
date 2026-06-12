# app.py

import re
from flask import Flask, render_template_string, request
from user_agents import parse
import time # برای شبیه‌سازی تاخیر

app = Flask(__name__)

# قالب HTML با تمام جزئیات و انیمیشن‌ها - بدون باکس اطلاعات کاربر
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>شبیه‌ساز هکری یونس</title> <!-- عنوان صفحه تغییر کرد -->
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
            flex-direction: column; /* چیدمان عمودی */
            padding: 20px;
            box-sizing: border-box;
        }
        .container {
            /* چون info-box حذف شده، container دیگه نیازی به flex-direction column نداره
               اما برای اطمینان نگهش می‌داریم */
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            max-width: 900px; /* عرض کلی صفحه */
        }
        /* .info-box حذف شده */

        /* استایل ترمینال */
        .terminal {
            width: 90%;
            max-width: 850px;
            height: 500px; /* کمی ارتفاع ترمینال را بیشتر کردیم تا جا داشته باشد */
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
        <!-- .info-box حذف شده -->

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
                if (type !== 'error') { // افکت تایپ برای همه به جز خطا (یا اگر خواستید خطا هم داشته باشه)
                    p.innerHTML = '<span class="typing-effect">' + text + '</span>';
                } else {
                    p.textContent = text; // برای خطا، فقط متن رو قرار بده
                }
                terminal.appendChild(p);
                // اسکرول خودکار به پایین
                terminal.scrollTop = terminal.scrollHeight;
            }, delay * 1000); // تاخیر بر حسب ثانیه
        }

        // شبیه‌سازی بارگذاری و اسکن
        setTimeout(() => { addTerminalLine("شروع اسکن پورت بر روی webserver-01 (10.0.0.10)..."); }, 3500);
        setTimeout(() => { addTerminalLine("پورت 80 (HTTP) باز است.", 'output'); }, 5000);
        setTimeout(() => { addTerminalLine("پورت 443 (HTTPS) باز است.", 'output'); }, 6000);
        setTimeout(() => { addTerminalLine("تلاش برای یافتن آسیب‌پذیری در وب‌سرور...", 'info-msg'); }, 7000);
        setTimeout(() => { addTerminalLine("آسیب‌پذیری SMB در دستگاه file-server (10.0.0.20) شناسایی شد!", 'highlight'); }, 8500);
        setTimeout(() => { addTerminalLine("تلاش برای دسترسی به سیستم فایل...", 'info-msg'); }, 9500);
        setTimeout(() => { addTerminalLine("دسترسی به فایل‌های حساس برقرار شد!", 'highlight'); }, 11000);
        setTimeout(() => { addTerminalLine("انتقال داده‌ها آغاز شد...", 'output'); }, 12000);
        setTimeout(() => { addTerminalLine("فایروال شبکه شناسایی شد. در حال تلاش برای دور زدن...", 'info-msg'); }, 13000);
        setTimeout(() => { addTerminalLine("اتصال ناامن شناسایی شد! ممکن است ترافیک شما شنود شود.", 'error'); }, 14500);

        // <<< پیام نهایی موفقیت >>>
        setTimeout(() => {
            addTerminalLine(">>>>>> نفوذ با موفقیت انجام شد! <<<<<<", 'highlight');
        }, 16000); // زمان نمایش پیام موفقیت

        // پیام پایانی برای بستن ترمینال
        setTimeout(() => {
            addTerminalLine("اتصال قطع شد. خروج از سیستم...", 'info-msg');
        }, 18000); // بعد از پیام موفقیت

    </script>
</body>
</html>
"""

@app.route('/')
def index():
    # این بخش اطلاعات کاربر رو میگیره ولی چون info-box حذف شده، دیگه نمایش داده نمیشه
    # اما برای عملکرد صحیح Flask لازمه
    ip_header = request.headers.get('X-Forwarded-For')
    if ip_header:
        ip = ip_header.split(',')[0].strip()
    else:
        ip = request.remote_addr
    ua_string = request.headers.get('User-Agent', '')
    user_agent = parse(ua_string)

    # استخراج مدل دستگاه با هوشمندی بیشتر
    device_model = user_agent.device.model
    if not device_model or "Generic" in device_model or device_model == "K":
        match = re.search(r'\(Linux; Android [^;]+; ([^;)]+)', ua_string)
        if match:
            device_model = match.group(1).replace('_', ' ')
        else:
            device_model = "دستگاه اندروید ناشناس"

    os_info = f"{user_agent.os.family} {user_agent.os.version_string}"
    browser_info = f"{user_agent.browser.family} {user_agent.browser.version_string}"

    # تنظیم مقادیر پیش‌فرض اگر چیزی دریافت نشد
    ip = ip if ip else "نامشخص"
    device_model = device_model if device_model else "نامشخص"
    os_info = os_info if os_info.strip() else "نامشخص"
    browser_info = browser_info if browser_info.strip() else "نامشخص"


    # چون info-box حذف شده، مقادیر رو به template پاس نمیدیم مگر اینکه لازم باشه
    # فعلا فقط raw_ua رو پاس میدیم برای دیباگ احتمالی در کنسول مرورگر
    return render_template_string(HTML_TEMPLATE, raw_ua=ua_string)

# برای اجرای محلی با پورت دلخواه
if __name__ == '__main__':
    # debug=True فقط برای توسعه محلی استفاده شود
    # app.run(debug=True)

    # برای اجرای روی سرور یا Render، این خط را استفاده کنید:
    # app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)

    # اجرای محلی با پورت 8080:
    app.run(host='0.0.0.0', port=8080)
