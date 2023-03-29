from .dispatcher import CallBackCommandHandler

callback_commands = []


def callback(name: str, *args, **kwargs):
    def with_args(function):
        callback_commands.append(
            CallBackCommandHandler(
                function=function,
                name=name
            )
        )
    return with_args
