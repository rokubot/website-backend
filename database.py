import asyncpg

import config


class Database:
    pool: asyncpg.Pool | None = None

    async def connect(self):
        if not config.DATABASE_URL:
            raise RuntimeError("DATABASE_URL environment variable is required")

        self.pool = await asyncpg.create_pool(dsn=config.DATABASE_URL)
        print("Connected to PostgreSQL")

    async def disconnect(self):
        if self.pool is not None:
            await self.pool.close()
            self.pool = None
            print("Disconnected from PostgreSQL")

    def __getattr__(self, name):
        if self.pool is None:
            raise RuntimeError("PostgreSQL connection pool is not initialized")
        return getattr(self.pool, name)


db = Database()
