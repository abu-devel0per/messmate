import http.server
import socketserver
import threading
import subprocess
import time
import re
import qrcode
import os
import sys

PORT = 8090
DIRECTORY = r"c:\Users\kames\mess mate\messmate1"
ARTIFACT_QR_PATH = r"C:\Users\kames\.gemini\antigravity-ide\brain\a7deed45-d65b-46af-ae42-895cab3b9335\apk_qr.png"
URL_FILE_PATH = os.path.join(DIRECTORY, "apk_download_url.txt")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"HTTP Server running on port {PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Server start note: {e}")

def get_cloudflare_url():
    cloudflared_exe = os.path.join(DIRECTORY, "cloudflared.exe")
    if not os.path.exists(cloudflared_exe):
        print("cloudflared.exe not found!")
        return None

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
    if os.path.exists(URL_FILE_PATH):
        try:
            os.remove(URL_FILE_PATH)
        except Exception:
            pass
            
    os.makedirs(os.path.dirname(ARTIFACT_QR_PATH), exist_ok=True)
    
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    time.sleep(1)
    
    print("Starting Cloudflare tunnel...")
    res = get_cloudflare_url()
    if res and res[0]:
        cf_url, proc = res
        download_url = f"{cf_url}/MessMate-Release.apk"
        print(f"PUBLIC_DOWNLOAD_URL: {download_url}")
        
        with open(URL_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(download_url)
            
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(download_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(ARTIFACT_QR_PATH)
        print(f"SUCCESS: QR saved to {ARTIFACT_QR_PATH}")
        
        # Keep server and tunnel alive for downloads
        print("Server and tunnel are live. Press Ctrl+C to stop.")
        while True:
            time.sleep(60)
    else:
        print("Failed to acquire trycloudflare URL within timeout.")
