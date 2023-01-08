from app.bot.assets import Command, Callback
from app.exceptions import FunctionIsNotAsynchronous
from inspect import iscoroutinefunction

commands, callbacks = ([], [],)


def message(**kwargs):
    def with_args(handler):
        if iscoroutinefunction(handler):
            if 'names' in kwargs:
                if not isinstance(kwargs['names'], list):
                    kwargs['names'] = [kwargs['names']]

                for name in kwargs['names']:
                    commands.append(
                        Command(
                            name=name,
                            handler=handler,
                            dialog=kwargs['dialog'] if 'dialog' in kwargs else 'all',
                            with_args=(kwargs['with_args'] if 'with_args' in kwargs else False)
                        )
                    )
        else:
            raise FunctionIsNotAsynchronous(handler)
    return with_args


def callback(**kwargs):
    def with_args(handler):
        if iscoroutinefunction(handler):
            if 'name' in kwargs:
                callbacks.append(
                    Callback(name=kwargs['name'], handler=handler)
                )
        else:
            raise FunctionIsNotAsynchronous(handler)
    return with_args
