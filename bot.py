"""

Main file handling methods from other files
and audio related options

"""

# Libs
from helpers.loader import *
# Additional libs
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
    await bot.load_extension("cogs.fun")

async def main():
    # Load env variables
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    # Load cogs
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

# When going online
@bot.event
async def on_ready():
    os.system("cls||clear")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='$help'))
    print(f"{logger.Colors.CYAN}Start time:\t{time.ctime()}\n{logger.Colors.GREY}")
    for guild in bot.guilds:
        print(f"{logger.Colors.YELLOW}{guild.name}{logger.Colors.GREY}")
    print("\n")

# Help command
@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(title="Help menu",description="Command prefix: *$*",color=discord.Color.from_rgb(0,188,255))
    embed.add_field(name="Music",value="""```\rplay\nskip\nleave / esc\nqueue / q\nloadlist / ll\nshuffle\r```""")
    embed.add_field(name="Fun",value="""```\rnsfw\npee-pee\nmeme\r```""")
    await(ctx.send(embed=embed))

if __name__ == "__main__":
    asyncio.run(main())