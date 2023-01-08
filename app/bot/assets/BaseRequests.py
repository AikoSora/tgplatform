import traceback
import logging
import sys


class Command:
    def __init__(self, **kwargs):
        if not kwargs.keys() & {'name', 'handler'}:
            raise Exception('Not enough arguments to create command object')
        self.name = kwargs['name'].lower()
        self.dialog = kwargs['dialog']
        self.__handler = kwargs['handler']
        self.with_args = kwargs['with_args']

    async def handle(self, message, path_args, bot, user):
        try:
            await self.__handler(message, path_args, bot, user)
            return True

        except Exception:
            ex_type, ex, tb = sys.exc_info()

            logging.error(f"\n{ex}\n")

            for text in traceback.format_tb(tb):
                print(text)

            return False


class Callback:
    def __init__(self, **kwargs):
        if not kwargs.keys() & {'name', 'handler'}:
            raise Exception('Not enough arguments to create callback object')

        self.name = kwargs['name'].lower()
        self.__handler = kwargs['handler']

    async def handle(self, callback, path_args, bot, user):
        try:
            await self.__handler(callback, path_args, bot, user)
            return True

        except Exception:
            ex_type, ex, tb = sys.exc_info()

            logging.error(f"\n{ex}\n")

            for text in traceback.format_tb(tb):
                print(text)

            return False
