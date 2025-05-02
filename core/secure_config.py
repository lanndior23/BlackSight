# core/secure_config.py

import os
import base64
from cryptography.fernet import Fernet
import getpass
from hashlib import sha256

CONFIG_FILE = "config.sec"

def generate_key(password: str) -> bytes:
    return sha256(password.encode()).digest()

def encrypt_config(data: dict, password: str, config_file: str = CONFIG_FILE):
    key = Fernet.generate_key()
    f = Fernet(key)
    token = f.encrypt(str(data).encode())

    master_key = generate_key(password)
    wrapper = Fernet(base64.urlsafe_b64encode(master_key[:32]))
    final = wrapper.encrypt(key)

    with open(config_file, "wb") as f:
        f.write(final + b"\n" + token)

    print(f"[+] Encrypted config saved to {config_file}.")

def load_config(password: str):
    try:
        with open(CONFIG_FILE, "rb") as f:
            key_encrypted = f.readline().strip()
            token = f.read().strip()

        master_key = generate_key(password)
        wrapper = Fernet(base64.urlsafe_b64encode(master_key[:32]))
        key = wrapper.decrypt(key_encrypted)

        f = Fernet(key)
        data = eval(f.decrypt(token).decode())

        return data

    except Exception as e:
        print("[-] Failed to load config:", e)
        return None
