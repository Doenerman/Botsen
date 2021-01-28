# custom_enums.py
import enum

class Positions(enum.Enum):
    """ An enum.Enum to determine the keys for dictionaries that contain
    information about commands to be executed and the functions they call.

    Attributes:
        ARG_COUNT:  The additional number of arguments that are mentioned.
        ARG_LIST:   The list of additional arguments.
        DESC:       The position of a description of a function/command.
        DETAIL:     The position of the a more detailed description of the
                    function.
        FUNC:       The position of the function/command to be executed.
        FUNC_NAME:  The name of the function/command to be executed.
        MSG:        The key in a dictionary, whose value is the discord.Message
                    that was received and which contains a command.
    """
    MSG = 0
    FUNC_NAME = 1
    ARG_COUNT = 2
    ARG_LIST = 3
    FUNC = 4
    DESC = 5
    DETAIL = 6
