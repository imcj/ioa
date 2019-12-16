import base64
from cryptography import fernet
from aiohttp_session import setup as setup_session, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

def setup(app):
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(base64.urlsafe_b64encode((" " * 32 ).encode()))
    setup_session(app, EncryptedCookieStorage(secret_key))