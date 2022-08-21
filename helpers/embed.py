"""

Easier embed making

"""
import discord


def make_embed(title,desc,color,*args,**kwargs):
    embed = discord.Embed(
    title=title, 
    description=desc,
    color=color
    )
    return embed