"""
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
import random
import helpers.yt as yt

from helpers.loader import *

async def vc_check_error(ctx):
    """Utility function to check for user presence in the voice channel"""
    if not ctx.message.author.voice:
        await(ctx.send(embed=discord.Embed(
            title="Error", 
            description=f"{ctx.message.author.name} is not connected to a voice channel", 
            color=discord.Color.from_rgb(*EMBED_COLORS["red"]))
            )
        )
        return False
    else:
        return True

class Music(commands.Cog):
    """Music handler"""

    def __init__(self,bot):
        self.bot = bot
        self.queue = {}

    @commands.Cog.listener()
    async def on_ready(self):
        """Setup queue structure for every server on start"""
        for guild in self.bot.guilds:
            self.queue[guild.id] = []


    def queue_handle(self,ctx):
        """Queue logic and handling"""
        if self.queue[ctx.guild.id]:
            coro = self.play(ctx, self.queue[ctx.guild.id][0], queue_handle=True)
            to_run = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
            try:
                to_run.result()
                if self.queue[ctx.guild.id][0]:
                    self.queue[ctx.guild.id].pop(0)
            except Exception as e:
                logger.Log("QUEUE", ctx.guild,ctx.message.author.name, time.ctime()).error_message(e)


    @commands.command(name="play",aliases=["PLAY"])
    async def play(self,ctx: commands.Context,*args,**kwargs):
        """Plays the 0th element in the queue"""
        # Check for trigger
        if kwargs and kwargs["queue_handle"] == True:
            logger.Log("QUEUE", ctx.guild,ctx.message.author.name, time.ctime()).action()
        else:
            logger.Log("PLAY", ctx.guild,ctx.message.author.name, time.ctime()).action()
       
        # VC user check
        if await vc_check_error(ctx) == False: 
            return

        # Check if URL or keyword search is needed
        if type(args[0]) == str:
            url = " ".join(str(i) for i in args)
        else:
            url = args[0][1]
       
        # Join user voice channel
        user = ctx.message.author
        vc = user.voice.channel
        if ctx.voice_client == None:
            await vc.connect()

        # Make player object
        player = await yt.YTDLSource.from_url(url, loop=self.bot.loop, stream=True)

        # Play / queue music based on error (not optimal but works 100% of the time)
        try:
            ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.queue_handle(ctx), self.bot.loop))
            await ctx.send(embed=discord.Embed(
                title="Now playing", 
                color=discord.Color.from_rgb(*EMBED_COLORS["blue"]),
                description=md_conv(player.title))
            ) 
        except discord.errors.ClientException:
            self.queue[ctx.guild.id].append([player,url])
            await(ctx.send(embed=discord.Embed(
                title="Added to queue", 
                description=player.title, 
                color=discord.Color.from_rgb(*EMBED_COLORS["blue"]))
                )
            )


    @commands.command(name="loadlist", aliases=["ll","LOADLIST","LL"])
    async def play_list(self, ctx: commands.Context, *args):
        """Loads playlist and adds each track to the queue"""
        logger.Log("LIST",ctx.guild,ctx.message.author.name,time.ctime()).action()
        
        # VC user check
        if await vc_check_error(ctx) == False: 
            return

        # Loop over the list and query each song individually
        data = await yt.YTDLSource.from_list(args[0], self.queue,ctx.guild.id, loop=self.bot.loop, stream=True)
        embed = discord.Embed(
            title=f"Tracks from *{md_conv(data['title'])}* are queued", 
            color=discord.Color.from_rgb(*EMBED_COLORS["blue"])
        )
        
        nl = "\n"
        embed.add_field(name="Current queue:", value=f"{nl}{nl.join(str(md_conv(s[0].title)) for s in self.queue[ctx.guild.id])}", inline=False)
        
        await(ctx.send(embed=embed))


    @commands.command(name="queue", aliases=["q","QUEUE","Q"])
    async def display_queue(self,ctx: commands.Context):
        """Show the queue"""
        logger.Log("QUEUE",ctx.guild,ctx.message.author.name,time.ctime()).action()

        if len(self.queue[ctx.guild.id]) > 0:
            embed = discord.Embed(
                title="Tracks in the queue",
                color=discord.Color.from_rgb(*EMBED_COLORS["blue"])
            )
            nl = "\n"
            embed.add_field(name="\u200b", value=f"{nl}{nl.join(str(md_conv(s[0].title)) for s in self.queue[ctx.guild.id])}", inline=False)
            await(ctx.send(embed=embed))
        else:
            await(ctx.send(embed=discord.Embed(
                title="There's nothing in the queue",
                color=discord.Color.from_rgb(*EMBED_COLORS["red"]))
                )
            )


    @commands.command(name="shuffle", aliases=["SHUFFLE"])
    async def shuffle_list(self,ctx: commands.Context):
        """Randomises queue"""
        logger.Log("SHUFFLE", ctx.guild,ctx.message.author.name, time.ctime()).action()

        # VC user check
        if await vc_check_error(ctx) == False: 
            return
        random.shuffle(self.queue[ctx.guild.id])


    @commands.command(name="skip", aliases=["stop","SKIP","STOP"])
    async def skip(self,ctx: commands.Context):
        """Skips current music"""
        logger.Log("SKIP", ctx.guild,ctx.message.author.name, time.ctime()).action()
        
        # VC user check
        if await vc_check_error(ctx) == False: 
            return

        await ctx.guild.voice_client.stop()
        
        asyncio.run_coroutine_threadsafe(self.queue_handle(ctx.guild.id), self.bot.loop)
        logger.Log("SKIP", ctx.guild,ctx.message.author.name, time.ctime()).action()


    @commands.command(name="leave",aliases=["esc","LEAVE","ESC"])
    async def leave(self,ctx:commands.Context):
        """Leaves voice channel and empties queue"""
        logger.Log("LEAVE", ctx.guild,ctx.message.author.name, time.ctime()).action()

        # VC user check
        if await vc_check_error(ctx) == False: 
            return

        self.queue[ctx.guild.id] = []

        await ctx.guild.voice_client.disconnect()
        


async def setup(bot):
    """Initialises the music cog"""
    await bot.add_cog(Music(bot))