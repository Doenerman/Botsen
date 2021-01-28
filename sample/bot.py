# bot.py
import argparse
import logging
import os

import discord
import enum

from discord import Client
from dotenv import load_dotenv

from commands import command_dict
from commands import Positions
from context import Context
from custom_enums import Positions

parser = argparse.ArgumentParser()
parser.add_argument(
    "-log", 
    "--log", 
    default="warning",
    help=(
        "Provide logging level. "
        "Example --log debug', default='warning'"),
    )

options = parser.parse_args()
levels = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warn': logging.WARNING,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}
level = levels.get(options.log.lower())
if level is None:
    raise ValueError(
        f"log level given: {options.log}"
        f" -- must be one of: {' | '.join(levels.keys())}")
logging.basicConfig(level=level)
logger = logging.getLogger(__name__)

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
joinableGuild = os.getenv('DISCORD_GUILD')
textChannel = os.getenv('DISCORD_TEXT_CHANNEL')
command_prefix = os.getenv('COMMAND_PREFIX')


class DiscordBot(discord.Client):
    """A class of a Discrod Bot that can play audio to the voice channel.

    The class provides the functionality to read a text channel and react to the
    content written.

    Methods:
    --------
    message_cutter(messge)
        Extracts the command of a message in case it contains one, otherwise
        returning False.
    """

    def __init__(self):
        super().__init__()

    def message_cutter(self, message: discord.Message):
        """The method add the words of the given Message 'message' to the ouput
        dictionary in case the message starts with the 'command_prefix'.

        The method first checks if the message if from a channel where commands can
        be send over. If that is the case and the message begins with the
        'command_prefix' and all words of the message are added to a list which
        is the last entry of the dictionary. The dictionary is expected to have
        the following keys:
            Position.MSG:           The 'discord.Message' that contains the command.
            Position.FUNC_NAME:     The name of the function/command that shall be
                                    executed.
            Position.ARG_COUNT      The number of arguments the function/command to be
                                    exectued shall use.
            optional:
                Position.ARG_LIST   A list of additional arguments for the
                                    function/command

        Parameters:
        -----------
        message : discord.Message 
            The discord.Message that should be inspected and checked if there it
            contains a command that has do be executed.

        Returns:
        --------
            dict:
                A dict is returned in case the discord.Message 'message' begins with the
                character 'command_prefix'. The dictionary is expected to
                contain the following keys:
                    Position.MSG:       The 'discord.Message' that contains the command.
                    Position.FUNC_NAME: The name of the function/command that shall be
                                        executed.
                    Position.ARG_COUNT  The number of arguments the function/command to be
                                        exectued shall use.
                and optional key is
                    Position.ARG_LIST   A list of additional arguments for the
                                        function/command
                
            False
                In case the parameter 'message' did not contain a command.
        """
        return_value = False
        if message.channel.name == textChannel:
            is_command = message.content.startswith( command_prefix )
            if is_command:
                command_end_pos = message.content.find(' ')
                command_dict = dict()
                command_dict[Positions.MSG] = message
                command_dict[Positions.ARG_COUNT] =  message.content.count( ' ' )
                if command_end_pos == -1:
                    command_dict[Positions.FUNC_NAME] = message.content[1:len(message.content)]
                else:
                    curr_command_start_pos = 1
                    command_args = list()
                    while command_end_pos != -1:
                        command_args.append(
                                message.content[curr_command_start_pos:command_end_pos]
                        )
                        curr_command_start_pos = command_end_pos
                        command_end_pos = message.content.find(' ')
                    command_dict[ARG_LIST] = command_args
                
                logging.debug('Command cut into:')
                logging.debug('Positions.MSG: %s', command_dict[Positions.MSG])
                logging.debug('Positions.ARG_COUNT: %s',
                              command_dict[Positions.ARG_COUNT])
                logging.debug('Positions.FUNC_NAME: %s',
                              command_dict[Positions.FUNC_NAME])


                return_value = command_dict

        return return_value


    async def on_ready(self):
        for guild in client.guilds:
            if guild.name == joinableGuild:
                break

        logging.info(
            f'{client.user} has connected to the guild!\n'
            f'{guild.name}(id: {guild.id})'
        )

    async def on_message(self,message):
        """The event that is triggered, in case the bot recognizes an incoming
        Message on the observed text channel. If a command is detected, it is
        method is called with the arguments given in the Message 'message'.

        The method calls 'message_cutter(self,message)' in order to check if the
        given Message contains a command or can be ignored. If it contains a
        command, the method expects a list with at least three elements with the
        following elements:

            1st:    The Message 'message' that requests the command.
            2nd:    The number of additional arguments for the command.
            3rd:    A 'str' of the command itself.
            4th:    List of additional arguments for the command.

        If the third entry of the list is a command that is a key in the
        dictionary 'self.coms.command_dict' the referenced method is called. If that is
        not the case the method 'print_commands(message)' is called.
        """
        command = self.message_cutter(message)

        logging.info("-{}--{}/{}: {}".format(message.guild,
                                             message.channel, 
                                             message.author,
                                             message.content) )

        context = Context(self, message)

        if command != False and len(command) > 2:
            # check if the command exists
            if command[Positions.FUNC_NAME] in command_dict:
                # execute the command
                await command_dict[command[Positions.FUNC_NAME]][Positions.FUNC](context)
            else:
                msg_string = 'The following commands are supported:```'
                for command in iter(sorted(command_dict)):
                    msg_string += '\n\t' + command + '\t' \
                                  + command_dict[command][Positions.DESC]
                msg_string += '```'
                await message.channel.send(msg_string)

client = DiscordBot()
client.run(token)
