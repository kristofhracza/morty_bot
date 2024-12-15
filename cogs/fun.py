import random

from helpers.loader import *

class Fun(commands.Cog):
    """Small fun functions"""

    def __init__(self,bot):
        self.bot = bot


    @commands.command(name="pp", aliases=["peepee","PP","PEEPEE"])
    async def pepe(self,ctx):
        """Shows size"""
        size = random.randrange(1,25)
        await ctx.send(embed=discord.Embed(
            title=f"{ctx.message.author.name}'s size",
            description=f"8{'='*size}D",
            color=discord.Color.from_rgb(*EMBED_COLORS["greenyellow"])
            )
        )
        logger.Log("PP", ctx.guild,ctx.message.author.name, time.ctime()).action()

    
    @commands.command(name="iq", aliases=["IQ"])
    async def iq_test(self, ctx):
        """Generates random IQ score"""
        iq = random.randint(50, 200)
        await ctx.send(embed=discord.Embed(
            title=f"{ctx.message.author.name}'s IQ",
            description=f"Your IQ is: **{iq}**",
            color=discord.Color.from_rgb(*EMBED_COLORS["greenyellow"])
        ))
        logger.Log("IQ", ctx.guild,ctx.message.author.name, time.ctime()).action()



async def setup(bot):
    """Initialises the fun cog"""
    await bot.add_cog(Fun(bot))