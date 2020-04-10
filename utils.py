import random
import hashlib

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def hash(password, salt):
    h = hashlib.sha256()
    h.update(salt.encode())
    h.update(password.encode())

    return h.hexdigest()


def rand(length=16):
    return ''.join([random.choice(ALPHABET) for i in range(length)])
