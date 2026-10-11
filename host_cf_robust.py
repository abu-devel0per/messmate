import http.server
import socketserver
import threading
import subprocess
import time
import re
import qrcode
import os

PORT = 8092 # New port to avoid conflicts
DIRECTORY = r"c:\Users\kames\mess mate\messmate1"
ARTIFACT_QR_PATH = r"C:\Users\kames\.gemini\antigravity-ide\brain\f14889b4-d3b0-4a94-bc8f-6e79d89a3421\apk_qr.png"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    # Explicitly bind to 127.0.0.1 so cloudflared can always reach it (bypasses Windows Firewall)
    try:
        with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
            print(f"HTTP Server running on 127.0.0.1:{PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Server error: {e}")

def get_cloudflare_url():
    cloudflared_exe = os.path.join(DIRECTORY, "cloudflared.exe")
    proc = subprocess.Popen(
        [cloudflared_exe, "tunnel", "--url", f"http://127.0.0.1:{PORT}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="ignore",
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    )
    url = None
    start_time = time.time()
    while time.time() - start_time < 20:
        line = proc.stdout.readline()
        if not line:
            time.sleep(0.1)
            continue
        match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
        if match:
            url = match.group(0)
            break
    return url, proc

if __name__ == "__main__":
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    time.sleep(2)
    
    res = get_cloudflare_url()
    if res and res[0]:
        cf_url, proc = res
        download_url = f"{cf_url}/MessMate-Release.apk"
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(download_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(ARTIFACT_QR_PATH)
        print(f"URL: {download_url}")
        
        while True:
            time.sleep(60)
