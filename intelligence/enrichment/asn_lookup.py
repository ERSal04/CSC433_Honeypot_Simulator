import geoip2.database
import os

class ASNLookup:
    """
    Identifies the Autonomous System Number (ASN) and Organization
    associated with an IP address.
    """
    def __init__(self, db_path="data/GeoLite2-ASN.mmdb"):
        self.reader = None
        if os.path.exists(db_path):
            try:
                self.reader = geoip2.database.Reader(db_path)
            except Exception as e:
                print(f"[ASN] Error loading DB: {e}")
        else:
            # It is okay if this is missing, we just won't return ASN data
            print(f"[ASN] Database not found at {db_path}")

    def lookup(self, ip_address):
        """
        Returns a dictionary with the ASN and Organization name.
        """
        if not self.reader or ip_address in ["127.0.0.1", "localhost"]:
            return {"asn": "Unknown", "org": "Unknown"}

        try:
            response = self.reader.asn(ip_address)
            return {
                "asn": f"AS{response.autonomous_system_number}",
                "org": response.autonomous_system_organization
            }
        except geoip2.errors.AddressNotFoundError:
            return {"asn": "Unknown", "org": "Unknown"}
        except Exception:
            return {"asn": "Unknown", "org": "Unknown"}