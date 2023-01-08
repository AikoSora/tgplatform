# Exceptions script

class FunctionIsNotAsynchronous(Exception):
    def __init__(self, function):
        #function.__globals__['__file__']
        self.message = f"{function.__name__} is not an asynchronous function!"

        super().__init__(self.message)
