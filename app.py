from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    x_forwarded_for = request.headers.get('X-Forwarded-For')
    x_real_ip = request.headers.get('X-Real-IP')
    cf_connecting_ip = request.headers.get('CF-Connecting-IP')
    true_client_ip = request.headers.get('True-Client-IP')
    fly_client_ip = request.headers.get('Fly-Client-IP')

    ip = None

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    elif x_real_ip:
        ip = x_real_ip.strip()
    elif cf_connecting_ip:
        ip = cf_connecting_ip.strip()
    elif true_client_ip:
        ip = true_client_ip.strip()
    elif fly_client_ip:
        ip = fly_client_ip.strip()
    else:
        ip = request.remote_addr

    print("\n" + "=" * 50)
    print(f"TIME: {now}")
    print(f"REAL IP: {ip}")
    print(f"REMOTE_ADDR: {request.remote_addr}")
    print(f"X-Forwarded-For: {x_forwarded_for}")
    print(f"X-Real-IP: {x_real_ip}")
    print(f"CF-Connecting-IP: {cf_connecting_ip}")
    print(f"True-Client-IP: {true_client_ip}")
    print(f"Fly-Client-IP: {fly_client_ip}")
    print(f"User-Agent: {request.headers.get('User-Agent')}")
    print("=" * 50 + "\n")

    return "System is online"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
