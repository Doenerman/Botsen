#decorator.py
import asyncio
import enum
import functools
import logging

class CommandDict(enum.Enum):
    FUNC = 1
    DESC = 2
    DETAIL = 3

decorator_dict = dict()


def command(desc: str = "",
            detail: str = ""):
    def inner(function):
        if not function.__name__ in decorator_dict:
            decorator_dict[function.__name__] = {
                        CommandDict.FUNC: function,
                        CommandDict.DESC: desc,
                        CommandDict.DETAIL: detail
                    }
        @functools.wraps(function)
        async def wrapper(*args, **kwargs):
            await function()
        return wrapper
    return inner
