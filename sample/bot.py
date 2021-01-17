# bot.py
import os

import discord
import enum

from discord import Client
from dotenv import load_dotenv

from commands import command_dict

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
joinableGuild = os.getenv('DISCORD_GUILD')
textChannel = os.getenv('DISCORD_TEXT_CHANNEL')

command_prefix = os.getenv('COMMAND_PREFIX')


class Positions(enum.Enum):
    """ An enum.Enum to determine the keys for dictionaries that contain
    information about commands to be executed and their attributes.

    Attributes:
        MSG:        The key in a dictionary, whose value is the discord.Message
                    that was received and which contains a command.
        FUNC_NAME:  The name of the function/command to be executed.
        ARG_COUNT:  The additional number of arguments that are mentioned.
        ARG_LIST:   The list of additional arguments.
    """
    MSG = 0
    FUNC_NAME = 1
    ARG_COUNT = 2
    ARG_LIST = 3


class DiscordBot( Client ):
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
        self.coms = Commands(self)

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


                return_value = command_dict

        return return_value


    async def on_ready(self):
        for guild in client.guilds:
            if guild.name == joinableGuild:
                break

        print(
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
            further elements:   Additional arguments for the command.

        If the third entry of the list is a command that is a key in the
        dictionary 'command_dict' the referenced method is called. If that is
        not the case the method 'print_commands(message)' is called.
        """
        command = self.message_cutter( message )

        print( "{}/{}: {}".format( message.channel, message.author, message.content) )

        if command != False:
            if ( command[1] == 3 ) and ( command[2] in command_dict ):
                await command_dict.get( command[2] )[0](self, command[0] )
            elif ( command[1] > 3 ) and ( command[2] in command_dict ):
                await command_dict.get( command[2] )[0](self, command[0], command[3:])
            else:
                await Commands.print_commands(self, message.channel)


client = DiscordBot()
client.run(token)
