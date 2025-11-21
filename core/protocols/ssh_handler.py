import datetime
from core.session_manager import HoneypotSession
from core.emulation.commands.command_processor import CommandProcessor

class SSHHandler:
    """Handles SSH protocol emulation"""

    def __init__(self, session: HoneypotSession):
        self.session = session
        self.processor = CommandProcessor(session)

    def handle(self):
        """Main SSH session handler"""
        self.session.log_event("CONNECTION_OPEN", {
            "protocol": "SSH",
            "banner": "OpenSSH_8.2p1"
        })

        # Send SSH banner
        self.session.client.send(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n")

        # Authenticate
        if self.authenticate():
            self.show_motd()
            self.interactive_shell()
        
        self.session.log_event("CONNECTION_CLOSE", {
            "commands_executed": self.session.command_count,
            "duration": (datetime.datetime.now() - self.session.start_time).total_seconds()
        })
        self.session.client.close()

    def authenticate(self):
        """Mock authentication - collect credentials"""
        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            self.session.send("login as: ")
            username = self.session.receive_line()
            if not username:
                return False

            self.session.send(f"{username}@honeypot's password: ")
            password = self.session.receive_line()
            if not password:
                return False
            
            self.session.log_event("AUTH_ATTEMPT", {
                "username": username,
                "password": password,
                "attempt": attempts + 1,
                "success": False
            })

            attempts += 1

            # Accept after 2 failed attempts OR weak credentials
            if attempts >= 2 or self._is_weak_credential(username, password):
                self.session.username = username
                self.session.authenticated = True
                self.session.log_event("AUTH_SUCCESS", {
                    "username": username,
                    "attempts": attempts 
                })
                return True
            else: 
                self.session.send("Permission denied, please try again.")

        self.session.send("Too many authenticated failures")
        self.session.log_event("AUTH_FAILURE", {"reason": "max_attempts"})
        return False
        
    def _is_weak_credential(self, username, password):
        """Check if credentials are in common weak list"""
        weak_combos = [
            ("root", "root"),
            ("root", "123456"),
            ("root", "password"),
            ("admin", "admin"),
            ("admin", "password"),
            ("user", "user"),
        ]
        return (username, password) in weak_combos
    
    def show_motd(self):
        """Display Message of the Day"""
        motd = """
Welcome to Ubuntu 20.04.5 LTS (GNU/Linux 5.4.0-128-generic x86_64)

* Documentation:  https://help.ubuntu.com
* Management:     https://landscape.canonical.com
* Support:        https://ubuntu.com/advantage

⚠️  WARNING: This system is monitored. Unauthorized access is prohibited.

Last login: Wed Nov 15 14:32:11 2025 from 10.0.0.5
"""
        self.session.send(motd)

    def interactive_shell(self):
        """The fake interactive shell"""
        while True:
            prompt = f"{self.session.username}@honeypot:{self.session.current_dir}# "
            self.session.send(prompt)

            # Get command
            command = self.session.receive_line()
            if not command:
                break
            
            self.session.command_count += 1
            self.session.log_event("COMMAND", {
                "command": command,
                "cwd": self.session.current_dir
            })

            # Check for exit commands
            if command.lower() in ["exit", "logout", "quit"]:
                self.session.send("logout")
                break

            # Process command
            output = self.processor.execute(command)
            if output:
                self.session.send(output)