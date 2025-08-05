from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

mongo_client: AsyncIOMotorClient = None
_db = None  # Make db private

async def connect_to_mongo():
    global mongo_client, _db
    mongo_client = AsyncIOMotorClient(settings.mongo_uri)
    _db = mongo_client["tsetmc_data"]

def get_db():
    if _db is None:
        raise RuntimeError("MongoDB not initialized. Make sure connect_to_mongo() was called.")
    return _db
