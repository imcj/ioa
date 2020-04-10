import PyRSS2Gen
import markdown
import bleach
from router import routes
from aiohttp import web
from models.dao.topic import TopicDAO
from io import StringIO
from aiohttp.web_request import Request


@routes.view("/rss.xml")
class RssView(web.View):
    def __init__(self, request: Request):
        super(RssView, self).__init__(request)
        self.topic_dao = TopicDAO()

    async def get(self):
        topics = await self.topic_dao.latest100()

        rss = PyRSS2Gen.RSS2(
            title="DOIST",
            link="https://doist.cn/",
            description=u"实干家",
            lastBuildDate="",
            items=[
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
        response = web.StreamResponse(headers={'Content-Type': 'text/xml'})
        await response.prepare(self.request)
        buf = StringIO()
        rss.write_xml(buf, 'utf-8')

        await response.write(buf.getvalue().encode('utf-8'))

        return response
