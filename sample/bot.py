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



load_dotenv()
token = os.getenv('DISCORD_TOKEN')
joinableGuild = os.getenv('DISCORD_GUILD')
textChannel = os.getenv('DISCORD_TEXT_CHANNEL')


bot = Bot(os.getenv('COMMAND_PREFIX'))

playlist = list()

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


@bot.command(brief="Nicely ask the bot to join for a choral",
             description="Invite the bot to join voices for a sweet "
                         "serenade with the notes given by the "
                         "youtube link.",
             pass_context=True)
async def sing(self, ctx, *, url):
    print(url)
    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=self.bot.loop)
        ctx.voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    await ctx.send('Now playing: {}'.format(player.title))

# start the actual bot
bot.run( token )
