from .functions import *
from .gateway import *

class bot:
    def __init__(self,TOKEN) -> None:
        self.TOKEN = TOKEN
        self.prefix = '!'
        self.loggging = 1
    def run(self):
        connect(self.TOKEN, self.loggging)