"""
Script to take audio from yt url
Big thanks to Rapptz
https://github.com/Rapptz/discord.py/blob/45d498c1b76deaf3b394d17ccf56112fa691d160/examples/basic_voice.py

"""
import os
import asyncio
import discord
import youtube_dl
from dotenv import load_dotenv
# Load env variables
load_dotenv()
FFMPEG = os.getenv('FFMPEG_PATH')

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

# Fix for music stopage: https://stackoverflow.com/questions/66070749/how-to-fix-discord-music-bot-that-stops-playing-before-the-song-is-actually-over
ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.thumbnail = data.get("thumbnail")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()

        # URL check to decide to search for url or keywords
        if "https://www.youtube.com/watch" not in url:
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{url}", download=not stream))
        else:
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options, executable=FFMPEG,), data=data)

    @classmethod
    async def from_list(cls,url,queue,id,loop=None,stream=False):
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        loop = loop or asyncio.get_event_loop()
        old_data = data
        data = data["entries"]

        # Load tracks into server queue
        for track in data:
            filename = track["webpage_url"] if stream else ytdl.prepare_filename(track)
            player = cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options, executable=FFMPEG,), data=track)
            queue[id].append([player, track["webpage_url"]])

        return old_data