from .handler import register

@register("READY")
async def ready(event):
    pass

def extract_ready(event):
    pass