import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.honeypot_server import HoneypotServer

def main():
    # Create necessary directories
    os.makedirs("data/logs/session", exist_ok=True)

    # Start the honeypot
    server = HoneypotServer(bind_ip="127.0.0.1", ssh_port=2222)
    server.start()

if __name__ == "__main__":
    main()