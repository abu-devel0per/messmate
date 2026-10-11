import os
import subprocess
import sys

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

android_dir = r"c:\Users\kames\mess mate\messmate1\frontend\android"
java_home = r"C:\Program Files\Android\Android Studio\jbr"

env = os.environ.copy()
env["JAVA_HOME"] = java_home
env["PATH"] = os.path.join(java_home, "bin") + os.pathsep + env.get("PATH", "")

print(f"Building release APK with JAVA_HOME={java_home} ...")
cmd = [os.path.join(android_dir, "gradlew.bat"), "assembleRelease"]

proc = subprocess.Popen(
    cmd,
    cwd=android_dir,
    env=env,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    encoding="utf-8",
    errors="replace"
)

for line in proc.stdout:
    sys.stdout.write(line)
    sys.stdout.flush()

proc.wait()
if proc.returncode == 0:
    print("\n✓ SUCCESS: Release APK built successfully!")
    out_apk = os.path.join(android_dir, "app", "build", "outputs", "apk", "release", "app-release.apk")
    if os.path.exists(out_apk):
        size_mb = os.path.getsize(out_apk) / (1024 * 1024)
        print(f"APK Location: {out_apk} ({size_mb:.2f} MB)")
        
        # Copy to root and frontend root for easy sharing
        dest1 = r"c:\Users\kames\mess mate\messmate1\MessMate-Release.apk"
        dest2 = r"c:\Users\kames\mess mate\messmate1\frontend\app-release.apk"
        import shutil
        shutil.copy2(out_apk, dest1)
        shutil.copy2(out_apk, dest2)
        print(f"Copied to {dest1}")
else:
    print(f"\n✗ Build failed with exit code: {proc.returncode}")
sys.exit(proc.returncode)
