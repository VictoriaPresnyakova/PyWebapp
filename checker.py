from flask import session
from functools import wraps


def check_logged_in(func: object) -> object:
    @wraps(func)
    def wrapper():
        if 'logged_in' in session:
            return func()
        return 'You are NOT logged in'
    return wrapper
