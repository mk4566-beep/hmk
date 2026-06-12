# app.py

import re
import os
import shutil # برای کپی فایل
from flask import Flask, render_template_string, request, send_from_directory
from user_agents import parse
# import time # اگر برای شبیه‌سازی تاخیر لازم بود، اینجا کامنت شده

app = Flask(__name__)

# --- تنظیمات فایل‌ها و پوشه‌ها ---
STATIC_FOLDER = 'static' # پوشه برای فایل‌های استاتیک (CSS, JS, Images)
IMAGE_FILENAME = 'image.png' # نام فایلی که می‌خواهیم نمایش دهیم

# --- اصلاح شده: مسیر فایل اصلی در /mnt/data ---
SOURCE_IMAGE_PATH = '[/mnt/data/image.png'](https://storage.gapgpt.app/media/code_interpreter/8365ef4f-103f-4fdb-8092-524c8267676b/image.png%27) # مسیر فایل اصلی
IMAGE_PATH_IN_STATIC = os.path.join(STATIC_FOLDER, IMAGE_FILENAME) # مسیر فایل در پوشه static

# --- اطمینان از وجود پوشه static و کپی فایل ---
if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)
    print(f"پوشه '{STATIC_FOLDER}' ساخته شد.")

# کپی فایل image.png از /mnt/data به پوشه static اگر وجود دارد و در مقصد نیست
if os.path.exists(SOURCE_IMAGE_PATH) and not os.path.exists(IMAGE_PATH_IN_STATIC):
    try:
        shutil.copyfile(SOURCE_IMAGE_PATH, IMAGE_PATH_IN_STATIC)
        print(f"فایل '{IMAGE_FILENAME}' از /mnt/data به پوشه '{STATIC_FOLDER}' کپی شد.")
    except Exception as e:
        print(f"خطا در کپی فایل '{IMAGE_FILENAME}': {e}")
elif not os.path.exists(IMAGE_PATH_IN_STATIC):
    print(f"هشدار: فایل '{IMAGE_FILENAME}' در مسیر '{SOURCE_IMAGE_PATH}' یافت نشد و در پوشه '{STATIC_FOLDER}' نیز وجود ندارد.")
    print("لطفاً فایل 'image.png' را در پوشه '/mnt/data' قرار دهید یا دستی در پوشه 'static' کپی کنید.")

