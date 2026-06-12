from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>System Info</title>
    <style>
        body {
            background-color: black;
            color: lime;
            font-family: monospace;
            padding: 40px;
        }
        .box {
            border: 1px solid lime;
            padding: 20px;
            width: 500px;
        }
    </style>
</head>
<body>
    <div class="box">
        <h2>Device Information</h2>
        <p><strong>IP Address:</strong> {{ ip }}</p>
        <p><strong>Device Type:</strong> {{ device }}</p>
        <p><strong>Browser:</strong> {{ browser }}</p>
        <p><strong>Operating System:</strong> {{ os }}</p>
    </div>
</body>
</html>
"""

def get_real_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        return response.json()["ip"]
    except:
        return "Unknown"

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')

    # تشخیص ساده دستگاه
    if "Mobile" in user_agent:
        device = "Mobile"
    else:
        device = "Desktop"

    # تشخیص مرورگر
    if "Chrome" in user_agent:
        browser = "Google Chrome"
    elif "Firefox" in user_agent:
        browser = "Mozilla Firefox"
    elif "Safari" in user_agent:
        browser = "Safari"
    else:
        browser = "Unknown Browser"

    # تشخیص سیستم عامل
    if "Windows" in user_agent:
        os_name = "Windows"
    elif "Linux" in user_agent:
        os_name = "Linux"
    elif "Mac" in user_agent:
        os_name = "MacOS"
    else:
        os_name = "Unknown OS"

    ip = request.remote_addr

    return render_template_string(
        HTML_TEMPLATE,
        ip=ip,
        device=device,
        browser=browser,
        os=os_name
    )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
