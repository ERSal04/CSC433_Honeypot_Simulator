import geoip2.database
import os

class GeoIPEnricher:
    """
    Resolves IP addresses to physical locations using the MaxMind GeoLite2 database.
    """
    def __init__(self, db_path="data/GeoLite2-City.mmdb"):
        self.reader = None
        # Check if the database file actually exists before trying to load it
        if os.path.exists(db_path):
            try:
                self.reader = geoip2.database.Reader(db_path)
            except Exception as e:
                print(f"[GeoIP] Error loading DB: {e}")
        else:
            print(f"[GeoIP] Database not found at {db_path}")

    def get_location(self, ip_address):
        """
        Returns a dictionary with Country, City, Latitude, and Longitude.
        Returns None if the IP is private (local) or not found.
        """
        # Skip lookup for localhost or if DB didn't load
        if not self.reader or ip_address in ["127.0.0.1", "localhost", "::1"]:
            return None

        try:
            response = self.reader.city(ip_address)
            return {
                "country": response.country.name,
                "iso_code": response.country.iso_code,
                "city": response.city.name,
                "latitude": response.location.latitude,
                "longitude": response.location.longitude
            }
        except geoip2.errors.AddressNotFoundError:
            # IP is valid but not in the database
            return None
        except Exception:
            # Any other error
            return None