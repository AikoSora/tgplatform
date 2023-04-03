from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from app.bot.сmanager import message, callback
from app.models import Account
from asyncio import sleep
from time import time


async def start(object, user, callback, language):
    if callback:
        text = "Привет!" if language == "ru" else "Hello!"
        language = "ru" if language == "en" else "en"

        await object.message.edit_text(f"{text} {time()}", reply_markup=IKM(inline_keyboard=[
            [IKB(f'{language.upper()}', callback_data=f'playboy {language}')],
        ]))
    else:
        await user.reply(f"Привет! {time()}", keyboard=IKM(inline_keyboard=[
            [IKB('EN', callback_data="playboy en")],
        ]))


@message(names='/start', dialog=Account.Dialog.START)
async def _(message, path_args, user, bot):
    await start(message, user, False, "")


@message(names='/info', dialog=Account.Dialog.START)
async def test(message, path_args, user, bot):
    await sleep(10)
    await user.reply(f"info! {time()}")


@message(names='', dialog=Account.Dialog.START)
async def _(message, path_args, user, bot):
    await sleep(10)
    await user.reply(f"Nothing! {time()}")


@callback(name="playboy")
async def _(event, path_args, user, bot):
    await start(event, user, True, path_args[-1])
