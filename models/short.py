from db.session import get_collection

async def get_short_collection():
    short_collection = get_collection('shorts')
    return short_collection