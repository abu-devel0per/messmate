with open('backend/server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'f"' in line and line.rstrip().endswith('{'):
        print(f'Line {i+1}: {line.strip()}')
