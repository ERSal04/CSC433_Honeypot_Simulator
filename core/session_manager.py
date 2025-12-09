import socket
import uuid
import datetime
import json

class HoneypotSession:
    """Manages a single attacker session"""

    def __init__(self, client_socket, address):
        self.session_id = str(uuid.uuid4())
        self.client = client_socket
        self.address = address
        self.current_dir = "/root"
        self.username = None
        self.authenticated = False
        self.command_count = 0
        self.start_time = datetime.datetime.now()

    def log_event(self, event_type, data):
        """Log events in JSON format for Role B"""
        event = {
            "timestamp": datetime.datetime.now().isoformat(),
            "session_id": self.session_id,
            "ip": self.address[0],
            "port": self.address[1],
            "event_type": event_type,
            "data": data,
            "session_duration": (datetime.datetime.now() - self.start_time).total_seconds()
        }

        # Write to main log file
        with open("data/logs/honey.log", "a") as f:
            f.write(json.dumps(event) + "\n")

        # Also write to session-specific log
        session_log = f"data/logs/sessions/{self.session_id}.json"
        with open(session_log, "a") as f:
            f.write(json.dumps(event) + "\n")

    def send(self, message):
        """Safely send data to client"""
        try:
            if isinstance(message, str):
                message = message.encode('utf-8')
            if not isinstance(message, bytes):
                message = str(message).encode('utf-8')
            self.client.send(message + b"\r\n")
        except Exception as e:
            self.log_event("SEND_ERROR", {"error": str(e)})
        
    def receive_line(self):
        """Receive a line of input from attacker"""
        buffer = b""
        try:
            self.client.settimeout(300) # 5 minute timeout
            while True:
                char = self.client.recv(1)
                if not char or char in [b"\n", b"\r"]:
                    break
                #  Log every keystroke
                self.log_event("KEYSTROKE", {"char": char.decode("utf-8", errors="ignore")})
                buffer += char
        except socket.timeout:
            self.log_event("TIMEOUT", {"reason": "idle"})
            return None
        except Exception as e:
            self.log_event("RECEIVE_ERROR", {"error": str(e)})
            return None

        return buffer.decode("utf-8", errors="ignore").strip()
 