import os

import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types
from app.models import Account
from .сmanager import load_all_commands, message_commands, callback_commands
from .handlers import *


class TelegramBot:
    def __init__(self, token, **kwargs):

        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

        self.set_logger(logging.INFO)
        self.__set_uvloop_policy()

        load_all_commands()
        self.__execute_start(token)

    def set_logger(self, level):
        logging.basicConfig(level=level, format="(%(asctime)s) [%(levelname)s]: %(message)s")

    def __set_uvloop_policy(self):
        """Function to set uvloop policy"""
        try:
            import uvloop

            if not isinstance(asyncio.get_event_loop_policy(), uvloop.EventLoopPolicy):
                asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        except ModuleNotFoundError:
            logging.warn("Uvloop not installed! (pip install uvloop)")

    def __execute_start(self, token):
        """Function to start the bot"""
        self.__bot = Bot(token=token)
        self.__dp = Dispatcher(self.__bot)

        Account.TempData.bot = self.__bot

        self.__dp.register_message_handler(MessageHandler(message_commands, self.__bot))
        self.__dp.register_callback_query_handler(CallBackHandler(callback_commands, self.__bot))

        executor.start_polling(self.__dp, skip_updates=True)
