import requests
import json
import sys
import whois
import dns.resolver
import ipinfo

def fetch_subdomains_crtsh(domain):
    print(f"[+] Gathering subdomains for {domain} using crt.sh ...")
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print("[-] Failed to fetch from crt.sh")
            return []

        data = response.json()
        subdomains = set()
        for entry in data:
            name_value = entry['name_value']
            for sub in name_value.split('\n'):
                if '*' not in sub:
                    subdomains.add(sub.strip())

        return sorted(subdomains)

    except Exception as e:
        print(f"[-] Error: {e}")
        return []

def perform_whois_lookup(domain):
    print(f"\n[+] Performing WHOIS lookup for {domain} ...")
    try:
        w = whois.whois(domain)
        print(f" - Domain Name: {w.domain_name}")
        print(f" - Registrar: {w.registrar}")
        print(f" - Creation Date: {w.creation_date}")
        print(f" - Expiry Date: {w.expiration_date}")
        print(f" - Name Servers: {w.name_servers}")
        print(f" - Emails: {w.emails}")
    except Exception as e:
        print(f"[-] WHOIS lookup failed: {e}")

def get_dns_records(domain):
    print(f"\n[+] Fetching DNS records for {domain} ...")
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT']
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            print(f" - {record_type} Records:")
            for rdata in answers:
                print(f"   -> {rdata}")
        except Exception:
            continue

def get_ip_info(ip):
    print(f"\n[+] Getting IP info for {ip} ...")
    try:
        handler = ipinfo.getHandler()
        details = handler.getDetails(ip)
        print(f" - IP: {details.ip}")
        print(f" - City: {details.city}")
        print(f" - Region: {details.region}")
        print(f" - Country: {details.country}")
        print(f" - Org: {details.org}")
    except Exception as e:
        print(f"[-] IP info lookup failed: {e}")

def run_recon(args):
    target = args.target.strip()
    print(f"[RECON] Starting recon on {target}")

    subdomains = fetch_subdomains_crtsh(target)
    if subdomains:
        print(f"\n[+] Found {len(subdomains)} subdomains:\n")
        for sub in subdomains:
            print(f" - {sub}")
    else:
        print("[-] No subdomains found.")

    perform_whois_lookup(target)
    get_dns_records(target)

    # Try to get IP info for A record
    try:
        ip = str(dns.resolver.resolve(target, 'A')[0])
        get_ip_info(ip)
    except:
        print("[-] Could not resolve IP for target.")
