class Log():
    """Logger for different scenarios"""

    def __init__(self, cmd, guild, user, time):
        self.cmd = cmd
        self.guild = guild
        self.user = user
        self.time = time

    def action(self):
        print(f"{self.time}\t{self.cmd}\t{self.user}\t{self.guild}")

    def error(self):
        print(f"{self.time}\t{self.cmd}\t{self.user}\t{self.guild}")

    def error_message(self, msg):
        print(f"\n{self.time}\t{self.cmd}\t{self.user}\t{self.guild}\t{msg}\n")
