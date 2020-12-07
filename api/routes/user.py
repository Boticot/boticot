from utils import response_template
from datetime import timedelta
from flask import request, jsonify
import json, os
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask import current_app
from user_service import UserService

@current_app.route("/register", methods=["POST"])
def register():
    request_data = json.loads((request.get_data()).decode())
    email = request_data.get("email")
    user = UserService.get_instance().find_user(email)
    if user:
        return response_template(409, "User Already Exist")
    else:
        first_name = request_data.get("first_name")
        last_name = request_data.get("last_name")
        password = request_data.get("password")
        UserService.get_instance().add_new_user(email, first_name, last_name, password)
        return response_template(201, "User added sucessfully")

@current_app.route("/login", methods=["POST"])
def login():
    request_data = json.loads((request.get_data()).decode())
    email = request_data.get("email")
    password = request_data.get("password")
    if email is None or password is None:
        return response_template(401, "Missing Email or Password")
    check_user = UserService.get_instance().check_user(email, password)
    if check_user:
        expires = timedelta(minutes=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 240)))
        access_token = create_access_token(identity=email, expires_delta=expires)
        return jsonify(access_token=access_token), 201
    else:
        return response_template(401, "Wrong Email or Password")

@current_app.route("/nlu/agents/<agent_name>/users/<user_id>", methods=["GET"])
def get_user_inputs(agent_name, user_id):
        min_confidence = request.args.get("minConfidence", default = 0, type = float)
        max_confidence = request.args.get("maxConfidence", default = 1, type = float)
        page_number = request.args.get("pageNumber", default = 1, type = int)
        page_size = request.args.get("pageSize", default = 20, type = int)
        users_inputs = []
        for user_input in AgentsService.get_instance().getUserInputs(agent_name, user_id, max_confidence, min_confidence, page_number, page_size):
                users_inputs.append(user_input)
        return jsonify(users_inputs)