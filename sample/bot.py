# bot.py

import asyncio

import discord
from discord import ext
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient

import dotenv
from dotenv import load_dotenv


import os

import youtube_dl


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
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
joinableGuild = os.getenv('DISCORD_GUILD')
textChannel = os.getenv('DISCORD_TEXT_CHANNEL')


bot = Bot(os.getenv('COMMAND_PREFIX'))

@bot.command(brief="Shutsdown the bot",
             description="Stopping all current activities of the bot and shuts it down.")
async def shutdown(ctx):
    """ Logs out the bot from discord

        By logging the bot out, the application is also shutdown.
    """
    await ctx.bot.logout()


@bot.command(brief="Ask the bot to join the talk",
             description="Kindly ask the bot if it has some free time "
                         "and interested in a little bit of chatting",
             pass_context=True)
async def summon(ctx):
    """ Let the bot join the voice channel the context 'ctx'
        
        If the author of the context 'ctx' is part of a voice channel,
        the bot also tries to enter the same channel.
    """
    if ctx.message.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()

@bot.command(brief="Nicely ask the bot to join for a choral of a private song",
             description="Invite the bot to join voices for a sweet "
                         "serenade that i composed at home to worship "
                         "Lekeke",
             pass_context=True)
async def singmysong( ctx, *, song):
    print( "no song" )

@bot.command(brief="Nicely ask the bot to join for a choral",
             description="Invite the bot to join voices for a sweet "
                         "serenade with the notes given by the "
                         "youtube link.",
             pass_context=True)
async def sing(ctx, *, url):
    print(url)
    
    
    for channel in bot.voice_clients:
        async with ctx.typing():
            player = await YTDLSource.from_url( url, loop=bot.loop )
            channel.play(player, after=lambda e: pring( 'Player error: %s' ) if e else None )
        await ctx.send( 'Now playing: {}'.format(player.title))

@bot.command(brief="Gives the bot a small break",
             description="Let the bot rest until there is someone that think he "
                         "is fit enough to continue and get back to work.")
async def rest(ctx):
    """ Requests the bot to pause playing audio.

        If the bot is currently playing some audio using the :class:VoiceClient
        the playback is paused otherwise, a message is send to the channel of the
        context.
    """
    for channel in bot.voice_clients:
        if channel.is_playing():
            channel.pause()
        else:
            await ctx.send( 'I don\'t need to rest, give me some action' )


@bot.command(brief="Commands the bot to continue playing",
             description="Orders to bot to go back to work and entertain the folks")
async def workwork(ctx):
    """ Requests the bot to resumes playing audio.

        If the bot is currently pause playing some audio using the :class:VoiceClient
        the playback is resumed otherwise, a message is send to the channel of the
        context.
    """
    for channel in bot.voice_clients:
        if channel.is_paused():
            channel.resume()
        else:
            await ctx.send( 'Give me a rest, i am already at work!!' )

# start the actual bot
bot.run( token )
