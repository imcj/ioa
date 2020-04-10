import functools
import contextvars

connection_context = contextvars.ContextVar('connection')


def transaction():
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            connection = connection_context.get()
            _transaction = await connection.begin()
            try:
                returns = await func(*args, **kwargs)
            except Exception as e:
                _transaction.rollback()
                raise e
            await _transaction.commit()
            return returns
        return wrapped

    return wrapper
