# decorator.py
import asyncio
import enum
import functools
import logging

from custom_enums import Positions



decorator_dict = dict()


def command(desc: str = "",
            detail: str = ""):
    def inner(function):
        if not function.__name__ in decorator_dict:
            decorator_dict[function.__name__] = {
                        Positions.FUNC: function,
                        Positions.DESC: desc,
                        Positions.DETAIL: detail
                    }
        @functools.wraps(function)
        async def wrapper(*args, **kwargs):
            await function()
        return wrapper
    return inner
