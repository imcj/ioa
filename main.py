import os
import asyncio
import aiohttp_jinja2
import jinja2
import aiomysql
from aiohttp import web

routes = web.RouteTableDef()
loop = None
pool = None


@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def hello(request):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT 42;")
            (r,) = await cur.fetchone()
    return {

    }

loop = asyncio.get_event_loop()

async def init_database():
    global pool
    config = {
        "host": '127.0.0.1',
        "port": 3306,
        "user": "root",
        "password": "",
        "db": "test",
        "loop": loop,
        "maxsize": 100
    }
    pool = await aiomysql.create_pool(**config)

loop.run_until_complete(init_database())


app = web.Application()
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader(os.path.abspath('./templates')))

app.add_routes(routes)
web.run_app(app)
