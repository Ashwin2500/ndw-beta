from .functions import *
from .gateway import *

class bot:
    def __init__(self,TOKEN) -> None:
        self.TOKEN = TOKEN
        self.prefix = '!'
        self.loggging = 20
        self._handlers = {}

    def run(self,level):
        connect(self.TOKEN, level, self._handlers, bot)
    
    def event(self, func):
        self._handlers[func.__name__] = func
        return func
    
    def update_user(self, data):
        for key,value in data.items():
            setattr(self,key,value)