from requests import get, put


class GoDaddyApiService:
    """
    This class is designed to integrate with the the godaddy API
    To initialise this class you will need to provide it with the api_key and secret key for your account
    see docs: https://developer.godaddy.com/getstarted
    """

    def __init__(self, api_key, secret_key, dns_records):
        self.api_key = api_key
        self.secret_key = secret_key
        self.dns_records = dns_records

    def get_dns_records_from_godaddy(self) -> list:
        """
        This will get the dns records stored in a GoDaddy DNS entry.
            [{"domain":"domain.co.uk", "dns_record_type": "A", "name":"DNSNameRecord"},
            {"domain":"domain.co.uk", "dns_record_type": "AAAA", "name":"DNSNameRecord"}]
        """

        headers = {"Authorization": "sso-key {}:{}".format(self.api_key, self.secret_key)}
        dns_records = []
        for dns_record in self.dns_records:
            url = "https://api.godaddy.com/v1/domains/{}/records/{}/{}".format(dns_record["domain"],
                                                                               dns_record["dns_record_type"],
                                                                               dns_record["name"])
            dns_records.append(get(url, headers=headers).text)
        return dns_records


    def update_dns_records_to_godaddy(self):

        headers = {"Authorization": "sso-key {}:{}".format(self.api_key, self.secret_key),
                   "body": [
                       {
                           "data": "string",
                           "port": 65535,
                           "priority": 0,
                           "protocol": "string",
                           "service": "string",
                           "ttl": 0
                       }
                   ]
                   }
        dns_records = []
        for dns_record in self.dns_records:
            url = "https://api.godaddy.com/v1/domains/{}/records/{}/{}".format(dns_record["domain"],
                                                                               dns_record["dns_record_type"],
                                                                               dns_record["name"])
            put(url, headers=headers).text()
        return dns_records