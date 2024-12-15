from helpers.loader import *

import os
from dotenv import load_dotenv


# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)
bot.remove_command("help")


# Deployment
async def load_extensions():
    await bot.load_extension("cogs.music")

async def main():
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

# Startup
@bot.event
async def on_ready():
    os.system("cls||clear")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='$help'))
    print(f"Start time: {time.ctime()}\n")
    for guild in bot.guilds:
        print(f"{guild.name}")
    print("\n")


# Help command
@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(title="Help Menu",description="Command prefix: *$*",color=discord.Color.from_rgb(0,188,255))
    embed.add_field(name="Music",value="""```\rplay\nskip\nleave / esc\nqueue / q\nloadlist / ll\nshuffle\r```""")
    await(ctx.send(embed=embed))

if __name__ == "__main__":
    asyncio.run(main())