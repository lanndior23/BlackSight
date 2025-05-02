import shodan
import getpass
from core.secure_config import load_config

def run_shodan_lookup(args):
    pw = getpass.getpass("Enter config password: ")
    config = load_config(pw)

    api_key = args.apikey or config.get("SHODAN_API_KEY")
    if not api_key:
        print("[-] No Shodan API key provided or found.")
        return

    api = shodan.Shodan(api_key)

    try:
        print(f"[+] Looking up {args.target} on Shodan...")
        result = api.host(args.target)

        print("="*50)
        print(f"IP: {result['ip_str']}")
        print(f"Organization: {result.get('org', 'n/a')}")
        print(f"Operating System: {result.get('os', 'n/a')}")
        print("Open Ports:", result.get('ports', []))
        print("-" * 50)

        for service in result['data']:
            print(f"Port: {service['port']}")
            print(f"Banner: {service.get('data', '').strip()[:100]}")
            print("-" * 30)

    except shodan.APIError as e:
        print(f"[-] Shodan error: {e}")
