import os
import asyncio
from aiomysql.sa import create_engine


async def init(app):
    loop = asyncio.get_event_loop()
    config = {
        "host": os.getenv('DATABASE_HOST', '127.0.0.1'),
        "port": int(os.getenv('DATABASE_PORT', 3306)),
        "user": os.getenv('DATABASE_USER', 'root'),
        "password": os.getenv('DATABASE_PASSWORD', ''),
        "db": os.getenv('DATABASE_NAME', 'test'),
        "loop": loop,
        # "pool_size": 100
    }
    engine = await create_engine(**config)
    app['engine'] = engine
