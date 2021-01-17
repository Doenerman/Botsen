# commands.py
import discord
import enum

class Commands:
    def __init__(self, client: discord.Client):
        self.client = client

    async def print_commands(self,
                             message: discord.Message):
        """The method sends a message with all supported commands the bot can receive over
        the text chat and react properly.

        The method iterates over the dictionary 'command_dict' and adds each
        the key of entry to the text that will be send to 'channel'.

        Parameters:
        -----------
            client: discordClient
                The discord client that shall print the command message into
                'channel'.
            channel: discord.Message.channel
                The text channel, where the information string shall be send to.
        """
        
        msg_content = 'I don\'t know that command, but i can\'t help you either'
        #msg_content += "The following commands are supported:\n"
        #for key in self.command_dict:
        #    msg_content += "!%s "%(key)
        #msg_content += "\n\nFor descriptions for a command type:\n"
        #msg_content += "\t!help <command>"

        await message.channel.send( msg_content )

    async def print_help(self,
                         channel: discord.Message.channel,
                         command: str):
        """The method sends a help message for the given command on the text
        channel of 'message'.The method sends a help message for the given
        command on the text channel of 'message'.

        The method checks if the given string 'command' is a key of the
        dictionary 'command_dict'. If so, the description of that command is
        send to the textchannel over which the Message 'message' was received
        over. In case the command is not supported, a list of supported commands
        is send to the text channel.

        Parameters:
        -----------
            client: discord.Client
                The discord client that shall print the information message about
                the commands.
            channel: discord.Message.channel
                The text channel, where the information string shall be send to.
            command:
                The string of the command whose more detailed description is
                requested.
        """
        if command in command_dict:
            await channel.send( command_dict[command][1] )
        else:
            await channel.send( "The command {command} is not supported" )
            await self.print_commands( message )

    async def shutdown(self,
                       message: discord.Message):
        """ Shuts down the given Discord Client.

            Parameters:
            -----------
                client: discord.Client
                    The client to shut down.
        """
        await self.client.close()
        print('Client shutting down')
