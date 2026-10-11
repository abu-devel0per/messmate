import subprocess
import time
import re
import os
import requests
import sys

DIRECTORY = r"c:\Users\kames\mess mate\messmate1"
CLOUDFLARED = os.path.join(DIRECTORY, "cloudflared.exe")
FRONTEND_ENV = os.path.join(DIRECTORY, "frontend", ".env")
FRONTEND_ENV_LOCAL = os.path.join(DIRECTORY, "frontend", ".env.local")
BACKEND_URL_FILE = os.path.join(DIRECTORY, "backend_public_url.txt")

def start_tunnel():
    print("Starting Cloudflare Tunnel for Backend (port 8000)...", flush=True)
    proc = subprocess.Popen(
        [CLOUDFLARED, "tunnel", "--url", "http://127.0.0.1:8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )
    
    url = None
    start_time = time.time()
    while time.time() - start_time < 45:
        line = proc.stdout.readline()
        if not line:
            time.sleep(0.1)
            continue
        print(line.strip(), flush=True)
        match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
        if match:
            url = match.group(0)
            break
            
    if url:
        print(f"\n=======================================================", flush=True)
        print(f"Backend Public URL: {url}", flush=True)
        print(f"=======================================================\n", flush=True)
        with open(BACKEND_URL_FILE, "w", encoding="utf-8") as f:
            f.write(url)
        with open(FRONTEND_ENV, "w", encoding="utf-8") as f:
            f.write(f"EXPO_PUBLIC_BACKEND_URL={url}\n")
        with open(FRONTEND_ENV_LOCAL, "w", encoding="utf-8") as f:
            f.write(f"EXPO_PUBLIC_BACKEND_URL={url}\n")
        print(f"Updated {FRONTEND_ENV} with {url}", flush=True)
        
        # Wait until Cloudflare edge DNS propagates
        for attempt in range(1, 15):
            time.sleep(2)
            try:
                r = requests.get(f"{url}/api", timeout=6)
                if r.status_code == 200:
                    print(f"✅ Public Backend is LIVE & RESPONDING: {url}/api -> {r.status_code}", flush=True)
                    break
            except Exception as e:
                print(f"Propagating DNS (attempt {attempt}/15)...", flush=True)
                
        while True:
            time.sleep(1)
    else:
        print("Failed to get Cloudflare tunnel URL", flush=True)
        sys.exit(1)

if __name__ == "__main__":
    start_tunnel()
