import motor.motor_asyncio

MONGODB_URL = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

def get_monogodb_client():
    client = MONGODB_URL
    return client

