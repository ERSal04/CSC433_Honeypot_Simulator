class SystemCommands:
    """Handles system information commands"""

    def __init__(self, session):
        self.session = session

    def handle(self, cmd, args):
        """Route system commands"""
        if cmd == "whoami":
            return self.session.username or "root"
        elif cmd == "id":
            return "uid-0(root) gid=0(root) groups=0(root)"
        elif cmd == "uname":
            return self._uname(args)
        elif cmd == "ps":
            return self._ps()
        elif cmd == "top":
            return "top - use 'ps' instead"
        return ""
    
    def _uname(self, args):
        """Fake uname output"""
        if "-a" in args:
            return "Linux honeypot 5.4.0-128generic #144-Ubuntu SMP x86_64 GNU/Linux"
        return "Linux"
    
    def _ps(self):
        """Fake process list"""
        processess = """PID TTY          TIME CMD
    1 ?        00:00:02 systemd
  445 ?        00:00:00 sshd
  892 ?        00:00:01 nginx
 1024 ?        00:00:00 mysql
 1337 pts/0    00:00:00 bash
 1445 pts/0    00:00:00 ps"""
        return processess