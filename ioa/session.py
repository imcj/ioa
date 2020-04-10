import base64
import aiohttp_session
from cryptography import fernet
from aiohttp_session.cookie_storage import EncryptedCookieStorage


def get_session_middleware():
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(base64.urlsafe_b64encode((" " * 32).encode()))
    return aiohttp_session.session_middleware(EncryptedCookieStorage(secret_key))
