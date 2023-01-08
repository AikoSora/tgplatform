from datetime import datetime
from aiogram.types import ReplyKeyboardMarkup as RKM, KeyboardButton as KB
from django.db import models


class Account(models.Model):
    class TempData:
        bot = None

    class Dialog:
        START = 'start'
        DEFAULT = 'default'

    # Base variables
    user_id = models.BigIntegerField(null=False)
    first_name = models.TextField()
    last_name = models.TextField(default='', null=True, blank=True)
    username = models.TextField(default=None, null=True, blank=True)
    reg_date = models.DateTimeField(default=datetime.now())
    dialog = models.TextField(default=Dialog.START)
    temp = models.TextField(default='', blank=True)

    async def reply(self, text, **kwargs):
        processed_text = '\n'.join(text) if isinstance(text, list) else text

        return await self.TempData.bot.send_message(
            self.user_id,
            processed_text % kwargs['concate'] if 'concate' in kwargs else processed_text,
            parse_mode='HTML',
            reply_markup=(kwargs['keyboard'] if 'keyboard' in kwargs else None)
        )

    async def return_menu(self, text='🚀 Вы зашли в <b>главное меню</b> бота', **kwargs):
        self.dialog = self.Dialog.DEFAULT
        self.save()
        return await self.reply(text, **kwargs)
