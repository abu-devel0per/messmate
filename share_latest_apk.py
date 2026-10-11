import http.server
import socketserver
import threading
import subprocess
import time
import re
import os
import sys
import qrcode

PORT = 8098
DIRECTORY = r"c:\Users\kames\mess mate\messmate1"
ARTIFACT_DIR = r"C:\Users\kames\.gemini\antigravity-ide\brain\5df438e8-8e9b-49ab-8b6b-c88bb919ed19"
QR_PATH = os.path.join(ARTIFACT_DIR, "apk_download_qr.png")
URL_FILE = os.path.join(DIRECTORY, "apk_download_url.txt")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
            print(f"HTTP Server serving on 0.0.0.0:{PORT}", flush=True)
            httpd.serve_forever()
    except Exception as e:
        print(f"HTTP server notice: {e}", flush=True)

def get_cloudflare_tunnel():
    cloudflared_exe = os.path.join(DIRECTORY, "cloudflared.exe")
    if not os.path.exists(cloudflared_exe):
        print("cloudflared.exe not found!", flush=True)
        return None, None

    proc = subprocess.Popen(
        [cloudflared_exe, "tunnel", "--url", f"http://127.0.0.1:{PORT}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )
    url = None
    start_time = time.time()
    while time.time() - start_time < 30:
        line = proc.stdout.readline()
        if not line:
            time.sleep(0.1)
            continue
        print(line.strip(), flush=True)
        match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
        if match:
            url = match.group(0)
            break
    return url, proc

if __name__ == "__main__":
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    time.sleep(1)

    url, proc = get_cloudflare_tunnel()
    if url:
        apk_url = f"{url}/MessMate-Release.apk"
        with open(URL_FILE, "w", encoding="utf-8") as f:
            f.write(apk_url)
        print(f"\n=======================================================", flush=True)
        print(f"APK_DOWNLOAD_URL={apk_url}", flush=True)
        print(f"=======================================================\n", flush=True)

        os.makedirs(ARTIFACT_DIR, exist_ok=True)
        qr = qrcode.QRCode(box_size=10, border=3)
        qr.add_data(apk_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(QR_PATH)
        print(f"QR code saved to: {QR_PATH}", flush=True)

        while True:
            time.sleep(30)
    else:
        print("Failed to get Cloudflare tunnel URL", flush=True)
        sys.exit(1)
