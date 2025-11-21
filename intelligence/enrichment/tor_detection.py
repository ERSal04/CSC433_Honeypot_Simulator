import requests
import threading
import time

class TorDetector:
    """
    Checks if an IP address belongs to a known Tor Exit Node.
    """
    def __init__(self):
        self.exit_nodes = set()
        self.url = "https://check.torproject.org/torbulkexitlist"
        self.last_updated = 0
        
        # Start background update
        self.update_list()

    def update_list(self):
        """Downloads the latest list of exit nodes."""
        def _worker():
            try:
                response = requests.get(self.url, timeout=10)
                if response.status_code == 200:
                    # Split by new line and add to set for fast lookup
                    self.exit_nodes = set(response.text.splitlines())
                    self.last_updated = time.time()
                    print(f"[TorDetector] Updated list: {len(self.exit_nodes)} nodes.")
            except Exception as e:
                print(f"[TorDetector] Update failed: {e}")

        # Run in a thread so we don't block startup
        t = threading.Thread(target=_worker, daemon=True)
        t.start()

    def is_tor(self, ip_address):
        """Returns True if the IP is a known Tor exit node."""
        # Refresh list if it's older than 24 hours (86400 seconds)
        if time.time() - self.last_updated > 86400:
            self.update_list()
            
        return ip_address in self.exit_nodes