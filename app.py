from flask import Flask, request
from user_agents import parse
import requests
import sys

app = Flask(__name__)

def get_real_ip(req):
    forwarded_for = req.headers.get('X-Forwarded-For')
    return forwarded_for.split(',')[0].strip() if forwarded_for else req.remote_addr

def get_geo_from_ip(ip):
    try:
        # ipapi.co free endpoint
        resp = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
        if resp.ok:
            data = resp.json()
            return {
                "city": data.get("city"),
                "region": data.get("region"),
                "country": data.get("country_name"),
                "org": data.get("org"),
                "timezone": data.get("timezone")
            }
    except Exception as e:
        print(f"GEO ERROR: {e}", file=sys.stdout, flush=True)
    return {
        "city": None,
        "region": None,
        "country": None,
        "org": None,
        "timezone": None
    }

@app.route('/')
def index():
    real_ip = get_real_ip(request)

    ua_string = request.headers.get('User-Agent', '')
    user_agent = parse(ua_string)

    device_model = user_agent.device.model or "Generic PC/Device"
    os_info = f"{user_agent.os.family} {user_agent.os.version_string}".strip()
    browser_info = f"{user_agent.browser.family} {user_agent.browser.version_string}".strip()

    geo = get_geo_from_ip(real_ip)

    print(f"\\n🎯 VISIT")
    print(f"IP: {real_ip}")
    print(f"DEVICE: {device_model}")
    print(f"OS: {os_info}")
    print(f"BROWSER: {browser_info}")
    print(f"CITY: {geo['city']}")
    print(f"REGION: {geo['region']}")
    print(f"COUNTRY: {geo['country']}")
    print(f"ORG: {geo['org']}")
    print(f"TIMEZONE: {geo['timezone']}")
    print(f"------------------------------", file=sys.stdout, flush=True)

    city = geo['city'] or 'Unknown'
    country = geo['country'] or 'Unknown'

    return f"""
    <!doctype html>
    <html lang="fa">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Connection Info</title>
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
          padding:
