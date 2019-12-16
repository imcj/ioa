import asyncio
import logging
from aiohttp import web
from router import routes
from ioa.database import init as init_database
from ioa.jinja import setup as setup_jinja
from ioa.session import setup as setup_session
from middlewares import setup_middleware, caculate_execute_time_middleware

from dotenv import load_dotenv
load_dotenv()


logging.basicConfig(level=logging.DEBUG)
loop = asyncio.get_event_loop()

loop.run_until_complete(init_database(loop))
app = web.Application()
app.middlewares.append(caculate_execute_time_middleware)
setup_jinja(app)
setup_session(app)
setup_middleware(app)

import controller
import os
app.add_routes([web.static('/static', os.path.abspath('./static'))])
app.add_routes(routes)
web.run_app(app, port=3000, host='0.0.0.0')
