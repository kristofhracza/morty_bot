"""

A cog for all the fun functions

"""
# Libs
from helpers.loader import *
# Additional libs
import nsfw,memes

class Fun(commands.Cog):
  def __init__(self,bot):
    self.bot = bot


  # Pepe meter
  @commands.command(name="pee-pee")
  async def pepe(self,ctx):
      size = random.randrange(1,25)
      await ctx.send(embed=make_embed(f"{ctx.message.author.name}'s size",f"8{'='*size}D",discord.Color.from_rgb(*EMBED_COLORS["greenyellow"])))
      logger.Log("PEE-PEE",ctx.guild,ctx.message.author.name,time.ctime()).action()

  # NSFW
  @commands.command(name="nsfw")
  async def nsfw(self,ctx):
      link = nsfw.get_gif()
      embed = discord.Embed(
      color=discord.Color.from_rgb(*EMBED_COLORS["magenta"]))
      embed.set_image(url=link)
      await ctx.send(embed=embed) 
      logger.Log("NSFW",ctx.guild,ctx.message.author.name,time.ctime()).action()

 # MEMES
  @commands.command(name="meme")
  async def meme(self,ctx):
      link = memes.get_meme()
      embed = discord.Embed(
      color=discord.Color.from_rgb(*EMBED_COLORS["greenyellow"]))
      embed.set_image(url=link)
      await ctx.send(embed=embed) 
      logger.Log("MEME",ctx.guild,ctx.message.author.name,time.ctime()).action()

async def setup(bot):
    await bot.add_cog(Fun(bot))