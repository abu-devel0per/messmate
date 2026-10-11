"""
Upload app-release.apk to GoFile.io (free, anonymous, no login, direct link)
then generate a styled QR code PNG for it.
"""
import os, json, sys, requests
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from PIL import Image, ImageDraw, ImageFont

APK_PATH = r"C:\Users\kames\mess mate\messmate1\frontend\app-release.apk"
QR_OUT   = r"C:\Users\kames\.gemini\antigravity-ide\brain\a7deed45-d65b-46af-ae42-895cab3b9335\messmate_apk_qr.png"

# ── 1. Get best GoFile server ───────────────────────────────────────────────
print("[1/4] Getting GoFile upload server …")
try:
    r = requests.get("https://api.gofile.io/servers", timeout=10)
    r.raise_for_status()
    data = r.json()
    server = data["data"]["servers"][0]["name"]
    print(f"      Using server: {server}")
except Exception as e:
    # fallback to known good server
    server = "store1"
    print(f"      Could not auto-detect server ({e}), using fallback: {server}")

# ── 2. Upload APK ───────────────────────────────────────────────────────────
apk_size_mb = os.path.getsize(APK_PATH) / 1_048_576
print(f"[2/4] Uploading APK ({apk_size_mb:.1f} MB) to GoFile …")
print("      This may take 3-5 minutes depending on network speed …")

upload_url = f"https://{server}.gofile.io/contents/uploadfile"
try:
    with open(APK_PATH, "rb") as f:
        resp = requests.post(
            upload_url,
            files={"file": ("MessMate-release.apk", f, "application/vnd.android.package-archive")},
            timeout=600,  # 10 min max
        )
    resp.raise_for_status()
    result = resp.json()
    if result.get("status") != "ok":
        print("Upload failed:", result)
        sys.exit(1)

    download_url = result["data"]["downloadPage"]
    direct_url   = result["data"].get("directLink", download_url)
    print(f"      ✓ Uploaded!")
    print(f"        Download page : {download_url}")
except Exception as e:
    print(f"Upload error: {e}")
    sys.exit(1)

# ── 3. Generate styled QR (points to the download page) ────────────────────
print("[3/4] Generating QR code …")

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=12,
    border=3,
)
qr.add_data(download_url)
qr.make(fit=True)

qr_img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    back_color=(15, 15, 25),   # dark background
    fill_color=(34, 197, 94),  # MessMate green
)

# Add banner
qr_rgba = qr_img.convert("RGBA")
W, H = qr_rgba.size
BANNER_H = 95
canvas = Image.new("RGBA", (W, H + BANNER_H), (15, 15, 25, 255))
canvas.paste(qr_rgba, (0, BANNER_H))

draw = ImageDraw.Draw(canvas)
try:
    font_title = ImageFont.truetype("arial.ttf", 30)
    font_sub   = ImageFont.truetype("arial.ttf", 15)
except OSError:
    font_title = ImageFont.load_default()
    font_sub   = font_title

for text, font, color, y in [
    ("MessMate APK", font_title, (34, 197, 94), 10),
    ("Scan to download  •  Link expires in 10 days", font_sub, (156, 163, 175), 52),
]:
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y), text, fill=color, font=font)

canvas.convert("RGB").save(QR_OUT, "PNG", optimize=True)
print(f"      ✓ QR saved → {QR_OUT}")

# ── 4. Summary ─────────────────────────────────────────────────────────────
print()
print("=" * 65)
print(f"  MessMate APK download page : {download_url}")
print(f"  QR image : {QR_OUT}")
print("=" * 65)
