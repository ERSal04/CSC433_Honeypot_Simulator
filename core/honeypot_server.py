import socket
import threading
from core.session_manager import HoneypotSession
from core.protocols.ssh_handler import SSHHandler

class HoneypotServer:
    """Main honeypot server - manages listeners"""

    def __init__(self, bind_ip="0.0.0.0", ssh_port=2222):
        self.bind_ip = bind_ip
        self.ssh_port = ssh_port
        self.running = False

    def start(self):
        """Start all protocol listeners"""
        self.running = True

        # Start SSH listener
        ssh_thread = threading.Thread(target=self._start_ssh_listener)
        ssh_thread.daemon = True
        ssh_thread.start()

        print(f"[*] Honeypot SSH listener on {self.bind_ip}:{self.ssh_port}")
        print(f"[*] Logs writing to: data/logs/honey.log")
        print(f"[*] Press Ctrl+c to stop\n")

        try:
            while self.running:
                pass
        except KeyboardInterrupt:
            print("\n[*] Shutting down honeypot...")
            self.running = False

    def _start_ssh_listener(self):
        """SSH protocol listener"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.bind_ip, self.ssh_port))
        server.listen(5)

        while self.running:
            try:
                client, addr = server.accept()
                print(f"[!] SSH Connection from: {addr[0]}:{addr[1]}")

                # Create session and handler
                session = HoneypotSession(client, addr)
                handler = SSHHandler(session)

                # Handle in separate thread
                thread = threading.Thread(target=handler.handle)
                thread.daemon = True
                thread.start()
            except Exception as e:
                if self.running:
                    print(f"[!] Error accepting connection: {e}")
        server.close()