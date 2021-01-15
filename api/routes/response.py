from utils import response_template
from flask import request, jsonify
import json
import sys
sys.path.append("..")
from responses_service import ResponsesService
from flask import current_app

@current_app.route("/responses/agents/<agent_name>/intents/<intent>", methods=["GET"])
def get_responses(agent_name, intent):
    """Get an array of responses by agent_name and intent"""
    data = ResponsesService.get_instance().get_agent_responses_by_intent(agent_name, intent)
    return jsonify(data)

@current_app.route("/responses/agents/<agent_name>", methods=["PUT"])
def add_response(agent_name):
    """Add a response associated to an agent name and intent"""
    if request.get_data():
        request_data = json.loads((request.get_data()).decode())
        if (request_data.get("responses") and isinstance(request_data.get("responses"), list)):
            ResponsesService.get_instance().add_agent_responses(agent_name, request_data["responses"])
            return response_template(200, "Responses was successfully added for agent {0}".format(agent_name))
        else:
            return response_template(400, "Should Contains valid responses array object")
    else:
        return response_template(400, "A body is mandatory inside the request")

@current_app.route("/responses/<id>", methods=["DELETE"])
def delete_response(id):
    """Remove a response by id"""
    ResponsesService.get_instance().delete_response(id)
    return response_template(200, "Response with id {0} successfully deleted".format(id))
