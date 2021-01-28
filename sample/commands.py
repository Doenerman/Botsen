# commands.py
import logging
import discord

import decorator

from context import Context
from custom_enums import Positions

CommandDict = decorator.decorator_dict


command_dict = decorator.decorator_dict

@decorator.command(desc="Let me tell you something about stuff " \
                        + "you don't know so far",
                   detail="Informs about a handling of and usage of " \
                          + "a that is specified.")
async def help(ctx: Context):
    """ Print the detailed description of the method that is specified in
    the 'context'.
    """
    if len(ctx.args) > 0 and ctx.args[0] in command_dict:
        await ctx.message.channel.send(command_dict[ctx.args[0]][Positions.DETAIL])
    else:
        msg_string = 'The given command is not supported. A list of commands i can ' \
                     + 'understand is given below\n'
        for command in command_dict:
            msg_string += command + ', '
        await ctx.message.channel.send(msg_string)
                    

@decorator.command(desc="Giving me the long awaited break.",
                   detail="Shotting me down, which makes me unreachable.")
async def shutdown(ctx: Context):
    """ Shuts down the given Discord Client.

        Parameters:
        -----------
            client: discord.Client
                The client to shut down.
    """
    logging.info('Client shutting down')
    await ctx.message.channel.send('Cya :wave:')
    await ctx.client.close()
