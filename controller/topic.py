from aiohttp_session import get_session
from aiohttp import web
from form import TopicForm, ReplyForm
from router import routes
import aiohttp_jinja2
from factory import default
from models import TopicDAO
from ioa.database import DatabaseContext
from service.exceptions import NoPermission

topic_service = default.create_topic_service()

class TopicController:
    @staticmethod
    @routes.route("*", "/topic/new")
    @aiohttp_jinja2.template('/topic/new.html')
    async def topic_new(request):
        session = await get_session(request)
        post = await request.post()
        form = TopicForm(post)

        if "POST" == request.method and form.validate():
            topic = await topic_service.speak(form.data, session['user_id'])
            if topic:
                return web.HTTPFound("/t/%d" % topic['id'])
            else:
                return web.HTTPFound("/")
        return {
            'form': form
        }

    @staticmethod
    @routes.route("*", "/t/{id}/edit")
    @aiohttp_jinja2.template('/topic/new.html')
    async def tpic_edit(request):
        topic_id = int(request.match_info['id'])
        topic = None
        user = request['user']
        async with await DatabaseContext.default.engine.acquire() as connection:
            topic_dao = TopicDAO(connection)
            topic = await topic_dao.find(topic_id)
        if not topic:
            return web.HTTPNotFound()
        
        if not (topic['author_id'] == user.id):
            return web.HTTPForbidden()

        post = await request.post()
        form = TopicForm(post, topic)

        if "POST" == request.method and form.validate():
            await topic_service.edit(topic_id, user.id, form.data)
            return web.HTTPFound("/t/%d" % topic['id'])
        return {
            'form': form
        }

    @staticmethod
    @routes.delete('/t/{id}')
    async def delete(request):
        try:
            await topic_service.shutup(
                int(request.match_info['id']),
                request['user'].id
            )

            return web.HTTPFound('/')
        except NoPermission:
            return web.HTTPForbidden()

    @staticmethod
    @routes.route("*", "/t/{id}", name="topic_detail")
    @aiohttp_jinja2.template('/topic/detail.html')
    async def topic_get(request):
        topic_id = int(request.match_info['id'])
        page = int(request.query.get("page", 1))

        if "POST" == request.method:
            post = await request.post()
            form = ReplyForm(post)

            if form.validate():
                reply = form.data.copy()
                reply['topic_id'] = topic_id
                session = await get_session(request)
                user_id = session['user_id']

                reply = await topic_service.reply(reply, user_id)

                return web.HTTPFound(
                    request.app.router['topic_detail'].url_for(id=str(topic_id))
                )
        else:
            form = ReplyForm()

        topic = await topic_service.detail(topic_id, page)
        return {
            "topic": topic,
            "form": form,
        }