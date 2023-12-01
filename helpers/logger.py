"""

Logging module

"""
# Colours for logging
class Colors:
    GREEN = "\033[1;32;40m"
    RED = "\33[31m"
    WHITE = "\033[1;37;40m"
    GREY = "\033[0;37;40m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    YELLOW = "\33[93m"

# Logger class
class Log():
    def __init__(self,cmd,guild,user,time):
        self.cmd = cmd
        self.guild = guild
        self.user = user
        self.time = time
    
    # Any command
    def action(self):
        self.time = f"{Colors.WHITE}{self.time}{Colors.GREY}"
        self.cmd = f"{Colors.GREEN}{self.cmd}{Colors.GREY} "
        self.user = f"{Colors.CYAN}{self.user}{Colors.GREY}"
        self.guild = f"{Colors.BLUE}{self.guild}{Colors.GREY}"
        print(f"{self.time}\t{self.cmd}\t{self.user}\t{self.guild}")

    # Errors
    def error(self):
        print(f"{Colors.RED}{self.time}\t{self.cmd}\t{self.user}\t{self.guild}{Colors.GREY}")

    # Errors with messages
    def error_message(self,msg):
        print(f"\n{Colors.RED}{self.time}\t{self.cmd}\t{self.user}\t{self.guild}\t{msg}\n{Colors.GREY}")
