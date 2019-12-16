import PyRSS2Gen
import markdown
import bleach
from router import routes
from aiohttp import web
from ioa.database import DatabaseContext
from models.dao.topic import TopicDAO
from io import StringIO

@routes.get("/rss.xml")
async def rss(request):
    engine = DatabaseContext.default.engine
    async with engine.acquire() as connection:
        topic_dao = TopicDAO(connection)
        topics = await topic_dao.latest100()
    
    rss = PyRSS2Gen.RSS2(
        title="DOIST",
        link="https://doist.cn/",
        description=u"实干家",
        lastBuildDate="",
        items = [
            PyRSS2Gen.RSSItem(
                title=topic['title'],
                link="https://doist.cn/t/%d" % (topic['id'],),
                description=markdown.markdown(
                    bleach.clean(topic['content']),
                    extensions=['markdown.extensions.tables']
                ),
                guid="https://doist.cn/t/%d" % (topic['id'],),
                pubDate=topic['created_at'],
            )
            for topic in topics
        ]
    )
    response = web.StreamResponse(headers={ 'Content-Type': 'text/xml'})
    await response.prepare(request)
    buf = StringIO()
    rss.write_xml(buf, 'utf-8')

    await response.write(buf.getvalue().encode('utf-8'))

    return response