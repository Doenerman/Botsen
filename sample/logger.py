# logger.py

import os


class Logger:
    """This class provides basic logger functionalities.

    The class can be used to log various types of behaviour on console.
    """

    def __init__(self):
        self.color_normal = '\033[92m'
        self.color_warning = '\033[93m'
        self.color_exception = '\033[91m'
        self.curr_msg_color = 0
        self.color_msg_0 = '\033[90m'
        self.color_msg_1 = '\033[94m'
        self.endc = '\033[0m'

    def log_warning( self, log_string ):
        """The method prints the 'log_string' into console using the color
        'Logger.color_warning'.
        """
        print(
                f"{self.color_warning}Warning: {log_string}{self.endc}"
        )

    def log_normal_behaviour( self, log_string ):
        """The method prints the 'log_string' into console using the color
        'Logger.color_normal'.
        """
        print(
                f"{self.color_normal}Log: {log_string}{self.endc}"
        )

    def log_exception( self, log_string ):
        """The method prints the 'log_string' into console using the color
        'Logger.color_exception'.
        """
        print(
                f"{self.color_exception}Exception: {log_string}{self.endc}"
        )

    def log_message( self, message ):
        """ The method prints the 'channel' over which the message is received,
        the author that wrote the message and the content of the message into
        the console.
        """
        if self.curr_msg_color == 0:
            print( f"{message.channel}/{message.author}: {self.color_msg_0}{message.content}{self.endc}" )
            self.curr_msg_color = 1
        elif self.curr_msg_color == 1:
            print( f"{message.channel}/{message.author}: {self.color_msg_1}{message.content}{self.endc}" )
            self.curr_msg_color = 0
