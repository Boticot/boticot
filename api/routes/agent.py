import os
from utils import response_template, remove_file_or_dir, create_folder
from flask import request, jsonify
from flask_jwt_extended import jwt_required
import json
import sys
sys.path.append("..")
from agents_service import AgentsService
from flask import current_app, send_from_directory

@current_app.route("/nlu/agents", methods=["GET"])
@jwt_required
def get_all_agents():
    agents = AgentsService.get_instance().get_agents()
    return jsonify(agents)

@current_app.route("/nlu/agents/<agent_name>", methods=["GET"])
@jwt_required
def get_agent(agent_name):
    agent = AgentsService.get_instance().get_agent(agent_name)
    return jsonify(agent)


@current_app.route("/nlu/agents/<agent_name>/export", methods=["GET"])
@jwt_required
def get_agent_file(agent_name):
    directory_name = os.environ.get("MODELS_PATH") + "export/" 
    file_name = agent_name + ".json"
    file_path = directory_name + file_name
    remove_file_or_dir(file_path)
    dic = AgentsService.get_instance().create_agent_file(agent_name)
    create_folder(directory_name)
    with open(file_path, "w+") as f:
        json.dump(dic,f)
    return(send_from_directory(directory = directory_name, filename = "./" + file_name, as_attachment = True))

@current_app.route("/nlu/agents", methods=["PUT"])
@jwt_required
def create_agent():
    agent_name = ""
    if request.files:
        """Create agent from file in the case of file uploading"""
        file_key = list(request.files)[0]
        data = json.loads(request.files[file_key].read().decode())
        agent_name = data.get("name")
        if agent_name is None or agent_name == "":
            return response_template(400, "Agent name field is mandatory")
        elif AgentsService.get_instance().agent_exist(agent_name):
            return response_template(400, "Already existing agent with name {0}".format(agent_name))
        elif data.get("config") is None:
            return response_template(400, "Should Contains config field inside file data")
        AgentsService.get_instance().create_agent(agent_name, 0, data.get("config"), data.get("rasa_nlu_data"), data.get("fallback"), data.get("responses"), data.get("current_version"))
    elif request.get_data():
        """Create agent with data passed directly inside query"""
        request_data = json.loads((request.get_data()).decode())
        agent_name = request_data.get("name")
        if agent_name is None or agent_name == "":
            return response_template(400, "Agent name field is mandatory")
        elif AgentsService.get_instance().agent_exist(agent_name):
            return response_template(400, "Already existing agent with name {0}".format(agent_name))
        elif request_data.get("config") is None:
            return response_template(400, "Should Contains config field inside body request")
        AgentsService.get_instance().create_agent(agent_name, 0, request_data.get("config"), request_data.get("rasa_nlu_data"), request_data.get("fallback"), request_data.get("responses"), request_data.get("current_version"))
    else:
        return response_template(400, "Shoulds Contains a valid body or file of new Agent") 
    return response_template(201, "Agent {0} successfully created".format(agent_name))

@current_app.route("/nlu/agents/<agent_name>", methods=["DELETE"])
@jwt_required
def delete_agent(agent_name):
    AgentsService.get_instance().delete_agent(agent_name)
    return response_template(200, "Agent {0} successfully deleted".format(agent_name))

@current_app.route("/nlu/agents/<agent_name>/parse", methods=["POST"])
def parse(agent_name):
    """Parse a text to get nlu response with intent/entities assosciated"""
    if request.get_data():
        query = (json.loads((request.get_data()).decode()))["text"]
        user_id = (json.loads((request.get_data()).decode())).get("user_id")
        bot = ((AgentsService.get_instance().get_bots()).get(agent_name))
        if bot is not None:
            nlu_response = bot.handle(query, agent_name, user_id)
            if (request.args.get("test") is None or request.args.get("test").lower() != "true"):
                AgentsService.get_instance().store_user_input(agent_name, dict(nlu_response), user_id)
            return jsonify(nlu_response)
        else:
            return response_template(404, "Agent {0} not found".format(agent_name))
    else:
        return response_template(400, "A body is mandatory inside the request")

@current_app.route("/nlu/agents/<agent_name>/inputs", methods=["GET"])
@jwt_required
def get_agent_inputs(agent_name):
    min_confidence = request.args.get("minConfidence", default = 0, type = float)
    max_confidence = request.args.get("maxConfidence", default = 1, type = float)
    page_number = request.args.get("pageNumber", default = 1, type = int)
    page_size = request.args.get("pageSize", default = 20, type = int)
    agent_inputs = AgentsService.get_instance().get_agent_inputs(agent_name, max_confidence, min_confidence, page_number, page_size)
    return jsonify(agent_inputs)

@current_app.route("/nlu/agents/<agent_name>/inputs/<id>", methods=["DELETE"])
@jwt_required
def delete_input(agent_name, id):
    AgentsService.get_instance().delete_agent_user_input(agent_name, id)
    return response_template(200, "User Input was successfully deleted for agent {0}".format(agent_name))

@current_app.route("/nlu/agents/<agent_name>/lookup", methods=["PUT"])
@jwt_required
def add_lookups(agent_name):
    if request.get_data():
        request_data = json.loads((request.get_data()).decode())
        AgentsService.get_instance().add_agent_lookups(agent_name, request_data["data"])
        return response_template(200, "Lookup successfully added for agent {0}".format(agent_name))
    else:
        return response_template(400, "A body is mandatory inside the request")

@current_app.route("/nlu/agents/<agent_name>/synonyms", methods = ["PUT"])
@jwt_required
def add_synonyms(agent_name):
    if request.get_data():
        request_data = json.loads((request.get_data()).decode())
        AgentsService.get_instance().add_agent_synonyms(request_data["agent_name"], request_data["data"])
        return response_template(200, "Synonyms successfully added for agent {0}".format(agent_name))
    else:
        return response_template(400, "A body is mandatory inside the request")

@current_app.route("/nlu/agents/<agent_name>/model", methods = ["PUT"])
@jwt_required
def set_specific_model(agent_name):
    if request.get_data():
        request_data = json.loads((request.get_data()).decode())
        if AgentsService.get_instance().load_agent(agent_name = agent_name, model_name = request_data.get("modelName")):
            return("Model " + request_data.get("modelName") + " loaded for bot " + agent_name)
        else:
            return("Can't load model " + request_data.get("modelName") + "for bot " + agent_name)
    else:
        return response_template(400, "A body is mandatory inside the request")



