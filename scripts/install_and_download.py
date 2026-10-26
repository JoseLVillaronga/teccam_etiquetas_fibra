import sys
import subprocess
import urllib.request
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent.parent
    pip_exe = root / "venv" / "bin" / "pip"
    req_file = root / "requirements.txt"
    vendor_dir = root / "app" / "static" / "vendor" / "tailwind"
    vendor_dir.mkdir(parents=True, exist_ok=True)
    tailwind_file = vendor_dir / "tailwind.js"

    print(f"[*] Installing requirements from {req_file.name}...")
    subprocess.check_call([str(pip_exe), "install", "-r", str(req_file)])

    print("[*] Downloading Tailwind CDN script for offline use...")
    url = "https://cdn.tailwindcss.com"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        content = response.read()
    
    tailwind_file.write_bytes(content)
    print(f"[+] Successfully saved Tailwind CDN to {tailwind_file} ({len(content)} bytes)")

if __name__ == "__main__":
    main()
