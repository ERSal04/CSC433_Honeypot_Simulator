import time

class NetworkCommands:
    """Handles network-related commands"""
    
    def __init__(self, session):
        self.session = session
    
    def handle(self, cmd, args):
        """Route network commands"""
        if cmd == "wget":
            return self._wget(args)
        elif cmd == "curl":
            return self._curl(args)
        elif cmd == "ping":
            return self._ping(args)
        return ""
    
    def _wget(self, args):
        """Fake wget - log the URL"""
        if not args:
            return "wget: missing URL"
        
        url = args[0]
        
        # Log the malware URL
        self.session.log_event("WGET_ATTEMPT", {
            "url": url,
            "command": f"wget {' '.join(args)}"
        })
        
        # Fake download progress
        filename = url.split('/')[-1] or "index.html"
        return f"""--2025-11-20 14:32:15--  {url}
Resolving {url.split('/')[2]}... 203.0.113.50
Connecting to {url.split('/')[2]}|203.0.113.50|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 15234 (15K) [application/octet-stream]
Saving to: '{filename}'

{filename}          100%[===================>]  14.88K  --.-KB/s    in 0.001s  

2025-11-20 14:32:16 (12.3 MB/s) - '{filename}' saved [15234/15234]"""
    
    def _curl(self, args):
        """Fake curl"""
        if not args:
            return "curl: try 'curl --help' for more information"
        
        url = args[0]
        
        # Log the attempt
        self.session.log_event("CURL_ATTEMPT", {
            "url": url,
            "command": f"curl {' '.join(args)}"
        })
        
        return f"<html><body>Fake response from {url}</body></html>"
    
    def _ping(self, args):
        """Fake ping"""
        if not args:
            return "ping: usage error: Destination address required"
        
        host = args[0]
        return f"""PING {host} (203.0.113.10) 56(84) bytes of data.
64 bytes from {host} (203.0.113.10): icmp_seq=1 ttl=64 time=0.123 ms
64 bytes from {host} (203.0.113.10): icmp_seq=2 ttl=64 time=0.098 ms
64 bytes from {host} (203.0.113.10): icmp_seq=3 ttl=64 time=0.115 ms
^C
--- {host} ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 0.098/0.112/0.123/0.010 ms"""