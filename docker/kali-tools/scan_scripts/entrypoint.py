import argparse
import json
import subprocess
import shlex


def run_nmap_basic(url: str) -> dict:
    try:
        cmd = f"nmap -Pn --top-ports 100 {shlex.quote(url)}"
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=120).decode()
    except Exception as e:
        return {"tool": "nmap", "error": str(e)}
    return {"tool": "nmap", "output": out}


def run_nikto_basic(url: str) -> dict:
    try:
        cmd = f"nikto -host {shlex.quote(url)} -Tuning b -maxtime 120s"
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=180).decode()
    except Exception as e:
        return {"tool": "nikto", "error": str(e)}
    return {"tool": "nikto", "output": out}


def run_sqlmap_basic(url: str) -> dict:
    try:
        cmd = f"sqlmap -u {shlex.quote(url)} --batch --crawl=1 --timeout=60 --level=1 --risk=1"
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=300).decode()
    except Exception as e:
        return {"tool": "sqlmap", "error": str(e)}
    return {"tool": "sqlmap", "output": out}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", required=True)
    parser.add_argument("--url", required=True)
    args = parser.parse_args()

    url = args.url
    scan_type = args.type

    result = {"url": url, "type": scan_type, "issues": []}
    if scan_type in ("port", "version", "network", "machine"):
        result["nmap"] = run_nmap_basic(url)
    elif scan_type == "application":
        result["nikto"] = run_nikto_basic(url)
    elif scan_type == "database":
        result["sqlmap"] = run_sqlmap_basic(url)
    elif scan_type == "server":
        result["nikto"] = run_nikto_basic(url)
    print(json.dumps(result))


if __name__ == "__main__":
    main()


