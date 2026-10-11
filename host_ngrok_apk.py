import http.server
import socketserver
import threading
import subprocess
import time
import requests
import qrcode
import os

PORT = 8090
DIRECTORY = r"c:\Users\kames\mess mate\messmate1"
ARTIFACT_QR_PATH = r"C:\Users\kames\.gemini\antigravity-ide\brain\40a8a915-52e8-4cbf-aa71-a56f43261c05\download_apk_qr.png"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"HTTP Server running on port {PORT}")
            httpd.serve_forever()
    except OSError:
        print("Port in use, assuming server already running")

if __name__ == "__main__":
    os.makedirs(os.path.dirname(ARTIFACT_QR_PATH), exist_ok=True)
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    
    # Start ngrok
    print("Starting ngrok tunnel...")
    ngrok_process = subprocess.Popen(["ngrok", "http", str(PORT)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(4) # Wait for ngrok to initialize
    
    try:
        res = requests.get("http://127.0.0.1:4040/api/tunnels")
        url = res.json()["tunnels"][0]["public_url"]
        download_url = f"{url}/MessMate-Release.apk"
        print(f"Ngrok URL: {download_url}")
        
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(download_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(ARTIFACT_QR_PATH)
        print(f"SUCCESS: QR saved to {ARTIFACT_QR_PATH}")
        
        print("Ngrok tunnel is live. Press Ctrl+C to stop.")
        while True:
            time.sleep(60)
    except Exception as e:
        print(f"Error: {e}")
        ngrok_process.kill()
