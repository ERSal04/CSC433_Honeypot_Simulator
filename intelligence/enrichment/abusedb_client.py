import requests
import logging

class AbuseDBClient:
    """
    Queries the AbuseIPDB API to check the reputation of an IP.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.logger = logging.getLogger("AbuseDB")
        self.base_url = "https://api.abuseipdb.com/api/v2/check"

    def check_ip(self, ip_address):
        """
        Returns reputation data: Abuse Confidence Score, Total Reports, etc.
        """
        if not self.api_key:
            return None

        # Don't check private IPs
        if ip_address.startswith("192.168.") or ip_address.startswith("10."):
            return None

        headers = {
            'Key': self.api_key,
            'Accept': 'application/json'
        }
        params = {
            'ipAddress': ip_address,
            'maxAgeInDays': 90
        }

        try:
            response = requests.get(self.base_url, headers=headers, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()['data']
                return {
                    "abuse_score": data.get('abuseConfidenceScore', 0),
                    "total_reports": data.get('totalReports', 0),
                    "last_reported": data.get('lastReportedAt', 'Never'),
                    "is_whitelisted": data.get('isWhitelisted', False)
                }
            else:
                self.logger.warning(f"AbuseIPDB Error: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"AbuseIPDB Request Failed: {e}")
            return None