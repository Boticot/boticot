from datetime import datetime
from bson import ObjectId
from flask.json import JSONEncoder
from werkzeug.routing import BaseConverter

class MongoJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

class ObjectIdConverter(BaseConverter):
    def to_python(self, value):
        return ObjectId(value)

    def to_url(self, value):
        return str(value)