"""

File to include all the most needed libs + any other variable used across the app

Colour rules for embeds:
    - Info:     Blue
    - Warning:  Yellow
    - Error:    Red
"""
import random,discord,time,asyncio
from discord.ext import commands

import helpers.logger as logger
from helpers.embed import make_embed

# Embed colours
EMBED_COLORS = {
    "magenta":[204,51,139],
    "blue":[99,203,251],
    "red":[255,0,50],
    "pickle":[27,11,32],
    "yellow":[255,255,0],
    "greenyellow":[173,255,47]
}