import socket

class ReverseDNS:
    """
    Performs Reverse DNS lookups to resolve IP addresses to Hostnames.
    Example: 8.8.8.8 -> dns.google
    """
    
    @staticmethod
    def lookup(ip_address):
        """
        Performs a reverse DNS lookup.
        Returns the hostname if found, otherwise returns 'Unknown'.
        """
        try:
            # socket.gethostbyaddr returns a tuple (hostname, aliaslist, ipaddrlist)
            # We only care about the hostname (the first element)
            hostname, _, _ = socket.gethostbyaddr(ip_address)
            return hostname
        except socket.herror:
            # Expected error if the IP has no DNS record
            return "Unknown"
        except Exception:
            # Catch-all for network timeouts or other errors
            return "Resolution Error"