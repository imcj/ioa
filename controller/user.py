from aiohttp import web
from form import RegistrationForm, LoginForm
from router import routes
import aiohttp_jinja2
from models import CredentailInvalid
from service.exceptions import DuplicatedUser
from aiohttp.web_request import Request
from service import UserService


@routes.view("/user/registration")
class UserRegistrationView(web.View):

    def __init__(self, request: Request):
        super(UserRegistrationView, self).__init__(request)
        self.service = UserService()

    @aiohttp_jinja2.template('user/registration.html')
    async def get(self):
        form = RegistrationForm()

        return {
            "form": form
        }

    @aiohttp_jinja2.template('user/registration.html')
    async def post(self):
        post = await self.request.post()
        form = RegistrationForm(post)

        if form.validate():
            try:
                user = await self.service.register(form.data)
                self.request['session']['user_id'] = user['id']
                return web.HTTPFound("/")
            except DuplicatedUser as e:
                form.username.errors.append(e)

        return {
            'form': form
        }


@routes.view("/user/login")
class UserLoginView(web.View):
    def __init__(self, request: Request):
        super(UserLoginView, self).__init__(request)
        self.service = UserService()

    @aiohttp_jinja2.template('user/login.html')
    async def get(self):
        return {
            "form": LoginForm(),
            "errors": []
        }

    @aiohttp_jinja2.template('user/login.html')
    async def post(self):
        post = await self.request.post()
        form = LoginForm(post)
        errors = []

        if form.validate():
            try:
                user = await self.service.login(form.data)
                self.request['session']['user_id'] = user['id']
                return web.HTTPFound("/")
            except CredentailInvalid:
                errors = ['用户名或密码无效']

        return {
            "form": form,
            "errors": errors
        }


@routes.view("/user/logout")
class UserLogoutView(web.View):

    async def get(self):
        del self.request['session']['user_id']

        return web.HTTPFound("/")
