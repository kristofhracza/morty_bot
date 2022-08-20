"""

Main file handling methods from other files
and audio related options

"""

# Libs
import os,time,discord,random
from unicodedata import name
from dotenv import load_dotenv
from discord.ext import commands
# Files
import yt,nsfw

# Load env variables
load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')
FFMPEG = os.getenv('FFMPEG_PATH')

# Colors
COLORS = {
  "green": "\033[1;32;40m",
  "red": "\033[1;31;40m",
  "white":"\033[1;37;40m",
  "grey":"\033[0;37;40m"
}

# Logging class
class Log():
    def __init__(self,cmd,guild,user,vc,time):
        self.cmd = cmd
        self.guild = guild
        self.user = user
        self.vc = vc
        self.time = time
    
    # Any command
    def action(self):
        print(f"{self.cmd} || {self.guild} || {self.user} || {self.vc} || {self.time}")
    
    # Errors
    def error(self):
        print(f"{COLORS['red']}ERROR: || {self.cmd} || {self.guild} || {self.user} || {self.vc} || {self.time}{COLORS['grey']}")


# Function to make embeds easier
def make_embed(title,desc,color,*args,**kwargs):
    embed = discord.Embed(
    title=title, 
    description=desc,
    color=color
    )
    return embed

# Initiate connection
bot = commands.Bot(command_prefix="$")
bot.remove_command("help")

# Connect
@bot.event
async def on_ready():
    os.system("cls||clear")
    await bot.change_presence(activity=discord. Activity(type=discord.ActivityType.listening, name='$help'))
    for guild in bot.guilds:
        print(f"{bot.user.name} is active in {guild.name}")

# Help command
@bot.command(name="help")
async def test(ctx):
    desc = """
    **Music**
     `play`,`pause`,`resume`,`stop / skip`,`leave`

     `$play [url to yt video]`
     `$play [keywords]`

    **General / fun**
        `pee-pee`,

    **NSFW**
     `nsfw`

    **Supported platforms**
      - `Youtube`
    """
    await(ctx.send(embed=make_embed("Help Menu",desc,discord.Color.teal())))

# leave VC
@bot.command(name="leave")
async def leave(ctx):
    user = ctx.message.author
    vc = user.voice.channel
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice == None:
        await(ctx.send(embed=make_embed("Error","I cannot leave, as I am not in a voice chat to begin with.",discord.Color.red())))
        if not user.voice:
            Log("LEAVE",ctx.guild,user,"N/A",time.ctime()).error()
        else:
            Log("LEAVE",ctx.guild,user,vc,time.ctime()).error()
    else:
        await ctx.voice_client.disconnect()
        # Check if user in VC
        if not user.voice:
            Log("LEAVE",ctx.guild,user,"N/A",time.ctime()).action()
        else:
            Log("LEAVE",ctx.guild,user,vc,time.ctime()).action()

# Play audio from URL YT
@bot.command(name="play")
async def play(ctx,*args):
    # Get the whole line of key words if not url
    url = ""
    for i in args:
        url += i
    # VC check
    if not ctx.message.author.voice:
        await(ctx.send(embed=make_embed("Error",f"{ctx.message.author.name} is not connected to a voice channel",discord.Color.red())))
        Log("PLAY",ctx.guild,ctx.message.author.name,"N/A",time.ctime()).error()
    else:
        # Connect to voice / stay in voice
        user = ctx.message.author
        vc = user.voice.channel
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice == None:
            await vc.connect()
        else:
            pass
        # Play yt
        try:
            player = await yt.YTDLSource.from_url(url, loop=bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f"Player error: {e} -- in {ctx.guild} -- {time.ctime()}") if e else None)
            # Send embed
            embed = discord.Embed(
            title="Now Playing", 
            description=player.title, 
            color=discord.Color.blue()
            )
            embed.set_thumbnail(url=player.thumbnail)
            await ctx.send(embed=embed) 
            Log("PLAY",ctx.guild,user,vc,time.ctime()).action()
        except discord.errors.ClientException:
            await(ctx.send(embed=make_embed("Music already playing","Wait until the music ends to play another audio",discord.Color.red())))
            Log("PLAY",ctx.guild,user,vc,time.ctime()).error()

# Pause audio
@bot.command(name="pause")
async def pause(ctx):
    try:
        ctx.voice_client.pause()
        await(ctx.send(embed=make_embed("Paused","Music is paused",discord.Color.orange())))
        Log("PAUSE",ctx.guild,ctx.message.author.name,"N/A",time.ctime()).action()
    except:
        await(ctx.send(embed=make_embed("No music","I am not playing any music at the moment",discord.Color.red())))
        Log("PAUSE",ctx.guild,ctx.message.author.name,"N/A",time.ctime()).error()

# Resume audio
@bot.command(name="resume")
async def resume(ctx):
    try:
        ctx.voice_client.resume()
        await(ctx.send(embed=make_embed("Resumed","Music is resumed",discord.Color.orange())))
        Log("RESUME",ctx.guild,ctx.message.author.name,"N/A",time.ctime()).action()
    except:
        await(ctx.send(embed=make_embed("No music","I am not playing any music at the moment",discord.Color.red())))
        Log("RESUME",ctx.guild,ctx.message.author.name,"N/A",time.ctime()).error()

# Stop / Skip audio
@bot.command(name="skip", aliases=["stop"])
async def resume(ctx):
    try:
        ctx.voice_client.stop()
        emoji = '\N{THUMBS UP SIGN}'
        await ctx.message.add_reaction(emoji)
        Log("SKIP",ctx.guild,ctx.message.author.name,"N/A",time.ctime()).action()
    except:
        await(ctx.send(embed=make_embed("No music","I am not playing any music at the moment",discord.Color.red())))
        Log("SKIP",ctx.guild,ctx.message.author.name,"N/A",time.ctime()).error()

# Pepe meter
@bot.command(name="pee-pee")
async def pepe(ctx):
    size = random.randrange(1,25)
    await ctx.send(embed=make_embed(f"{ctx.message.author.name}'s size",f"8{'='*size}D",discord.Color.gold()))
    Log("PEE-PEE",ctx.guild,ctx.message.author.name,"N/A",time.ctime()).action()

# NSFW
@bot.command(name="nsfw")
async def porn(ctx):
    # Send embed
    link = nsfw.get_gif()
    embed = discord.Embed(
    color=discord.Color.magenta()
    )
    embed.set_image(url=link)
    await ctx.send(embed=embed) 
    Log("NSFW",ctx.guild,ctx.message.author.name,"N/A",time.ctime()).action()

if __name__ == "__main__":
    bot.run(TOKEN)