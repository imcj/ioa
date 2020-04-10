import aiohttp_jinja2
import service

from aiohttp import web
from form import TopicForm, ReplyForm
from router import routes
from models import TopicDAO
from service.exceptions import NoPermission
from aiohttp.web_request import Request


@routes.view("/t/{id}", name="topic_detail")
class TopicDetailView(web.View):

    def __init__(self, request: Request):
        super(TopicDetailView, self).__init__(request)
        self.service = service.TopicService()

    @property
    def topic_id(self):
        topic_id = int(self.request.match_info['id'])
        return topic_id

    @aiohttp_jinja2.template('/topic/detail.html')
    async def get(self):
        page = int(self.request.query.get("page", 1))
        form = ReplyForm()

        topic = await self.service.detail(self.topic_id, page)
        return {
            "topic": topic,
            "form": form,
        }

    @aiohttp_jinja2.template('/topic/detail.html')
    async def post(self):
        post = await self.request.post()
        form = ReplyForm(post)

        if form.validate():
            reply = form.data.copy()
            reply['topic_id'] = self.topic_id
            user_id = self.request['session']['user_id']

            await self.service.reply(reply, user_id)

            return web.HTTPFound(
                self.request.app.router['topic_detail'].url_for(id=str(self.topic_id))
            )


@routes.view("/t/{id}/edit")
class TopicEditView(web.View):

    def __init__(self, request: Request):
        super(TopicEditView, self).__init__(request)
        self.topic_dao = TopicDAO()
        self.service = service.TopicService()

    async def guard(self):
        topic_id = int(self.request.match_info['id'])
        user = self.request['user']
        topic = await self.topic_dao.find(topic_id)
        if not topic:
            return user, topic, web.HTTPNotFound()

        if not (topic['author_id'] == user.id):
            return user, topic, web.HTTPForbidden()

        return user, topic, None

    @aiohttp_jinja2.template('/topic/new.html')
    async def get(self):
        _, topic, response = await self.guard()
        if response:
            return response

        form = TopicForm(obj=topic)

        return {
            'form': form
        }

    @aiohttp_jinja2.template('/topic/new.html')
    async def post(self):
        user, topic, response = await self.guard()
        if response:
            return response

        post = await self.request.post()
        form = TopicForm(post, topic)

        if form.validate():
            await self.service.edit(topic.id, user.id, form.data)
            return web.HTTPFound("/t/%d" % topic['id'])

        return {
            'form': form
        }


@routes.view("/topic/new")
class TopicCreationView(web.View):
    def __init__(self, request: Request):
        super(TopicCreationView, self).__init__(request)
        self.service = service.TopicService()

    @aiohttp_jinja2.template('/topic/new.html')
    async def get(self):
        return {
            'form': TopicForm()
        }

    @aiohttp_jinja2.template('/topic/new.html')
    async def post(self):
        form = TopicForm(await self.request.post())
        if form.validate():
            topic = await self.service.speak(form.data, self.request['session']['user_id'])
            if topic:
                return web.HTTPFound("/t/%d" % topic['id'])
            else:

                return web.HTTPFound("/")
        return {
            'form': form
        }


@routes.view('/t/{id}')
class TopicDeleteView(web.View):
    def __init__(self, request: Request):
        super(TopicDeleteView, self).__init__(request)
        self.service = service.TopicService()

    async def delete(self):
        try:
            await self.service.shutup(
                int(self.request.match_info['id']),
                self.request['user'].id
            )

            return web.HTTPFound('/')
        except NoPermission:
            return web.HTTPForbidden()
