from core.emulation.virtual_filesystem import VirtualFileSystem

class FileCommands:
    """Handles file-related commands"""
    
    def __init__(self, session):
        self.session = session
        try:
            self.vfs = VirtualFileSystem()
        except FileNotFoundError:
            print("[!] Warning: VFS config not found, using fallback")
            self.vfs = None
    
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
        """Fake ls output with flags support"""
        if not self.vfs:
            return "Documents  Downloads  passwords.txt"
        
        # Parse flags
        show_hidden = "-a" in args or "-la" in args or "-al" in args
        long_format = "-l" in args or "-la" in args or "-al" in args
        
        # Get directory to list
        path = self.session.current_dir
        
        # Get contents
        contents = self.vfs.list_directory(path)
        if contents is None:
            return f"ls: cannot access '{path}': No such file or directory"
        
        # Filter hidden files
        if not show_hidden:
            contents = [f for f in contents if not f.startswith('.')]
        
        # Format output
        if long_format:
            output = []
            for item in contents:
                full_path = f"{path}/{item}".replace('//', '/')
                if self.vfs.is_directory(full_path):
                    output.append(f"drwxr-xr-x 2 root root 4096 Nov 15 14:32 {item}")
                else:
                    output.append(f"-rw-r--r-- 1 root root 1234 Nov 15 14:32 {item}")
            return "\n".join(output)
        else:
            return "  ".join(contents)
    
    def _cd(self, args):
        """Change directory"""
        if not self.vfs:
            return ""
            
        if not args:
            self.session.current_dir = "/root"
            return ""
        
        target = args[0]
        
        # Handle special cases
        if target == "..":
            # Go up one directory
            if self.session.current_dir != "/":
                self.session.current_dir = "/".join(self.session.current_dir.split("/")[:-1]) or "/"
            return ""
        elif target == ".":
            return ""
        
        # Resolve path
        new_path = self.vfs.resolve_path(self.session.current_dir, target)
        
        if self.vfs.is_directory(new_path):
            self.session.current_dir = new_path
            return ""
        else:
            return f"-bash: cd: {target}: No such file or directory"
    
    def _cat(self, args):
        """Display file contents"""
        if not args:
            return "cat: missing operand"
        
        if not self.vfs:
            # Fallback honeyfiles
            honeyfiles = {
                "passwords.txt": "admin:P@ssw0rd123\nroot:SuperSecret99",
            }
            filename = args[0]
            return honeyfiles.get(filename, f"cat: {filename}: No such file or directory")
        
        filename = args[0]
        
        # Try to resolve as absolute path first
        if filename.startswith('/'):
            file_path = filename
        else:
            # Relative to current directory
            file_path = f"{self.session.current_dir}/{filename}".replace('//', '/')
        
        # Try to read from VFS
        content = self.vfs.read_file(file_path)
        
        # If not found, try just the filename
        if content is None:
            content = self.vfs.read_file(filename)
        
        if content:
            return content
        else:
            return f"cat: {filename}: No such file or directory"