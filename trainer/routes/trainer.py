import os
from . import routes
from flask import current_app

@current_app.route( "/", methods=["GET"])
def index():
    return "Boticot Trainer !"

@current_app.route( "/healthcheck", methods=["GET"])
def healthcheck():
        return "Boticot Trainer Run OK"

@current_app.route( "/nlu/agents/<agentName>/training", methods=["POST"])
def train(agentName):
    raise NotImplementedError("Train method is not yet implemented !")
