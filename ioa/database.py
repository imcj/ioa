import os
import logging
from aiomysql.sa import create_engine

class DatabaseContext:
    default = None
    engine = None

DatabaseContext.default = DatabaseContext()

async def init(loop):
    logging.info('opening database')
    config = {
        "host": os.getenv('DATABASE_HOST', '127.0.0.1'),
        "port": int(os.getenv('DATABASE_PORT', 3306)),
        "user": os.getenv('DATABASE_USER', 'root'),
        "password": os.getenv('DATABASE_PASSWORD', ''),
        "db": os.getenv('DATABASE_NAME', 'test'),
        "loop": loop,
        # "pool_size": 100
    }
    logging.info(config)
    engine = await create_engine(**config)
    DatabaseContext.default.engine = engine
    print("database initialized.")
    