import aiohttp_jinja2
import config
import service
from aiohttp import web
from router import routes
from aiohttp.web_request import Request


@routes.view("/", name='home')
class HomeView(web.View):

    def __init__(self, request: Request):
        super(HomeView, self).__init__(request)
        self.service = service.TopicService()

    @aiohttp_jinja2.template('index.html')
    async def get(self):
        request = self.request
        page = int(request.query.get("page", '1'))
        import paginate

        topics = await self.service.topics(page)

        p = paginate.Pagination(
            page=page,
            page_parameter="page",
            per_page=config.PER_PAGE_SIZE,
            per_page_parameter="per_page",
            total=topics['count'],
            alignment="center"
        )

        def page_href(page):
            if not page:
                return ""
            return request.app.router['home'].url_for().with_query({"page": page})

        p.page_href = page_href

        return {
            "topics": topics['topics'],
            "pagination": p,
        }
