import qrcode

def generate_cloudflare_qr():
    url = "https://inf-ceremony-respectively-enlarge.trycloudflare.com/MessMate-Release.apk"
    print(f"Generating QR for: {url}")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    artifact_path = r"C:\Users\kames\.gemini\antigravity-ide\brain\e94fa19f-b301-488b-a0ad-128a3c976080\cloudflare_apk_qr.png"
    img.save(artifact_path)
    print(f"Saved QR code to {artifact_path}")

if __name__ == "__main__":
    generate_cloudflare_qr()
