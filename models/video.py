from db.session import get_collection


async def get_video_collection():
    video_collection = get_collection('videos')
    return video_collection
