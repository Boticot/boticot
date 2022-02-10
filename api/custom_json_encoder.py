from werkzeug.http import http_date
from flask.json import JSONEncoder
from datetime import datetime


class CustomJSONEncoder(JSONEncoder):
    def custom_default(self, o):
        if isinstance(o, datetime):
            return http_date(o)
        return JSONEncoder.default(self, o)
