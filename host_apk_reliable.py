import subprocess
import time
import urllib.request
import json
import qrcode
import os
import socket
import sys

PORT = 8088
DIRECTORY = r"c:\Users\kames\mess mate\messmate1"
ARTIFACT_DIR = r"C:\Users\kames\.gemini\antigravity-ide\brain\40a8a915-52e8-4cbf-aa71-a56f43261c05"
NGROK_QR_PATH = os.path.join(ARTIFACT_DIR, "ngrok_apk_qr.png")
LAN_QR_PATH = os.path.join(ARTIFACT_DIR, "lan_apk_qr.png")
URLS_FILE = os.path.join(DIRECTORY, "apk_urls.txt")

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "172.17.3.146"

def kill_port(port):
    if os.name == "nt":
        try:
            out = subprocess.check_output(f'netstat -ano | findstr "::{port}"', shell=True, text=True, errors="ignore")
            for line in out.strip().split("\n"):
                parts = line.split()
                if len(parts) > 4:
                    pid = parts[-1]
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

def get_ngrok_url():
    for _ in range(30):
        try:
            req = urllib.request.Request("http://127.0.0.1:4040/api/tunnels")
            with urllib.request.urlopen(req, timeout=2) as response:
                data = json.loads(response.read().decode('utf-8'))
                tunnels = data.get("tunnels", [])
                for tunnel in tunnels:
                    if tunnel.get("proto") == "https":
                        return tunnel["public_url"]
                if tunnels:
                    return tunnels[0]["public_url"]
        except Exception:
            time.sleep(1)
    return None

def make_qr(data_url, save_path):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(save_path)
    print(f"Generated QR for {data_url} -> {save_path}")

if __name__ == "__main__":
    kill_port(PORT)
    kill_port(4040)
    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    
    # Start HTTP server as a robust independent process
    server_proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT)],
        cwd=DIRECTORY,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    )
    print(f"Started HTTP Server PID: {server_proc.pid} on port {PORT}")
    time.sleep(2)
    
    lan_ip = get_lan_ip()
    lan_url = f"http://{lan_ip}:{PORT}/MessMate-Release.apk"
    make_qr(lan_url, LAN_QR_PATH)
    
    # Start ngrok tunnel
    print("Starting ngrok...")
    ngrok_proc = subprocess.Popen(
        ["ngrok", "http", str(PORT)],
        cwd=DIRECTORY,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    )
    
    ngrok_public = get_ngrok_url()
    ngrok_url = f"{ngrok_public}/MessMate-Release.apk" if ngrok_public else "FAILED"
    if ngrok_public:
        make_qr(ngrok_url, NGROK_QR_PATH)
    else:
        print("Could not retrieve ngrok URL")
        
    with open(URLS_FILE, "w", encoding="utf-8") as f:
        f.write(f"NGROK:{ngrok_url}\n")
        f.write(f"LAN:{lan_url}\n")
        
    print("All servers live and running. Press Ctrl+C to stop.")
    while True:
        time.sleep(60)