# --- قالب HTML ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>اسکنر امنیتی یونس</title>
    <style>
        body {
            background-color: #0a0a0a;
            color: #00ff41;
            font-family: 'Consolas', 'Monaco', 'Andale Mono', 'Ubuntu Mono', monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            overflow-x: hidden; /* جلوگیری از اسکرول افقی */
            flex-direction: column;
            padding: 20px;
            box-sizing: border-box;
        }
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            max-width: 900px;
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
            margin-bottom: 30px;
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
            height: 400px;
            background-color: #000;
            border: 2px solid #00ff41;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.6);
            overflow-y: scroll;
            padding: 15px;
            box-sizing: border-box;
            font-size: 14px;
            white-space: pre-wrap;
            position: relative;
        }
        .terminal::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(rgba(0, 255, 65, 0.1) 1px, transparent 1px);
            background-size: 100% 20px;
            opacity: 0.5;
            animation: blink 1s steps(1) infinite;
        }
        @keyframes blink { 50% { opacity: 0.7; } }

        .terminal p { margin: 5px 0; line-height: 1.4; }
        .command { color: #00ffff; }
        .output { color: #eee; }
        .error { color: #ff4136; }
        .info-msg { color: #ffdd57; }
        .highlight { color: #ff8533; font-weight: bold;}

        /* انیمیشن تایپ شدن */
        .typing-effect {
            display: inline-block;
            overflow: hidden;
            white-space: nowrap;
            margin: 0 auto;
            letter-spacing: .1em;
            animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite;
        }
        @keyframes typing { from { width: 0 } to { width: 100% } }
        @keyframes blink-caret { from, to { color: transparent } 50% { color: #00ff41; } }

        /* استایل جدید برای بخش عکس */
        .image-container {
            margin-top: 30px;
            text-align: center;
            border: 1px dashed #005f21;
            padding: 15px;
            border-radius: 8px;
            background: rgba(0, 100, 30, 0.1);
            width: 90%;
            max-width: 450px; /* تنظیم عرض برای هماهنگی با info-box */
        }
        .image-container img {
            display: block;
            max-width: 100%;
            height: auto;
            border: 2px solid #00ff41;
            border-radius: 8px;
            margin-top: 10px;
            box-shadow: 0 0 10px rgba(0, 255, 65, 0.4);
        }
        .image-container a {
            color: #00ffff;
            text-decoration: underline;
            font-size: 0.9em;
            display: block; /* برای اینکه زیر عکس نمایش داده شود */
            margin-top: 10px;
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

        <!-- نمایش عکس -->
        {% if image_url %}
        <div class="image-container">
            <p class="info-msg typing-effect" style="animation-delay: 0s; width: auto;">تصویر نمایشی:</p>
            <a href="{{ image_url }}" target="_blank">
                مشاهده عکس اصلی
            </a>
            <img src="{{ image_url }}" alt="نمایش عکس">
        </div>
        {% endif %}

        <div class="terminal">
            <p class="info-msg typing-effect" style="animation-delay: 0s;">در حال بارگذاری سیستم اسکن امنیتی...</p>
            <p class="info-msg typing-effect" style="animation-delay: 1.5s;">تلاش برای اتصال به شبکه فرضی...</p>
            <p class="output typing-effect" style="animation-delay: 2.5s;">شبکه فرضی شناسایی شد: 10.0.0.0/8</p>
            <p class="output typing-effect" style="animation-delay: 3.5s;">در حال اسکن دستگاه‌ها...</p>
            <p class="output typing-effect" style="animation-delay: 4.5s;">شروع اسکن پورت بر روی webserver-01 (10.0.0.10)...</p>
            <p class="output typing-effect" style="animation-delay: 6.0s;">پورت 80 (HTTP) باز است.</p>
            <p class="output typing-effect" style="animation-delay: 7.0s;">پورت 443 (HTTPS) باز است.</p>
            <p class="info-msg typing-effect" style="animation-delay: 8.0s;">تلاش برای یافتن آسیب‌پذیری در وب‌سرور...</p>
            <p class="highlight typing-effect" style="animation-delay: 9.5s;">آسیب‌پذیری SMB در دستگاه file-server (10.0.0.20) شناسایی شد!</p>
            <p class="info-msg typing-effect" style="animation-delay: 11.0s;">تلاش برای دسترسی به سیستم فایل...</p>
            <p class="highlight typing-effect" style="animation-delay: 12.5s;">دسترسی به فایل‌های حساس برقرار شد!</p>
            <p class="output typing-effect" style="animation-delay: 13.5s;">انتقال داده‌ها آغاز شد...</p>
            <p class="info-msg typing-effect" style="animation-delay: 14.5s;">فایروال شبکه شناسایی شد. در حال تلاش برای دور زدن...</p>
            <p class="error typing-effect" style="animation-delay: 16.0s;">اتصال ناامن شناسایی شد! ممکن است ترافیک شما شنود شود.</p>
            <p class="highlight typing-effect" style="animation-delay: 17.5s;">>>>>>> نفوذ با موفقیت انجام شد! <<<<<<</p>
            <p class="info-msg typing-effect" style="animation-delay: 19.0s;">اتصال قطع شد. خروج از سیستم...</p>
        </div>
    </div>

    <script>
        // تابع کمکی برای اضافه کردن خطوط با افکت تایپ
        function addTerminalLine(text, type = 'output', delay = 0, elementId = null) {
            const terminal = document.querySelector('.terminal');
            // اگر المنت خاصی برای نمایش متن در نظر گرفته شده، از آن استفاده کن
            const targetElement = elementId ? document.getElementById(elementId) : terminal;

            setTimeout(() => {
                const p = document.createElement('p');
                p.className = type;
                p.textContent = text;

                // برای افکت تایپ، متن را درون یک span قرار می‌دهیم
                if (type !== 'error' && type !== 'info-msg' && type !== 'highlight') {
                    p.innerHTML = '<span class="typing-effect">' + text + '</span>';
                } else if (type === 'info-msg' || type === 'highlight') {
                     // برای info-msg و highlight هم افکت تایپ را نگه می‌داریم
                     p.innerHTML = '<span class="typing-effect">' + text + '</span>';
                }
                // برای error، افکت تایپ لازم نیست مگر اینکه بخواهیم

                // اگر المنت والد مشخص شده باشد، اضافه کردن به آن المنت
                // در غیر این صورت به ترمینال اضافه می‌شود
                if (elementId) {
                    targetElement.appendChild(p);
                } else {
                    terminal.appendChild(p);
                }
                terminal.scrollTop = terminal.scrollHeight; // اسکرول خودکار
            }, delay * 1000);
        }

        // انیمیشن خطوط ترمینال - زمان‌بندی‌ها برای هر خط
        // (اینها در HTML Template با animation-delay تنظیم شده‌اند، اما تابع addTerminalLine هم می‌تواند استفاده شود)

        // تنظیم انیمیشن تایپ شدن برای خطوط مختلف
        // این کار را به صورت دستی در HTML با animation-delay انجام دادیم که کنترل بیشتری دارد.
        // اگر خواستید از تابع addTerminalLine برای این خطوط استفاده کنید، باید delay ها را تنظیم کنید.
        // مثال:
        // addTerminalLine("در حال بارگذاری سیستم اسکن امنیتی...", 'info-msg', 0);
        // addTerminalLine("تلاش برای اتصال به شبکه فرضی...", 'info-msg', 1.5);

    </script>
</body>
</html>
"""

@app.route('/')
def index():
    # گرفتن IP با در نظر گرفتن پروکسی‌ها
    ip_header = request.headers.get('X-Forwarded-For')
    if ip_header:
        ip = ip_header.split(',')[0].strip()
    else:
        ip = request.remote_addr

    ua_string = request.headers.get('User-Agent', '')
    user_agent = parse(ua_string)

    # استخراج مدل دستگاه با هوشمندی بیشتر
    device_model = user_agent.device.model
    # اگر مدل خالی بود یا "Generic" یا "K" بود، سعی کن از UA خام استخراج کنی
    if not device_model or "Generic" in device_model or device_model == "K":
        match = re.search(r'\(Linux; Android [^;]+; ([^;)]+)', ua_string)
        if match:
            device_model = match.group(1).replace('_', ' ') # جایگزینی آندر اسکور با فاصله
        else:
            # اگر باز هم پیدا نشد، یک پیام عمومی فارسی
            device_model = "دستگاه اندروید ناشناس"

    # اطلاعات سیستم عامل و مرورگر
    os_info = f"{user_agent.os.family} {user_agent.os.version_string}"
    browser_info = f"{user_agent.browser.family} {user_agent.browser.version_string}"

    # اگر IP یا UA خالی بود، پیام مناسب بده
    if not ip: ip = "نامشخص"
    if not device_model: device_model = "نامشخص"
    if not os_info or os_info.strip() == "": os_info = "نامشخص"
    if not browser_info or browser_info.strip() == "": browser_info = "نامشخص"

    # ساخت URL برای نمایش عکس
    # اگر فایل image.png در پوشه static باشد، این URL کار می‌کند
    image_url = None
    if os.path.exists(IMAGE_PATH_IN_STATIC):
        image_url = f"/serve_image/{IMAGE_FILENAME}"
    else:
        print(f"هشدار: فایل '{IMAGE_FILENAME}' برای سرو کردن پیدا نشد.")


    return render_template_string(HTML_TEMPLATE, ip=ip, device=device_model, os=os_info, browser=browser_info, raw_ua=ua_string, image_url=image_url)

@app.route('/serve_image/<filename>')
def serve_image(filename):
    # این تابع اجازه می‌دهد فایل‌ها از پوشه static سرو شوند
    try:
        # اطمینان از اینکه فقط فایل‌های داخل پوشه static قابل دسترسی هستند
        if filename == IMAGE_FILENAME and os.path.exists(IMAGE_PATH_IN_STATIC):
            return send_from_directory(STATIC_FOLDER, filename)
        else:
            return "دسترسی مجاز نیست یا فایل یافت نشد!", 403
    except FileNotFoundError:
        return "فایل مورد نظر یافت نشد!", 404
    except Exception as e:
        print(f"خطا در سرو کردن فایل '{filename}': {e}")
        return "خطای داخلی سرور!", 500


if __name__ == '__main__':
    # اجرای برنامه
    # debug=True برای توسعه محلی بسیار مفید است تا تغییرات را سریعتر ببینید.
    # در محیط production (مثل Render) باید debug=False باشد.
    # این بخش را برای دیپلوی روی پلتفرم‌هایی مثل Render باید اصلاح کنید تا از متغیر محیطی PORT استفاده کند:
    # port = int(os.environ.get('PORT', 8080))
    # app.run(host='0.0.0.0', port=port, debug=False) # debug=False برای production

    # اجرای محلی با debug=True (پیش‌فرض):
    app.run(host='0.0.0.0', port=8080, debug=True)
