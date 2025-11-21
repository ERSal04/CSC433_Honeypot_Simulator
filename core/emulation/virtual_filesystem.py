# core/emulation/virtual_filesystem.py
import json
import os

class VirtualFileSystem:
    """Realistic virtual file system for honeypot"""

    def __init__(self, config_path="config/vfs_structure.json"):
        with open(config_path, 'r') as f:
            self.structure = json.load(f)
        self.files = self.structure.get("files", {})

    def _normalize_path(self, path):
        """Normalize path to use forward slashes (Linux style)"""
        return os.path.normpath(path).replace('\\', '/')

    def path_exists(self, path):
        """Check if a path exists in VFS"""
        path = self._normalize_path(path)
        return path in self.structure
    
    def is_directory(self, path):
        """Check if path is a directory"""
        path = self._normalize_path(path)
        if path in self.structure:
            return self.structure[path].get("type") == "directory"
        return False
    
    def list_directory(self, path):
        """List contents of a directory"""
        path = self._normalize_path(path)
        if path in self.structure and self.is_directory(path):
            return self.structure[path].get("contents", [])
        return None
    
    def read_file(self, path):
        """Read file contents"""
        # Normalize the path
        path = self._normalize_path(path)
        
        # Try exact match
        if path in self.files:
            return self.files[path]
        
        # Try with leading slash if not present
        if not path.startswith('/'):
            full_path = '/' + path
            if full_path in self.files:
                return self.files[full_path]
        
        # Try just filename - search all files
        for key in self.files:
            if key.endswith('/' + path) or key == path:
                return self.files[key]
            
        return None
    
    def resolve_path(self, current_dir, target):
        """Resolve relative paths to absolute paths"""
        if target.startswith('/'):
            result = self._normalize_path(target)
        else:
            result = self._normalize_path(os.path.join(current_dir, target))
        return result