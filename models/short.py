from db.session import get_collection

async def get_shorts_collection():
    shorts_collection = get_collection('shorts')
    return shorts_collection