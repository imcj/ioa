from aiohttp_session import get_session
from router import routes
import aiohttp_jinja2
from factory import default
import config

topic_service = default.create_topic_service()

class HomeController:
    @staticmethod
    @routes.get("/", name="home")
    @aiohttp_jinja2.template('index.html')
    async def home(request):
        page = int(request.query.get("page", 1))
        import paginate
        
        topics = await topic_service.topics(page)
        print(topics['count'])

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
            # 'request': request,
        }