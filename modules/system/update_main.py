import subprocess
import os
import requests
import zipfile
import io

GITHUB_ZIP_URL = "https://github.com/your-org/BlackSight/archive/refs/heads/main.zip"

def run_update(args):
    if os.path.isdir(".git"):
        print("[*] Detected Git repository. Pulling updates...")
        try:
            result = subprocess.run(["git", "pull"], capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("[-] Git Error:", result.stderr)
        except Exception as e:
            print(f"[-] Git update failed: {e}")
        return

    print("[*] Git not found. Fetching ZIP from remote source...")
    try:
        r = requests.get(GITHUB_ZIP_URL)
        if r.status_code != 200:
            print("[-] Failed to fetch update ZIP.")
            return

        with zipfile.ZipFile(io.BytesIO(r.content)) as zip_ref:
            zip_ref.extractall("temp_update")

        print("[+] Update downloaded. You must now manually replace the old files.")
        print("    Suggested: backup current folder, copy from ./temp_update")

    except Exception as e:
        print(f"[-] ZIP update failed: {e}")
