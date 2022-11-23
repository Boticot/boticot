import functools
import os
from flask import request
from utils import response_template
from secrets import compare_digest
import json


def check_client(client_id, client_secret_key):
    dict_api_key = json.loads(os.environ.get("API_KEY"))
    if client_id in dict_api_key and compare_digest(dict_api_key[client_id], client_secret_key):
        return True
    return False


def api_auth_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        client_id = request.headers.get("Client-Id")
        client_secret_key = request.headers.get("Client-Secret-Key")
        if client_id is None or client_secret_key is None:
            return response_template(400, "Missing client id or client secret key")
        if check_client(client_id, client_secret_key):
            return func(*args, **kwargs)
        else:
            return response_template(401, "Not authorized, client id or client secret key is invalid")
    return decorator
