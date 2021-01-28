# context.py

import discord

class Context:
    """ This class provides useful information for a commands
    that are called from chat.

    Objects of this class can be passed to functions that implement
    commands that can be invoked by the discord chat.

    Attributes:
    ===========

        args: list
            A list of arguments that shall be passed to the commands
            that were invoked by a chat command.

        client: discord.Client
            The client the commands shall be able to edit.

        message: discord.Message
            The message in which the command is called.
    """
    def __init__(self, 
                 client: discord.Client,
                 msg: discord.Message,
                 args: list = None):
        """ Initialize a object of this class.

        Parameter:
        ==========

            args: list
                A list of arguments that shall be passed to the command/function
                to be executed.

            client: discord.Client
                The client a command shall be edit and modify.

            msg: discord.Message
                The message that invokes a command/function to be executed.
        """
        self.client = client
        self.message = msg
        if args == None:
            self.args = list()
