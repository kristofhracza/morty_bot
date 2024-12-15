import os
import asyncio
import discord
import yt_dlp
import platform
from dotenv import load_dotenv

# Load env variables
load_dotenv()
if platform.system() == "Linux":
    FFMPEG = "/usr/bin/ffmpeg"
else:
    FFMPEG = os.getenv("FFMPEG_PATH")

ytdlp_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

# https://stackoverflow.com/questions/66070749/how-to-fix-discord-music-bot-that-stops-playing-before-the-song-is-actually-over
ffmpeg_options = {
    "options": "-vn",
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

yt_dlp_player = yt_dlp.YoutubeDL(ytdlp_options)


# Source handling class
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.3):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    """ Loads single song """
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()

        # Keyword / URL search
        if "https://www.youtube.com/watch" not in url:
            data = await loop.run_in_executor(None, lambda: yt_dlp_player.extract_info(f"ytsearch:{url}", download=not stream))
        else:
            data = await loop.run_in_executor(None, lambda: yt_dlp_player.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else yt_dlp_player.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options, executable=FFMPEG,), data=data)

    """ Loads playlist """
    @classmethod
    async def from_list(cls,url,queue,id,loop=None,stream=False):
        # Get list
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: yt_dlp_player.extract_info(url, download=not stream))
        old_data = data

        # Tracks into server queue
        for track in data["entries"]:
            if track != None:
                filename = track["webpage_url"] if stream else yt_dlp_player.prepare_filename(track)
                player = cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options, executable=FFMPEG,), data=track)
                queue[id].append([player, track["webpage_url"]])

        return old_data