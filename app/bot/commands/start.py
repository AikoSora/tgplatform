from app.bot import handler
from app.models import Account


@handler.message(names='/start', dialog=Account.Dialog.START)
async def start(message, path_args, bot, user):
    await user.reply("Привет!")


@handler.message(names='/start', dialog=Account.Dialog.START)
async def test(message, path_args, bot, user):
    await user.reply("Привет!")
