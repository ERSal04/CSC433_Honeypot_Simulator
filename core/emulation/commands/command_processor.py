# core/emulation/command_processor.py
from core.emulation.commands.file_commands import FileCommands
from core.emulation.commands.system_commands import SystemCommands
from core.emulation.commands.network_commands import NetworkCommands

class CommandProcessor:
    """Routes commands to appropriate handlers"""
    
    def __init__(self, session):
        self.session = session
        self.file_cmds = FileCommands(session)
        self.system_cmds = SystemCommands(session)
        self.network_cmds = NetworkCommands(session)
    
    def execute(self, command_line):
        """Parse and execute a command"""
        parts = command_line.strip().split()
        if not parts:
            return ""
        
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        # Route to appropriate handler
        if cmd in ["ls", "cat", "cd", "pwd"]:
            return self.file_cmds.handle(cmd, args)
        elif cmd in ["whoami", "id", "uname", "ps", "top", "ifconfig", "netstat", "hostname", "uptime"]:
            return self.system_cmds.handle(cmd, args)
        elif cmd in ["wget", "curl", "ping"]:
            return self.network_cmds.handle(cmd, args)
        elif cmd == "history":
            return self._fake_history()
        elif cmd == "clear":
            return "\n" * 50  # Simulate screen clear
        else:
            return f"-bash: {cmd}: command not found"
    
    def _fake_history(self):
        """Return fake command history"""
        fake_history = [
            "  1  ls -la",
            "  2  cd /var/www",
            "  3  cat config.php",
            "  4  mysql -u root -p",
            "  5  wget http://updates.example.com/patch.sh",
            "  6  chmod +x patch.sh",
            "  7  ./patch.sh",
            "  8  rm patch.sh",
            "  9  history"
        ]
        return "\n".join(fake_history)