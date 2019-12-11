# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
joinableGuild = os.getenv('DISCORD_GUILD')
textChannel = os.getenv('DISCORD_TEXT_CHANNEL')

command_prefix = os.getenv('COMMAND_PREFIX')

client = discord.Client()


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
        self.command_dict = { 
                "shutdown" : self.shutdown,
                "help" : self.print_help,
        }
        """The dictionary maps each supported command to a method to execute when
        the bot receives the command.

        Elements:
        ---------
            shutdown    ->  self.close()
                The bot is requested to shutdown and the command to do is is
                'self.close()'
        """

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
                A list of str. The str of the list are the words of 'message'
                seperated by a whitespace.
            False
                In case the parameter 'message' did not contain a command.
        """
        return_value = False
        if message.channel.name == textChannel:
            is_command = message.content.startswith( command_prefix )
            if is_command:
                command_end_pos = message.content.find(' ')
                if command_end_pos == -1:
                    return_value = message.content[1:len(message.content)]
                else:
                    command_list = []
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
        command = self.message_cutter( message )

        if command != False:
            self.command_dict.get( command[0] )


client = DiscordBot()
client.run(token)
