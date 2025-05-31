from . import *

event_handlers = {}
user_event_handlers = {}


def register(event_name):
    def decorator(func):
        event_handlers[event_name] = func
        return func
    return decorator

def set_user_handelers(handelers):
    global user_event_handlers
    user_event_handlers = handelers

async def handle(event):
    event_name = event.get('t')
    if not event_name:
        return
    
    if event_name in event_handlers:
        await event_handlers[event_name](event)
    
    user_func = user_event_handlers.get(f'on_{event_name.lower()}')
    if user_func:
        await user_func()