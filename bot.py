import os

from dotenv import load_dotenv
from helpers.loader import *

# Initialise bot with intent
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)
bot.remove_command("help")


async def load_extensions():
    """Loads all cogs"""
    await bot.load_extension("cogs.music")


@bot.event
async def on_ready():
    """Triggered when  the bot goes online"""
    os.system("cls || clear")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="$help"))

    print(f"Start time: {time.ctime()}\n")
    for guild in bot.guilds:
        print(f"{guild.name}")
    print("\n")


@bot.command(name="help")
async def help(ctx):
    """Sends embed for help command"""
    embed = discord.Embed(title="Help Menu", description="Command prefix: *$*", color=discord.Color.from_rgb(0,188,255))
    embed.add_field(
        name="Music Commands", 
        value=("""
            `play` `loadlist` `skip` `leave` `shuffle` `queue`
        """)
    )

    await(ctx.send(embed=embed))


async def main():
    """Setup the environment"""
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())