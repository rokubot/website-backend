from motor.motor_asyncio import AsyncIOMotorClient
import config

class Database:
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    def connect(cls):
        cls.client = AsyncIOMotorClient(config.MONGODB_URI)
        cls.db = cls.client[config.DB_NAME]
        print("Connected to MongoDB")

    @classmethod
    def disconnect(cls):
        if cls.client:
            cls.client.close()
            print("Disconnected from MongoDB")

db = Database()
