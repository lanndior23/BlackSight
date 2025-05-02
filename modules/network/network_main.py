import ipaddress
import socket
import subprocess
import platform
import json
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def ping_host(ip):
    try:
        output = subprocess.run(
            ['ping', '-c', '1', '-W', '1', ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return output.returncode == 0
    except Exception:
        return False

def ping_sweep(subnet):
    print(f"[+] Performing ping sweep on {subnet} ...")
    live_hosts = []
    executor = ThreadPoolExecutor(max_workers=50)
    try:
        futures = {executor.submit(ping_host, str(ip)): ip for ip in ipaddress.IPv4Network(subnet, strict=False)}
        for future in as_completed(futures):
            ip = futures[future]
            try:
                if future.result(timeout=2):
                    print(f" - Host Up: {ip}")
                    live_hosts.append(str(ip))
            except Exception as e:
                print(f"[!] Error with {ip}: {e}")
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user. Exiting cleanly...")
        executor.shutdown(wait=False)  # Don't wait for threads
        return []
    finally:
        executor.shutdown(wait=False)  # Ensure shutdown on any path
    return live_hosts

def tcp_connect_scan(host, ports):
    print(f"\n[+] Starting TCP Connect Scan on {host} ...")
    open_ports = []
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex((host, port))
                if result == 0:
                    open_ports.append(port)
                    banner = grab_banner(host, port)
                    if banner:
                        print(f" - Port {port}/TCP Open | Banner: {banner}")
                    else:
                        print(f" - Port {port}/TCP Open | Banner: [No response]")
        except Exception:
            continue
    return open_ports

def grab_banner(ip, port):
    try:
        with socket.socket() as s:
            s.settimeout(1)
            s.connect((ip, port))
            banner = s.recv(1024).decode().strip()
            return banner
    except:
        return None

def parse_ports(ports_arg, scan_type):
    if ports_arg:
        return [int(p.strip()) for p in ports_arg.split(',') if p.strip().isdigit()]
    return list(range(1, 1025)) if scan_type == 'quick' else list(range(1, 65536))

def nmap_service_scan(ip):
    if platform.system().lower() != 'linux':
        print("[-] Nmap scanning is only supported on Linux.")
        return

    print(f"\n[+] Running Nmap version scan on {ip} ...")
    try:
        result = subprocess.check_output(['nmap', '-sV', '-Pn', ip], stderr=subprocess.DEVNULL)
        print(result.decode())
    except subprocess.CalledProcessError:
        print("[-] Nmap scan failed.")

def scan_host(host, port_list):
    print(f"\n[+] Scanning host: {host}")
    host_result = []
    for port in port_list:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex((host, port))
                if result == 0:
                    banner = grab_banner(host, port)
                    print(f" - Port {port}/TCP Open | Banner: {banner or '[No response]'}")
                    host_result.append({'port': port, 'banner': banner or 'N/A'})
        except:
            continue
    return host_result

def save_results_to_file(results, output_file):
    try:
        with open(output_file, 'w') as outfile:
            json.dump(results, outfile, indent=4)
        print(f"\n[+] Scan results saved to {output_file}")
    except Exception as e:
        print(f"[-] Failed to save results: {e}")

def run_network_scan(args):
    target = args.target
    scan_type = args.scan_type
    port_list = parse_ports(args.ports, scan_type)
    results = {}

    if '/' in target:
        hosts = ping_sweep(target)
    else:
        hosts = [target]

    for host in hosts:
        host_result = scan_host(host, port_list)
        results[host] = host_result

        # Optional Nmap scan
        if args.use_nmap:
            nmap_service_scan(host)

    # Optional JSON output
    if args.output:
        save_results_to_file(results, args.output)

def main():
    parser = argparse.ArgumentParser(description="Network scanning tool")
    parser.add_argument('--use-nmap', action='store_true', help='Use Nmap for version detection (Linux only)')
    # Add other arguments as needed
    args = parser.parse_args()
    run_network_scan(args)

if __name__ == "__main__":
    main()
