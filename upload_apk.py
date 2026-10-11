import urllib.request
import json
import os

file_path = r"C:\Users\kames\mess mate\messmate1\MessMate-Release.apk"
url = 'https://file.io/?expires=1d'

# file.io requires multipart/form-data for uploads. Let's use a simpler boundary construction
boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
headers = {'Content-Type': f'multipart/form-data; boundary={boundary}'}

with open(file_path, 'rb') as f:
    file_data = f.read()

body = (
    f'--{boundary}\r\n'
    f'Content-Disposition: form-data; name="file"; filename="MessMate-Release.apk"\r\n'
    f'Content-Type: application/vnd.android.package-archive\r\n\r\n'
).encode('utf-8') + file_data + f'\r\n--{boundary}--\r\n'.encode('utf-8')

req = urllib.request.Request(url, data=body, headers=headers, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(f"DOWNLOAD_LINK: {result['link']}")
except Exception as e:
    print(f"ERROR: {e}")
