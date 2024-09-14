from db.session import get_collection

async def get_audio_collection():
    audio_collection = get_collection('audios')
    return audio_collection