from flask import Blueprint, current_app
import sys, os
sys.path.append(os.path.abspath(os.path.join("..", "persistence")))
sys.path.append("..")

from persistence.mongodb import mongo
current_app.config["MONGO_URI"] = os.environ.get("MONGO_CONNECTION_STRING")
mongo.init_app(current_app)

from flask_jwt_extended import JWTManager
jwt = JWTManager(current_app)
current_app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

from flask_cors import CORS
CORS(current_app)
routes = Blueprint("routes", __name__)

from .agent import *
from .training_data import *
from .user import *

from agents_service import AgentsService
AgentsService.get_instance().starting_load_agents()

from user_service import UserService
exist_user = UserService.get_instance().exist_user()
if not exist_user:
        UserService.get_instance().add_new_user(os.environ.get("ADMIN_LOGIN"), "Admin", "Admin", os.environ.get("ADMIN_PWD"))

@current_app.route( "/", methods=["GET"])
def index():
        return "Boticot API !"

@current_app.route( "/healthcheck", methods=["GET"])
def healthcheck():
        return "Boticot API Run OK"

@current_app.before_request   
def before_request_callback():
        if (request.view_args is not None):       
                agent_name = request.view_args.get("agent_name")      
                path = request.path       
                method = request.method
                if agent_name is not None and (method != "PUT" or path != "/nlu/agents/" + agent_name):
                        """Return 404 in case of non existing agent associated to agent_name used in path 
                        except creation case"""
                        if not AgentsService.get_instance().agent_exist(agent_name):
                                return response_template(404, "Agent {0} not found".format(agent_name))