import ioa
import time
import ioa.session
from aiohttp_session import get_session
from models import UserDAO
from view.model.user import AnonymousUser, User
from aiohttp.web import middleware


@middleware
async def caculate_execute_time_middleware(request, handler):
    start = time.time()
    request['request_began_at'] = time.time()
    request['now'] = lambda: time.time()
    response = await handler(request)
    request['executed_time'] = time.time() - start
    # logging.info("request duration %.4f" % (time.time() - start, ))
    return response


@middleware
async def user_middleware(request, handler):
    session = request['session']

    if 'user_id' in session:
        user_id = session['user_id']
        dao = UserDAO()
        user_table = await dao.find(user_id)
        if not user_table:
            user = AnonymousUser()
        else:
            user = User()
            user.id = user_table['id']
            user.username = user_table['username']
    else:
        user = AnonymousUser()
    request['user'] = user
    request['aiohttp_jinja2_context'] = {
        'user': user,
        'request': request
    }
    response = await handler(request)
    return response


@middleware
async def session_to_request_middleware(request, handler):
    session = await get_session(request)
    request['session'] = session

    return await handler(request)


def connection_middleware(app):
    @middleware
    async def _connection_middleware(request, handler):
        connection = await app['engine'].acquire()
        request['connection'] = connection
        ioa.connection_context.set(connection)
        response = await handler(request)
        await connection.close()
        return response

    return _connection_middleware


def setup_middleware(app):
    app.middlewares.append(connection_middleware(app))
    app.middlewares.append(ioa.session.get_session_middleware())
    app.middlewares.append(session_to_request_middleware)
    app.middlewares.append(user_middleware)
    # app.middlewares.append(caculate_execute_time_middleware)
    pass
