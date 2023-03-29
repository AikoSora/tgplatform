import importlib
import logging
import sys
import traceback
from django.conf import settings


def load_all_commands():
    """Function to read commands files"""

    path = settings.BASE_DIR.joinpath("app/bot/commands/")

    for command in path.rglob('**/*.py'):
        try:
            spec = importlib.util.spec_from_file_location(
                command.name, command
            )

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            logging.info(f"{command.name} is load.")
        except Exception:

            _, ex, tb = sys.exc_info()
            error_text = "\n"

            for text in traceback.format_tb(tb):
                error_text += text

            logging.error(error_text + f"{ex}")
            logging.info(f"{command.name} is not load!")
