from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask import current_app
from agents_service import AgentsService

@current_app.route("/nlu/agents/<agent_name>/users/<user_id>", methods=["GET"])
@jwt_required
def get_user_inputs(agent_name, user_id):
        min_confidence = request.args.get("min_confidence", default = 0, type = float)
        max_confidence = request.args.get("max_confidence", default = 1, type = float)
        page_number = request.args.get("page_number", default = 1, type = int)
        page_size = request.args.get("page_size", default = 20, type = int)
        users_inputs = []
        for user_input in AgentsService.get_instance().getUserInputs(agent_name, user_id, max_confidence, min_confidence, page_number, page_size):
                users_inputs.append(user_input)
        return jsonify(users_inputs)
