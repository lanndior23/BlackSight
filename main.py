#!/usr/bin/env python3
import argparse
import platform
import sys
import json
import csv
import os
from modules.web.web_main import run_web_scan

try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    print("Error: The 'bs4' module is not installed. Please install it using 'pip install beautifulsoup4'.")
    sys.exit(1)

# Ensure the correct import path for password_main
from modules.passwords.password_main import run_password_attack
from modules.wifi.wifi_main import run_wifi_crack
from modules.exploits.exploit_main import run_exploit_msf
from modules.intel.shodan_main import run_shodan_lookup
from modules.system.update_main import run_update

def show_banner():
    print(r"""
██████╗ ██╗      █████╗  ██████╗██╗  ██╗    ███████╗██╗ ██████╗ ██╗  ██╗████████╗
██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝    ██╔════╝██║██╔═══██╗██║ ██╔╝╚══██╔══╝
██████╔╝██║     ███████║██║     █████╔╝     █████╗  ██║██║   ██║█████╔╝    ██║   
██╔═══╝ ██║     ██╔══██║██║     ██╔═██╗     ██╔══╝  ██║██║   ██║██╔═██╗    ██║   
██║     ███████╗██║  ██║╚██████╗██║  ██╗    ██║     ██║╚██████╔╝██║  ██╗   ██║   
╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝                                                                            
Advanced Terminal-Based Ethical Hacking Toolkit - Black Sight
""")

def show_module_menu():
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                📦 Black Sight - Module Selection Menu                     ║
╠════════╦═════════════════════════════════════════════════════════════════ ╣
║  No.   ║ Module   │ Description                                           ║
╠════════╬══════════╪═══════════════════════════════════════════════════════╣
║   1    ║ recon    │ Passive recon & OSINT (DNS, whois, HTTP headers)      ║
║   2    ║ network  │ Port scanning (TCP/UDP) with optional Nmap support    ║
║   3    ║ web      │ Web fuzzing / dir brute-force / header fingerprint    ║
║   4    ║ pass     │ Password brute-force (FTP, SSH, etc.)                 ║ 
║   5    ║ wifi     │ Wi-Fi scanner & WPA2 cracking (Linux only)            ║
║   6    ║ exploit  │ Exploit execution & metasploit use                    ║
║   7    ║ shodan   │ Shodan Intelligence Gathering via API                 ║
║   8    ║ export   │ Report exporter (PDF, HTML, Markdown)                 ║
║   9    ║ update   │ Check for updates, install new modules                ║
╚════════╩══════════╧═══════════════════════════════════════════════════════╝

🧪 Examples:
    🔍 Recon       → python3 main.py recon --target example.com
    🌐 Network     → python3 main.py network --target 192.168.1.1 --tcp
    🕸️  Web        → python3 main.py web --target http://site.com --wordlist wordlist.txt
    🔐 Password    → python3 main.py pass --service ssh --target 192.168.1.100 --user root --wordlist rockyou.txt
    📡 Wi-Fi      → sudo python3 main.py wifi --interface wlan0
    💥 Exploit     → python3 main.py exploit --module ms17_010 --target 192.168.1.105
    🌍 Shodan      → python3 main.py shodan --query "apache"
    📤 Export      → python3 main.py export --format pdf --output report.pdf
    🔄 Update      → python3 main.py update
