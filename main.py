import os
from aiohttp import web
import aiohttp_jinja2
import jinja2

routes = web.RouteTableDef()


@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def hello(request):
    # return web.Response(text="Hello, world")
    return {

    }

app = web.Application()
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader(os.path.abspath('./templates')))

app.add_routes(routes)
web.run_app(app)