import json
import csv
import os

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
