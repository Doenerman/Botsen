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
