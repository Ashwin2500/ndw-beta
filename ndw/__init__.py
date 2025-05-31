from .functions import *
from .gateway import *

class bot:
    def __init__(self,TOKEN) -> None:
        self.TOKEN = TOKEN
        self.prefix = '!'
        self.loggging = 20
        self._handlers = {}

    def run(self):
        connect(self.TOKEN, self.loggging, self._handlers)
    
    def event(self, func):
        self._handlers[func.__name__] = func
        return func