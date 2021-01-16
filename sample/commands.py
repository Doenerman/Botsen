# commands.py
import discord

async def print_commands(client: discord.Client, channel: discord.Message.channel):
    """The method sends a message with all supported commands the bot can receive over
    the text chat and react properly.

    The method iterates over the dictionary 'command_dict' and adds each
    the key of entry to the text that will be send to 'channel'.
    """
    msg_content = str()
    msg_content += "The following commands are supported:\n"
    for key in Commands.command_dict:
        msg_content += "!%s "%(key)
    msg_content += "\n\nFor descriptions for a command type:\n"
    msg_content += "\t!help <command>"

    await channel.send( msg_content )

async def print_help(client: discord.Client,
                     message: discord.Message,
                     command: str):
    """The method sends a help message for the given command on the text
    channel of 'message'.The method sends a help message for the given
    command on the text channel of 'message'.

    The method checks if the given string 'command' is a key of the
    dictionary 'command_dict'. If so, the description of that command is
    send to the textchannel over which the Message 'message' was received
    over. In case the command is not supported, a list of supported commands
    is send to the text channel.
    """
    if command in Commands.command_dict:
        await message.channel.send( Commands.command_dict[command][1] )
    else:
        await message.channel.send( "The command {command} is not supported" )
        await Command.print_commands( message )

async def shutdown(client: discord.Client, _):
    """ Shuts down the given Discord Client.
    """
    await client.close()
    print('Client shutting down')


command_dict = {
    "shutdown" : 
    [ shutdown, "Shuts down the bot" ],
    "commands" : 
    [ print_commands, "Prints this message" ],
}
