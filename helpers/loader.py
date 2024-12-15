import random
import discord
import time
import asyncio

from discord.ext import commands
import helpers.logger as logger

# Color codes for embeds
EMBED_COLORS = {
    "magenta":[204,51,139],
    "blue":[99,203,251],
    "red":[255,0,50],
    "pickle":[27,11,32],
    "yellow":[255,255,0],
    "greenyellow":[173,255,47]
}


# MD file character replacement
FORBIDDEN_CHARS = ["*","`","#","_",">"]
def md_conv(str):
    nstr = ""
    for c in str:
        if c in FORBIDDEN_CHARS:
            nstr += "@"
        else:
            nstr += c
    return nstr