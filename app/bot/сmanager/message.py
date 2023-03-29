from .dispatcher import MessageCommandHandler
from typing import Union

message_commands = []


def message(
        names: Union[str, list],
        dialog: str = None,
        with_args: bool = True,
        *args,
        **kwargs
):
    def with_args(function):
        names_list = names

        if not isinstance(names, list):
            names_list = [names]

        for name in names_list:
            message_commands.append(
                MessageCommandHandler(
                    function=function,
                    name=name,
                    dialog=dialog,
                    with_args=with_args
                )
            )
    return with_args
