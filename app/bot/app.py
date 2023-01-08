import os
import importlib
import re
import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types
from app.models import Account
from app.bot import handler
from pathlib import Path


logging.basicConfig(level=logging.INFO, format="(%(asctime)s) [%(levelname)s]: %(message)s")


try:
    import uvloop
except ModuleNotFoundError:
    logging.warn("Uvloop not installed! (pip install uvloop)")
    uvloop = None


class TelegramBot:
    def __init__(self, **kwargs):
        if 'auth_token' not in kwargs or kwargs.get('auth_token') is None:
            raise Exception('Not enough arguments to initialize the bot')

        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

        self.__set_uvloop_policy()
        self.__read_handlers()
        self.__execute_start(kwargs['auth_token'])

    def __set_uvloop_policy(self):
        """Function to set uvloop policy"""

        if uvloop is not None:
            if not isinstance(asyncio.get_event_loop_policy(), uvloop.EventLoopPolicy):
                asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    def __execute_start(self, token):
        """Function to start the bot"""
        self.__bot = Bot(token=token)
        self.__dp = Dispatcher(self.__bot)

        Account.TempData.bot = self.__bot

        self.__dp.register_message_handler(self.message_handler)
        self.__dp.register_callback_query_handler(self.callback_query_handler)

        executor.start_polling(self.__dp, skip_updates=True)

    def __read_handlers(self):
        """Function to read commands files"""

        path = Path(__file__).resolve().parent.joinpath("commands/")

        for command in path.rglob('**/*.py'):

            spec = importlib.util.spec_from_file_location(
                command.name, command
            )

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

    def load_or_create(self, user_obj):
        """Function to create user in database"""

        return Account.objects.get_or_create(
            user_id=user_obj.id,
            defaults={
                'first_name': user_obj.first_name,
                'last_name': user_obj.last_name,
                'username': user_obj.username}
        )[0]

    async def message_handler(self, message: types.Message):
        """Message handler function"""

        processed_name = message.text.lower().strip()
        path_args = re.split(r'\s+', processed_name)
        user = self.load_or_create(message['from'])

        if 'меню' not in processed_name:
            for command in handler.commands:
                if ((not command.with_args and command.name in ['', processed_name])
                    or (command.with_args and command.name in ['', path_args[0]])) and \
                        (command.dialog == user.dialog or command.dialog == "all"):

                    if not await command.handle(message, path_args, self.__bot, user):
                        await message.reply('❌ Произошла <b>системная</b> ошибка. Выйдите в меню и попробуйте <b>ещё раз</b>.', parse_mode='HTML')
                    break
            else:
                await message.reply('⚠️ Неизвестная команда. Напишите мне <b>«Меню»</b> и воспользуйтесь кнопками', parse_mode='HTML')
        else:
            await user.return_menu()

    async def callback_query_handler(self, call: types.CallbackQuery):
        """Callback message handler function"""

        path_args = re.split(r'\s+', call.data)
        user = self.load_or_create(call.from_user)

        for callback in handler.callbacks:
            if callback.name == path_args[0]:
                if not await callback.handle(call, path_args, self.__bot, user):
                    await self.__bot.answer_callback_query(callback_query_id=call.id, text='❌ Возникла ошибка при обработке события', show_alert=True)
                break
        else:
            await self.__bot.answer_callback_query(callback_query_id=call.id, text='❌ Неизвестный запрос', show_alert=True)
