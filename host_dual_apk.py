import http.server
import socketserver
import threading
import subprocess
import time
import re
import os
import sys
import socket
import json
import qrcode

PORT = 8092
DIRECTORY = r"c:\Users\kames\mess mate\messmate1"
ARTIFACT_DIR = r"C:\Users\kames\.gemini\antigravity-ide\brain\5df438e8-8e9b-49ab-8b6b-c88bb919ed19"

LAN_QR_PATH = os.path.join(ARTIFACT_DIR, "lan_apk_qr.png")
NGROK_QR_PATH = os.path.join(ARTIFACT_DIR, "ngrok_apk_qr.png")
CF_QR_PATH = os.path.join(ARTIFACT_DIR, "cf_apk_qr.png")
URL_FILE = os.path.join(DIRECTORY, "apk_urls_active.txt")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
            print(f"HTTP Server running on port {PORT}", flush=True)
            httpd.serve_forever()
    except Exception as e:
        print(f"HTTP server notice: {e}", flush=True)

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "172.17.2.136"

def start_ngrok():
    ngrok_exe = os.path.join(DIRECTORY, "ngrok.exe")
    if not os.path.exists(ngrok_exe):
        ngrok_exe = "ngrok"
    try:
        subprocess.Popen([ngrok_exe, "http", str(PORT)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
        import urllib.request
        for _ in range(10):
            try:
                req = urllib.request.Request("http://127.0.0.1:4040/api/tunnels")
                with urllib.request.urlopen(req, timeout=2) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    for tunnel in data.get("tunnels", []):
                        if tunnel.get("proto") == "https":
                            return tunnel["public_url"]
            except Exception:
                time.sleep(1)
    except Exception as e:
        print(f"Ngrok note: {e}", flush=True)
    return None

def start_cf():
    cloudflared_exe = os.path.join(DIRECTORY, "cloudflared.exe")
    if not os.path.exists(cloudflared_exe):
        return None
    proc = subprocess.Popen(
        [cloudflared_exe, "tunnel", "--url", f"http://127.0.0.1:{PORT}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )
    start_time = time.time()
    while time.time() - start_time < 25:
        line = proc.stdout.readline()
        if not line:
            time.sleep(0.1)
            continue
        match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
        if match:
            return match.group(0)
    return None

def make_qr(url, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    qr = qrcode.QRCode(box_size=10, border=3)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(path)
    print(f"QR code saved -> {path}", flush=True)

if __name__ == "__main__":
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    time.sleep(1)

    lan_ip = get_lan_ip()
    lan_url = f"http://{lan_ip}:{PORT}/MessMate-Release.apk"
    make_qr(lan_url, LAN_QR_PATH)

    cf_url = start_cf()
    if cf_url:
        cf_apk = f"{cf_url}/MessMate-Release.apk"
        make_qr(cf_apk, CF_QR_PATH)
    else:
        cf_apk = None

    ngrok_base = start_ngrok()
    if ngrok_base:
        ngrok_apk = f"{ngrok_base}/MessMate-Release.apk"
        make_qr(ngrok_apk, NGROK_QR_PATH)
    else:
        ngrok_apk = None

    with open(URL_FILE, "w", encoding="utf-8") as f:
        f.write(f"LAN: {lan_url}\n")
        if cf_apk:
            f.write(f"CLOUDFLARE: {cf_apk}\n")
        if ngrok_apk:
            f.write(f"NGROK: {ngrok_apk}\n")

    print("\n--- ACTIVE APK URLS ---", flush=True)
    print(f"LAN_URL: {lan_url}", flush=True)
    if cf_apk:
        print(f"CF_URL: {cf_apk}", flush=True)
    if ngrok_apk:
        print(f"NGROK_URL: {ngrok_apk}", flush=True)
    print("------------------------\n", flush=True)

    while True:
        time.sleep(30)
