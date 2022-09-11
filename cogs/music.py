"""

Cog that handles music queues and playing audio
Also controls states such as: play, stop, skip, leave

Queue Visualisation:

Q = {
    ID_1 = [[player,url]],
    ID_2 = [],    
    ID_3 = [],    
}

Navigation:
Q[i] = [[player,url]]
    Q[i][0] = [player,url]
        Q[i][0][0] = player
        Q[i][0][1] = url

"""
# Libs
import helpers.str as str_conv
from helpers.loader import *
# Additional libs
import yt

class Music(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.queue = {}

    # Setup queue structure on start
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            self.queue[guild.id] = []

    # Handle the music queue
    def queue_handle(self,ctx):
        if not self.queue[ctx.guild.id]:
            pass
        else:
            coro = self.play(ctx,self.queue[ctx.guild.id][0])
            to_run = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
            try:
                to_run.result()
                if self.queue[ctx.guild.id][0]:
                    self.queue[ctx.guild.id].pop(0)
            except Exception as e:
                print(e)

    # Playing music
    @commands.command(name="play")
    async def play(self,ctx: commands.Context,*args):
        logger.Log("PLAY",ctx.guild,ctx.message.author.name,time.ctime()).action()
        # Key words or url
        if type(args[0]) == str:
            url = " ".join(str(i) for i in args)
        else:
            url = args[0][1]
        # VC check
        if not ctx.message.author.voice:
            await(ctx.send(embed=make_embed("Error",f"{ctx.message.author.name} is not connected to a voice channel",discord.Color.from_rgb(*EMBED_COLORS["red"]))))
        else:
            # Connect to voice / stay in voice
            user = ctx.message.author
            vc = user.voice.channel
            if ctx.voice_client == None:
                await vc.connect()
            else:
                pass
            # Play audio
            player = await yt.YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            try:
                ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.queue_handle(ctx), self.bot.loop))
                # Send embed
                embed = discord.Embed(title="Now playing", color=discord.Color.from_rgb(*EMBED_COLORS["blue"]),description=str_conv.conv(player.title))
                await ctx.send(embed=embed) 
            except discord.errors.ClientException:
                self.queue[ctx.guild.id].append([player,url])
                embed = discord.Embed(title="Added to queue", description=player.title, color=discord.Color.from_rgb(*EMBED_COLORS["blue"]))
                nl = "\n"
                embed.add_field(name="Queue:", value=
                f"{f' {nl} '.join(str_conv.conv(str(s[0].title)) for s in self.queue[ctx.guild.id])}",
                inline=False)
                await(ctx.send(embed=embed))

    @commands.command(name="queue", aliases=["q"])
    async def display_queue(self,ctx: commands.Context):
        if len(self.queue[ctx.guild.id]) > 0:
            print("Q")
            embed = discord.Embed(title="Tracks in the queue",color=discord.Color.from_rgb(*EMBED_COLORS["blue"]))
            nl = "\n"
            embed.add_field(name="\u200b",value=f"{f' {nl} '.join(str_conv.conv(str(s[0].title)) for s in self.queue[ctx.guild.id])}",inline=False)
            await(ctx.send(embed=embed))
        else:
            print("N")
            embed = discord.Embed(title="There's nothing in the queue",color=discord.Color.from_rgb(*EMBED_COLORS["red"]))
            await(ctx.send(embed=embed))

    # Stop / Skip audio
    @commands.command(name="skip", aliases=["stop"])
    async def skip(self,ctx: commands.Context):
        logger.Log("SKIP",ctx.guild,ctx.message.author.name,time.ctime()).action()
        await ctx.voice_client.stop()
        asyncio.run_coroutine_threadsafe(self.queue_handle(ctx.guild.id), self.bot.loop)

    # Leave
    @commands.command(name="leave")
    async def leave(self,ctx: commands.Context):
        logger.Log("LEAVE",ctx.guild,ctx.message.author.name,time.ctime()).action()
        await ctx.guild.voice_client.disconnect()

async def setup(bot):
    await bot.add_cog(Music(bot))