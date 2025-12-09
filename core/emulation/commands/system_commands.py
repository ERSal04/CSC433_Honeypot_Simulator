# core/emulation/commands/system_commands.py

class SystemCommands:
    """Handles system information commands"""
    
    def __init__(self, session):
        self.session = session
    
    def handle(self, cmd, args):
        """Route system commands"""
        if cmd == "whoami":
            return self.session.username or "root"
        elif cmd == "id":
            return "uid=0(root) gid=0(root) groups=0(root)"
        elif cmd == "uname":
            return self._uname(args)
        elif cmd == "ps":
            return self._ps()
        elif cmd == "top":
            return "top - 14:32:11 up 45 days,  3:21,  1 user,  load average: 0.15, 0.10, 0.08"
        elif cmd == "ifconfig":
            return self._ifconfig()
        elif cmd == "netstat":
            return self._netstat()
        elif cmd == "hostname":
            return "ubuntu-server"
        elif cmd == "uptime":
            return "14:32:11 up 45 days,  3:21,  1 user,  load average: 0.15, 0.10, 0.08"
        return ""
    
    def _uname(self, args):
        """Fake uname output"""
        if not args or "-a" in args:
            return "Linux honeypot 5.4.0-128-generic #144-Ubuntu SMP Tue Sep 20 11:00:00 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux"
        elif "-r" in args:
            return "5.4.0-128-generic"
        elif "-s" in args:
            return "Linux"
        return "Linux"
    
    def _ps(self):
        """Fake process list"""
        processes = """  PID TTY          TIME CMD
    1 ?        00:00:02 systemd
  445 ?        00:00:00 sshd
  892 ?        00:00:01 nginx
  893 ?        00:00:00 nginx
 1024 ?        00:00:12 mysqld
 1337 pts/0    00:00:00 bash
 1445 pts/0    00:00:00 ps"""
        return processes
    
    def _ifconfig(self):
        """Fake network interface info"""
        return """eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::a00:27ff:fe4e:66a1  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:4e:66:a1  txqueuelen 1000  (Ethernet)
        RX packets 12845  bytes 8924561 (8.9 MB)
        TX packets 8421  bytes 1245789 (1.2 MB)

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)"""
    
    def _netstat(self):
        """Fake network connections"""
        return """Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 192.168.1.100:22        203.0.113.5:54321       ESTABLISHED
tcp        0      0 192.168.1.100:80        198.51.100.23:43210     TIME_WAIT  
tcp        0      0 192.168.1.100:3306      192.168.1.50:51234      ESTABLISHED"""