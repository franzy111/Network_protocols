import os
import re
import requests
from prettytable import PrettyTable
import argparse


def tracert(ip):
    out = os.popen(f"tracert -4 -d {ip}")
    stdout = out.read()
    reg = re.compile("\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}")
    return reg.findall(stdout)[1:]


def info_about_ip(query):
    ans = requests.get(f"http://ip-api.com/json/{query}?fields=27137")
    if ans.status_code == 200:
        info = ans.json()
        if info["status"] == "success":
            if info["as"] != "":
                return [info["query"], info["as"].split()[0], info["country"], info["isp"]]
            else:
                return [info["query"], "Nil", info["country"], info["isp"]]
        else:
            return [query, "local", "local", "local"]
    else:
        return [query, "error", "error", "error"]


def pretty_table(ip):
    table = PrettyTable(["hop", "ip", "as", "country", "provider"])
    for i, record in enumerate(ip, start=1):
        table.add_row([i] + record)
    print(table)


def main():
    parser = argparse.ArgumentParser(description="The script that runs tracert and receives information on each hop")
    parser.add_argument("target_ip", help="Target IP address/DNS name")
    args = parser.parse_args()
    all_ip = tracert(args.target_ip)
    info = (info_about_ip(ip) for ip in all_ip)
    pretty_table(info)


if __name__ == "__main__":
    main()
