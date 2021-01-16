# bot.py
import os

from discord import Client
from dotenv import load_dotenv

from commands import command_dict

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
joinableGuild = os.getenv('DISCORD_GUILD')
textChannel = os.getenv('DISCORD_TEXT_CHANNEL')

command_prefix = os.getenv('COMMAND_PREFIX')

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

    def message_cutter(self,message):
        """The method add the words of the given Message 'message' to the ouput
        list in case the message starts with an '!'.

        The method first checks if the message if from a channel where commands can
        be send over. If that is the case and the message begins with '!' and
        all words of the message are added to a list in the order they appear in
        'message'.

        Parameters:
        -----------
        message : Message 
            The Message that should be inspected and checked if there it
            contains a command that has do be executed.

        Returns:
        --------
            list
                A list is returned in case the Message 'message' begins with the
                character '!'. If so list contains at least three elements, which
                layout is as followed.
                1st element:        The Message 'message' that requests the
                                    command.
                2nd element:        The number of additional arguments the
                                    command got.
                3rd element:        The 'str' of the command itself.
                further elements:   The additional arguments for the command in
                                    the same order, they apear in the Message
                                    'message'.
            False
                In case the parameter 'message' did not contain a command.
        """
        return_value = False
        if message.channel.name == textChannel:
            is_command = message.content.startswith( command_prefix )
            if is_command:
                command_end_pos = message.content.find(' ')
                command_list = list()
                command_list.append( message )
                # compute length of the list
                # +1 for information about the length
                # +1 for the message itself
                # +1 in case only on command is contains but no whitespace
                command_list.append( message.content.count( ' ' ) +3)
                if command_end_pos == -1:
                    command_list.append( message.content[1:len(message.content)] )
                else:
                    curr_command_start_pos = 1
                    while command_end_pos != -1:
                        command_list.append(
                                message.content[curr_command_start_pos:command_end_pos]
                        )
                        curr_command_start_pos = command_end_pos
                        command_end_pos = message.content.find(' ')


                return_value = command_list

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
            3rd:    A 'str' of the command.
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
