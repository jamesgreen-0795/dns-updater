from go_daddy_api_service import GoDaddyApiService
from requests import get
import ast


def validate_if_ip_needs_updating(dns_records, host_ips):
    ipv4_needs_updating = None
    ipv6_needs_updating = None

    for dns_record in range(len(dns_records)):
        dns_record_type = ast.literal_eval(dns_records[dns_record])[0]["type"]
        if dns_record_type == "A":
            if not ast.literal_eval(dns_records[dns_record])[0]["data"] == host_ips["ipv4"] is False:
                print("ipv4 address does NOT match record in DNS")
                ipv4_needs_updating = True
        if dns_record_type == "AAAA":
            if not ast.literal_eval(dns_records[dns_record])[0]["data"] == host_ips["ipv6"] is False:
                print("ipv6 address does NOT match record in DNS")
                ipv6_needs_updating = True

    if ipv4_needs_updating or ipv6_needs_updating:
        return True
    if ipv4_needs_updating is False and ipv6_needs_updating is False:
        return False


def get_host_device_ip_address() -> dict:
    current_ipv4_address = get('https://api.ipify.org').text
    current_ipv6_address = get('https://api64.ipify.org').text
    return {"ipv4": current_ipv4_address, "ipv6": current_ipv6_address}


def get_dns_records_from_my_dns():
    dns_records = client.get_dns_records_from_godaddy()
    return dns_records


def update_dns():
    client.update_dns_records_to_godaddy()


if __name__ == "__main__":
    client = GoDaddyApiService(
        api_key="eoM9SU7a971H_2WF28yMJ4rKSJc9KEkYHmA",
        secret_key="EmVTavbv6jJq9r9BeVaEJD",
        dns_records=[{"domain": "greenjames.co.uk", "dns_record_type": "A", "name": "camera"},
                   {"domain": "greenjames.co.uk", "dns_record_type": "AAAA", "name": "camera"}])

    dns_records = get_dns_records_from_my_dns()
    host_ips = get_host_device_ip_address()
    result = validate_if_ip_needs_updating(dns_records, host_ips)
    if result:
        update_dns()
    if result is False:
        print("DNS records are correct nothing to do")
