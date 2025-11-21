from core.emulation.commands.file_commands import FileCommands
from core.emulation.commands.system_commands import SystemCommands

class CommandProcessor:
    """Routes commands to apporpriate handlers"""

    def __init__(self, session):
        self.session = session
        self.file_cmds = FileCommands(session)
        self.system_cmds = SystemCommands(session)

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
        elif cmd in ["whoami", "id", "uname", "ps", "top"]:
            return self.system_cmds.handle(cmd, args)
        elif cmd == "history":
            return self._fake_history()
        else:
            return f"-bash: {cmd}: command not found"
        
    def _fake_history(self):
        """Return fake command history"""
        fake_history = [
            "1 ls -la",
            "2 cd /var/www",
            "3 cat config.php",
            "4 wget http://update.example.com/patch.sh",
            "5 history"
        ]
        return "\n".join(fake_history)