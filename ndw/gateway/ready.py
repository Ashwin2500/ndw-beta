from .handler import register, extractor

@register("READY")
async def ready(event,bot):
    keys = event['d']['user']
    print(keys)
    bot.update_user(bot,data=event['d']['user'])
    pass


@extractor("READY")
def ready_extract(event):
    pass