"""

Logging actions and error
"""
# Colours for logging
COLORS = {
  "green": "\033[1;32;40m",
  "red": "\033[1;31;40m",
  "white":"\033[1;37;40m",
  "grey":"\033[0;37;40m"
}

class Log():
    def __init__(self,cmd,guild,user,time):
        self.cmd = cmd
        self.guild = guild
        self.user = user
        self.time = time
    
    # Any command
    def action(self):
        print(f"{self.cmd} || {self.guild} || {self.user} || {self.time}")
    
    # Errors
    def error(self):
        print(f"{COLORS['red']}ERROR: || {self.cmd} || {self.guild} || {self.user} || {self.time}{COLORS['grey']}")
