from utils import response_template
from flask import request, jsonify
from flask_jwt_extended import jwt_required
import json
import sys
sys.path.append("..")
from agents_service import AgentsService
from flask import current_app

@current_app.route("/nlu/agents/<agent_name>/training-data", methods=["GET"])
@jwt_required
def get_training_data(agent_name):
    """Get training Data by agent_name, filters existing in query params: intent, page size and page number"""
    intent = request.args.get("intent", default = None, type = str)
    page_number = request.args.get("pageNumber", default = 1, type = int)
    page_size = request.args.get("pageSize", default = 30, type = int)
    data = AgentsService.get_instance().get_training_data(agent_name, intent, page_number, page_size)
    return jsonify(data)

@current_app.route("/nlu/agents/<agent_name>/training-data/<id>", methods=["DELETE"])
@jwt_required
def delete_trainingData(agent_name, id):
    if not AgentsService.get_instance().training_data_exist(id):
        return response_template(404, "Training Data not found for agent {0}".format(agent_name))
    AgentsService.get_instance().delete_agent_training_data(agent_name, id)
    return response_template(200, "Training Data was successfully deleted for agent {0}".format(agent_name))

@current_app.route("/nlu/agents/<agent_name>/training-data/<id>", methods=["PUT"])
@jwt_required
def update_training_data(agent_name, id):
    if not AgentsService.get_instance().training_data_exist(id):
        return response_template(404, "Training Data not found for agent {0}".format(agent_name))
    if request.get_data():
        request_data = json.loads((request.get_data()).decode())
        if (request_data.get("data") and not isinstance(request_data.get("data"), list)):
            AgentsService.get_instance().update_agent_training_data(agent_name, id, request_data["data"])
            return response_template(200, "Training Data was successfully updated for agent {0}".format(agent_name))
        else:
            return response_template(400, "Should Contains valid data inside body request")
    else:
        return response_template(400, "A body is mandatory inside the request")

@current_app.route("/nlu/agents/<agent_name>/training-data", methods=["POST"])
@jwt_required
def add_training_data(agent_name):
    if request.get_data():
        request_data = json.loads((request.get_data()).decode())
        if (request_data.get("data") and isinstance(request_data.get("data"), list)):
            AgentsService.get_instance().add_agent_training_data(agent_name, request_data["data"])
            if request_data.get("responses"):
                AgentsService.get_instance().add_agent_responses(agent_name, request_data["responses"])
            return response_template(200, "Training Data was successfully added for agent {0}".format(agent_name))
        else:
            return response_template(400, "Should Contains valid data object with array of training Data")
    else:
        return response_template(400, "A body is mandatory inside the request")