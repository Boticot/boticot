from utils import response_template
from flask import request, jsonify
from flask_jwt_extended import jwt_required
import json
import sys
sys.path.append("..")
from agents_service import AgentsService
from flask import current_app


@current_app.route("/nlu/agents/<agent_name>/regex", methods=["GET"])
@jwt_required
def get_regex(agent_name):
    data = AgentsService.get_instance().get_regex(agent_name)
    return jsonify(data)

@current_app.route("/nlu/agents/<agent_name>/regex", methods=["POST"])
@jwt_required
def add_regex(agent_name):
    if request.get_data():
        request_data = json.loads((request.get_data()).decode())
        if (request_data.get("data") and isinstance(request_data.get("data"), list)):
            AgentsService.get_instance().add_agent_regex(agent_name, request_data["data"])
            return response_template(200, "Regex was successfully added for agent {0}".format(agent_name))
        else:
            return response_template(400, "Should contain valid regex array object")
    else:
        return response_template(400, "A body is mandatory inside the request")

@current_app.route("/nlu/agents/<agent_name>/regex/<id>", methods=["DELETE"])
@jwt_required
def delete_regex(agent_name, id):
    if not AgentsService.get_instance().regex_exist(id):
        return response_template(404, "Regex not found for agent {0}".format(agent_name))
    AgentsService.get_instance().delete_agent_regex(agent_name, id)
    return response_template(200, "Regex was successfully deleted for agent {0}".format(agent_name))

@current_app.route("/nlu/agents/<agent_name>/regex/<id>", methods=["PUT"])
@jwt_required
def update_regex(agent_name, id):
    if not AgentsService.get_instance().regex_exist(id):
        return response_template(404, "Regex not found for agent {0}".format(agent_name))
    if request.get_data():
        request_data = json.loads((request.get_data()).decode())
        if (request_data.get("data") and not isinstance(request_data.get("data"), list)):
            AgentsService.get_instance().update_agent_regex(agent_name, id, request_data["data"])
            return response_template(200, "Regex was successfully updated for agent {0}".format(agent_name))
        else:
            return response_template(400, "Should contain valid data inside body request")
    else:
        return response_template(400, "A body is mandatory inside the request")
