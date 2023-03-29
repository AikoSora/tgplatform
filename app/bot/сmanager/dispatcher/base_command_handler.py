import logging
import sys
import traceback
from asyncio import create_task


class BaseCommandHandler:
    """
    ---------------
    Command handler
    ---------------

    @function -> Function
    @name -> str
    @dialog -> str (Default: None)
    @with_args -> bool (Default: True)
    """

    def __init__(
            self,
            function,
            name: str,
            dialog: str = None,
            with_args=True,
            *args,
            **kwargs
    ):
        self.command_name = name
        self.command_dialog = dialog
        self.command_with_args = with_args
        self.command_function = function

    def register_data(self, name, path_args, user, bot):
        """
        Function for register event data
        """

        self.name = name
        self.path_args = path_args
        self.user = user
        self.bot = bot

    def allowed_name(self) -> bool:
        """
        Function for check command name to name

        @return -> bool
        """
        if self.command_with_args:
            return self.command_name in ['', self.path_args[0]]
        return self.command_name in ['', self.name]

    def allowed_dialog(self) -> bool:
        """
        Function for check command dialog to user dialog

        @return -> bool
        """
        if self.command_dialog is None:
            return True
        return self.command_dialog == self.user.dialog

    async def execute(self, event_object):
        try:
            create_task(
                self.command_function(
                    event_object,
                    self.path_args,
                    self.user,
                    self.bot
                )
            )
            return True
        except Exception:
            _, ex, tb = sys.exc_info()

            for text in traceback.format_tb(tb):
                logging.error(text)

            logging.error(f"\n{ex}\n")

            return False
