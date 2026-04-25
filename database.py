from motor.motor_asyncio import AsyncIOMotorClient
import config

class Database:
    client: AsyncIOMotorClient = None

    @classmethod
    def connect(cls):
        cls.client = AsyncIOMotorClient(config.MONGODB_URI)
        print("Connected to MongoDB")

    @classmethod
    def disconnect(cls):
        if cls.client:
            cls.client.close()
            print("Disconnected from MongoDB")

    @property
    def db(self):
        return self.client[config.DB_NAME]

    def __getattr__(self, name):
        # Allows db.welcome instead of db.db.welcome
        return getattr(self.client[config.DB_NAME], name)

db = Database()
