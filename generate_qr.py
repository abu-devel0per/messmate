import urllib.request
import json
import qrcode
import sys

def get_ngrok_url():
    try:
        req = urllib.request.Request("http://localhost:4040/api/tunnels")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            for tunnel in data['tunnels']:
                if tunnel['proto'] == 'https':
                    return tunnel['public_url']
            return data['tunnels'][0]['public_url']
    except Exception as e:
        print(f"Failed to fetch ngrok URL: {e}")
        sys.exit(1)

def generate_qr(url):
    apk_url = f"{url}/MessMate-Release.apk"
    print(f"Generating QR for: {apk_url}")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(apk_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    artifact_path = r"C:\Users\kames\.gemini\antigravity-ide\brain\e94fa19f-b301-488b-a0ad-128a3c976080\download_qr_latest.png"
    img.save(artifact_path)
    print(f"Saved QR code to {artifact_path}")

if __name__ == "__main__":
    url = get_ngrok_url()
    generate_qr(url)
