from utils import response_template
from flask import request, jsonify
from flask_jwt_extended import jwt_required
import json
import sys
sys.path.append("..")
from synonyms_service import SynonymsService
from flask import current_app

@current_app.route("/nlu/agents/<agent_name>/synonyms", methods=["GET"])
@jwt_required
def get_synonyms(agent_name):
    data = SynonymsService.get_instance().get_synonyms(agent_name)
    return jsonify(data)

@current_app.route("/nlu/agents/<agent_name>/synonyms/<id>", methods=["DELETE"])
@jwt_required
def delete_synonym(agent_name, id):
    if not SynonymsService.get_instance().synonym_exist(id):
        return response_template(404, "Synonym not found for agent {0}".format(agent_name))
    SynonymsService.get_instance().delete_agent_synonym(agent_name, id)
    return response_template(200, "Synonym was successfully deleted for agent {0}".format(agent_name))

@current_app.route("/nlu/agents/<agent_name>/synonyms/<id>", methods=["PUT"])
@jwt_required
def update_synonym(agent_name, id):
    if not SynonymsService.get_instance().synonym_exist(id):
        return response_template(404, "Synonym not found for agent {0}".format(agent_name))
    if request.get_data():
        request_data = json.loads((request.get_data()).decode())
        if (request_data.get("synonyms") and not isinstance(request_data.get("synonyms"), list)):
            SynonymsService.get_instance().update_agent_synonym(agent_name, id, request_data["synonyms"])
            return response_template(200, "Synonym was successfully updated for agent {0}".format(agent_name))
        else:
            return response_template(400, "Should contain valid synonyms inside body request")
    else:
        return response_template(400, "A body is mandatory inside the request")

@current_app.route("/nlu/agents/<agent_name>/synonyms", methods = ["POST"])
@jwt_required
def add_synonyms(agent_name):
    if request.get_data():
        request_data = json.loads((request.get_data()).decode())
        if (request_data.get("synonyms") and isinstance(request_data.get("synonyms"), list)):
            SynonymsService.get_instance().add_agent_synonyms(agent_name, request_data["synonyms"])
            return response_template(200, "Synonyms successfully added for agent {0}".format(agent_name))
        else:
            return response_template(400, "Should contain valid synonyms array object")
    else:
        return response_template(400, "A body is mandatory inside the request")
