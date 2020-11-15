from flask import Blueprint, current_app
import sys, os
sys.path.append(os.path.abspath(os.path.join("..", "persistence")))
sys.path.append("..")

from persistence.mongodb import mongo
current_app.config["MONGO_URI"] = os.environ.get("MONGO_CONNECTION_STRING")
mongo.init_app(current_app)

from flask_cors import CORS
CORS(current_app)
routes = Blueprint("routes", __name__)

from .trainer import *