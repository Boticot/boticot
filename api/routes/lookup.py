from utils import response_template
from flask import request, jsonify
from flask_jwt_extended import jwt_required
import json
import sys
sys.path.append("..")
from agents_service import AgentsService
from flask import current_app


@current_app.route("/nlu/agents/<agent_name>/lookups", methods=["GET"])
@jwt_required
def get_lookups(agent_name):
    data = AgentsService.get_instance().get_lookups(agent_name)
    return jsonify(data)

@current_app.route("/nlu/agents/<agent_name>/lookups", methods=["POST"])
@jwt_required
def add_lookups(agent_name):
    if request.get_data():
        request_data = json.loads((request.get_data()).decode())
        if (request_data.get("data") and isinstance(request_data.get("data"), list)):
            AgentsService.get_instance().add_agent_lookups(agent_name, request_data["data"])
            return response_template(200, "Lookups successfully added for agent {0}".format(agent_name))
        else:
            return response_template(400, "Should contain valid lookups array object")
    else:
        return response_template(400, "A body is mandatory inside the request")

@current_app.route("/nlu/agents/<agent_name>/lookups/<lookup_name>", methods=["DELETE"])
@jwt_required
def delete_lookup(agent_name, lookup_name):
    if not AgentsService.get_instance().lookup_exist(agent_name, lookup_name):
        return response_template(404, "Lookup not found for agent {0}".format(agent_name))
    AgentsService.get_instance().delete_agent_lookup(agent_name, lookup_name)
    return response_template(200, "Lookup was successfully deleted for agent {0}".format(agent_name))
