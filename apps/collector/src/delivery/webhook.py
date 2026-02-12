"""Alert webhook dispatcher — V2."""
# TODO: POST to user webhook URL on alert match
async def dispatch_webhook(url: str, payload: dict) -> bool:
    """Send payload to webhook URL."""
    return False
