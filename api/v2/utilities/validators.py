from flask import request
from functools import wraps

def validate_bouquet_adding(func):
    @wraps(func)
    def wrapper():
        if func.__name__ == 'post':
            request_data = request.get_json()
            return func()
        return func()
    return wrapper
