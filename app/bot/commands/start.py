from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from app.bot.сmanager import message, callback
from app.models import Account
from asyncio import sleep
from time import time


async def start(object, user, callback, language):
    if not callback:
        await user.reply(f"Привет! {time()}", keyboard=IKM(inline_keyboard=[
            [IKB('EN', callback_data="playboy en")],
        ]))
    else:
        if language == "ru":
            text = "Привет!"
        elif language == "en":
            text = "Hello!"
        await object.message.edit_text(f"{text} {time()}", reply_markup=IKM(inline_keyboard=[
            [IKB(f'{"RU" if language == "en" else "EN"}', callback_data=f'playboy {"ru" if language == "en" else "en"}')],
        ]))


@message(names='/start', dialog=Account.Dialog.START)
async def _(message, path_args, user, bot):
    await start(message, user, False, "")


@message(names='/info', dialog=Account.Dialog.START)
async def test(message, path_args, user, bot):
    await sleep(10)
    await user.reply(f"info! {time()}")


@callback(name="playboy")
async def _(event, path_args, user, bot):
    await start(event, user, True, path_args[-1])