""")

def save_report(data, filename, fmt):
    os.makedirs("reports", exist_ok=True)
    path = os.path.join("reports", f"{filename}.{fmt}")

    if fmt == "json":
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"[+] JSON report saved to {path}")

    elif fmt == "csv":
        if isinstance(data, list) and isinstance(data[0], dict):
            with open(path, "w", newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            print(f"[+] CSV report saved to {path}")
        else:
            print("[-] CSV export requires a list of dictionaries.")

    else:
        print("[-] Unsupported report format.")

def run_report_export(args):
    if not os.path.exists(args.input):
        print("[-] Input file not found.")
        return

    with open(args.input) as f:
        data = json.load(f)

    save_report(data, args.output, args.format)

def main():
    show_banner()

    parser = argparse.ArgumentParser(description='Black Sight - Advanced Ethical Hacking Toolkit')
    subparsers = parser.add_subparsers(dest='command', help='Module to run')

    # Recon module
    recon_parser = subparsers.add_parser('recon', help='Reconnaissance and OSINT tools')
    recon_parser.add_argument('--target', required=True, help='Target domain or IP')

    # Network scanner
    net_parser = subparsers.add_parser('network', help='Network scanning tools')
    net_parser.add_argument('--target', required=True, help='Target IP/subnet')
    net_parser.add_argument('--scan-type', choices=['full', 'quick'], default='quick')
    net_parser.add_argument('--ports', help='Comma-separated list of ports (e.g. 21,22,80)')
    net_parser.add_argument('--output', help='Path to save results in JSON format')
    net_parser.add_argument('--use-nmap', action='store_true', help='Use Nmap for version detection (Linux only)')

    # Web module
    web_parser = subparsers.add_parser('web', help='Web app testing')
    web_parser.add_argument('--target', required=True, help='Target URL (e.g. http://example.com)')
    web_parser.add_argument('--wordlist', help='Path to wordlist file')
    web_parser.add_argument('--brute-login', action='store_true', help='Enable login form bruteforce')
    web_parser.add_argument('--userlist', help='Username wordlist path')
    web_parser.add_argument('--passlist', help='Password wordlist path')
    web_parser.add_argument('--json-report', action='store_true', help='Save scan results as JSON')
    web_parser.set_defaults(func=run_web_scan)

    # Password module
    pass_parser = subparsers.add_parser('pass', help='Password attacks (SSH, etc.)')
    pass_parser.add_argument('--service', required=True, choices=['ssh', 'ftp'], help='Target service (ssh or ftp)')
    pass_parser.add_argument('--host', required=True, help='Target IP or hostname')
    pass_parser.add_argument('--port', type=int, help='Custom port (default 22 for SSH)')
    pass_parser.add_argument('--userlist', required=True, help='Username wordlist path')
    pass_parser.add_argument('--passlist', required=True, help='Password wordlist path')
    pass_parser.set_defaults(func=run_password_attack)

    # Wi-Fi cracking module
    wifi_parser = subparsers.add_parser('wifi', help='Wi-Fi cracking module (Linux only)')
    wifi_parser.add_argument('--interface', required=True, help='Wireless interface (e.g., wlan0)')
    wifi_parser.add_argument('--bssid', required=True, help='Target BSSID (MAC address)')
    wifi_parser.add_argument('--channel', required=True, help='Wi-Fi channel')
    wifi_parser.add_argument('--wordlist', required=True, help='Path to wordlist file')
    wifi_parser.set_defaults(func=run_wifi_crack)

    # Exploit module
    exploit_parser = subparsers.add_parser('exploit', help='Run automated exploits using Metasploit')
    exploit_parser.add_argument('--target', required=True, help='Target IP')
    exploit_parser.add_argument('--exploit', required=True, help='Exploit module path (e.g., exploit/windows/smb/ms17_010_eternalblue)')
    exploit_parser.add_argument('--payload', required=True, help='Payload (e.g., windows/meterpreter/reverse_tcp)')
    exploit_parser.add_argument('--lhost', required=True, help='Local host IP')
    exploit_parser.add_argument('--lport', required=True, help='Local port')
    exploit_parser.set_defaults(func=run_exploit_msf)

    # Shodan lookup module
    shodan_parser = subparsers.add_parser('shodan', help='Lookup IP using Shodan')
    shodan_parser.add_argument('--target', required=True, help='Target IP address')
    shodan_parser.add_argument('--apikey', required=True, help='Your Shodan API key')
    shodan_parser.set_defaults(func=run_shodan_lookup)

    # Report export module
    report_parser = subparsers.add_parser('export', help='Export reports in JSON or CSV format')
    report_parser.add_argument('--input', required=True, help='Path to input JSON file')
    report_parser.add_argument('--output', required=True, help='Output filename (without extension)')
    report_parser.add_argument('--format', required=True, choices=['json', 'csv'], help='Output format (json or csv)')
    report_parser.set_defaults(func=run_report_export)

    # Update module
    update_parser = subparsers.add_parser('update', help='Pull latest version from GitHub')
    update_parser.set_defaults(func=run_update)

    args = parser.parse_args()

    if args.command == 'recon':
        from modules.recon.recon_main import run_recon
        run_recon(args)
    elif args.command == 'network':
        from modules.network.network_main import run_network_scan
        run_network_scan(args)
    elif args.command == 'web':
        run_web_scan(args)
    elif args.command == 'pass':
        run_password_attack(args)
    elif args.command == 'wifi':
        run_wifi_crack(args)
    elif args.command == 'exploit':
        run_exploit_msf(args)
    elif args.command == 'export':
        run_report_export(args)
    elif args.command == 'shodan':
        run_shodan_lookup(args)
    elif args.command == 'update':
        run_update(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        show_banner()
        show_module_menu()
        sys.exit(0)
    main()
