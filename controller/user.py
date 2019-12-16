from aiohttp import web
from aiohttp_session import get_session
from form import RegistrationForm, LoginForm
from router import routes
import aiohttp_jinja2
from factory import default
from models import CredentailInvalid
from service.exceptions import DuplicatedUser

user_service = default.create_user_service()
class UserController:
    
    @staticmethod
    @routes.route("*", "/user/registration")
    @aiohttp_jinja2.template('user/registration.html')
    async def registration(request):
        session = await get_session(request)
        post = await request.post()
        form = RegistrationForm(post)
        
        if "POST" == request.method and form.validate():
            try:
                user = await user_service.register(form.data)
                session['user_id'] = user['id']
                return web.HTTPFound("/")
            except DuplicatedUser as e:
                form.username.errors.append(e)

        return {
            "form": form
        }

    @staticmethod
    @routes.route("*", "/user/login")
    @aiohttp_jinja2.template('user/login.html')
    async def login(request):
        session = await get_session(request)
        post = await request.post()
        form = LoginForm(post)
        errors = []
        
        if "POST" == request.method and form.validate():
            try:
                user = await user_service.login(form.data)
                session['user_id'] = user['id']
                return web.HTTPFound("/")
            except CredentailInvalid:
                errors = ['用户名或密码无效']

        return {
            "form": form,
            "errors": errors
        }
    @staticmethod
    @routes.get("/user/logout")
    async def logout(request):
        del request['session']['user_id']

        return web.HTTPFound("/")