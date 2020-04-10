import os
import jinja2
import humanize
import aiohttp_jinja2

import markdown
import bleach


def naturaldelta(datetime):
    return humanize.naturaldelta(datetime)


def setup(app):
    env = aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(os.path.abspath('./templates')),
    )
    env.filters['naturaldelta'] = naturaldelta
    env.filters['markdown'] = lambda x: markdown.markdown(
        x, extensions=['markdown.extensions.tables']
    )
    env.filters['bleach'] = lambda x: bleach.clean(x)
