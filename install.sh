#!/bin/bash
echo "[*] Installing BlackSight..."
sudo apt update
sudo apt install -y python3 python3-pip
pip3 install -r requirements.txt
chmod +x main.py
echo "[*] Done. Run with: python3 main.py"
