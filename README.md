# 🛡️ Black Sight

> Advanced Terminal-Based Ethical Hacking Toolkit — for Kali Linux & Windows

![banner](https://img.shields.io/badge/status-stable-green)  
CLI-only, offline-capable, modular, and powerful for red teamers & ethical hackers.

---

## 🚀 Features

- 🌐 Network & Port Scanning (TCP/UDP)
- 🔎 Web Recon (Directory brute-forcing, headers)
- 🔐 Password Attacks (FTP, SSH)
- 📶 Wi-Fi Cracking (Linux only)
- 📡 Shodan Integration & OSINT
- 📄 Report Generator (PDF, HTML, Markdown)
- 🔄 Auto-Update / Plugin Loader
- 💼 Works in Offline/Air-Gapped Environments

---

## ⚙️ Installation

### Kali Linux:
```bash
git clone https://github.com/lanndior23/BlackSight.git
cd BlackSight
chmod +x install.sh
./install.sh

Windows:
Download BlackSight-Windows.zip
Extract and run using:
run.bat network --target 192.168.1.1

🧪 Example Usage
python3 main.py network --target 192.168.1.1
python3 main.py web --target http://site.com --wordlist modules/web/common.txt
python3 main.py ftp --target 192.168.1.5 --user admin --wordlist rockyou.txt
python3 main.py report --target 192.168.1.1 --module web --result results.txt --output pdf

📁 Modules
network: Port scanning with optional Nmap integration

web: Directory discovery and fingerprinting

ftp, ssh: Password brute-forcing

wifi: Monitor, scan, deauth & crack (Linux only)

shodan: Intelligence gathering with API

report: Export in clean formats

📄 License
MIT © 2025 lanndior

🔗 Links
GitHub: github.com/lanndior23/BlackSight


---

## ✅ Add LICENSE File

Create a file named `LICENSE`:

```text
MIT License

Copyright (c) 2025 lanndior


▶️ Run the tool (examples):

🔍 Network Scan:
python3 main.py network --target 192.168.1.1

🌐 Web Recon:
python3 main.py web --target http://example.com --wordlist modules/web/common.txt

🔐 FTP Brute-force:
python3 main.py ftp --target 192.168.1.10 --user admin --wordlist rockyou.txt

📡 Shodan OSINT:
python3 main.py shodan --target google.com

🧾 Report Generator:
python3 main.py report --target 192.168.1.1 --module network --result output.txt --output pdf
