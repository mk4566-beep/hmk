from flask import Flask, render_template, request
from user_agents import parse

app = Flask(__name__)

@app.get('/')
def index():
    # گرفتن IP واقعی پشت پروکسی رندر
    ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ',' in ip_addr:
        ip_addr = ip_addr.split(',')[0]

    # تحلیل مشخصات دستگاه
    ua_string = request.headers.get('User-Agent')
    user_agent = parse(ua_string)
    
    # استخراج مدل گوشی با دقت بیشتر
    brand = user_agent.device.brand if user_agent.device.brand else ""
    model = user_agent.device.model if user_agent.device.model else ""
    
    # اگه مدل رو پیدا نکرد، سعی میکنیم از متن خام درش بیاریم
    if not model or model == 'Generic Smartphone':
        import re
        # دنبال الگوهایی مثل SM-A725F در متن می‌گرده
        match = re.search(r'\(([^;]+); ([^;]+); ([^\)]+)\)', ua_string)
        if match:
            model = match.group(3).split('Build')[0].strip()

    device_info = f"{brand} {model}".strip() if (brand or model) else "کامپیوتر یا دستگاه نامشخص"
    
    os_info = f"{user_agent.os.family} {user_agent.os.version_string}"
    browser_info = f"{user_agent.browser.family} {user_agent.browser.version_string}"

    return render_template('index.html', 
                           ip=ip_addr, 
                           device=device_info, 
                           os=os_info, 
                           browser=browser_info)

# برای اجرا در رندر نیازی به app.run نیست، گانیکورن خودش مدیریت میکنه
