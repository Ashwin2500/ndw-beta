from . import *
import inspect

event_handlers = {}
user_event_handlers = {}
extractors = {}

def register(event_name):
    def decorator(func):
        event_handlers[event_name] = func
        return func
    return decorator

def set_user_handelers(handelers):
    global user_event_handlers
    user_event_handlers = handelers

def extractor(event_name):
    def decorator(func):
        extractors[event_name]= func
        return func
    return decorator

async def handle(event):
    event_name = event.get('t')
    if not event_name:
        return
    
    if event_name in event_handlers:
        await event_handlers[event_name](event)
    data = None
    if event_name in extractors:
        data = extractors[event_name](event)
    user_func = user_event_handlers.get(f'on_{event_name.lower()}')
    if user_func:
        if isinstance(data, dict):
            keys = inspect.signature(user_func)
            params = keys.parameters.keys()

            args = {key: value for key,value in data.items() if key in params}
            await user_func(**args)
        else:
            await user_func()