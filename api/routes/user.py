from utils import response_template
from datetime import timedelta
from flask import request, jsonify
import json, os
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask import current_app
from users_service import UsersService

@current_app.route("/login", methods=["POST"])
def login():
    request_data = json.loads((request.get_data()).decode())
    email = request_data.get("email")
    password = request_data.get("password")
    if email is None or password is None:
        return response_template(401, "Missing Email or Password")
    user = UsersService.get_instance().check_user(email, password)
    if user:
        expires = timedelta(minutes=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 240)))
        access_token = create_access_token(identity=email, expires_delta=expires)
        return jsonify(access_token=access_token), 201
    else:
        return response_template(401, "Wrong Email or Password")

@current_app.route("/users/register", methods=["POST"])
@jwt_required
def register():
    if (not UsersService.get_instance().is_user_super_admin(get_jwt_identity())):
        return response_template(401, "Unauthorized to add user") 
    else:
        request_data = json.loads((request.get_data()).decode())
        email = request_data.get("email")
        user = UsersService.get_instance().find_user(email)
        if user:
            return response_template(409, "User Already Exist")
        else:
            first_name = request_data.get("first_name")
            last_name = request_data.get("last_name")
            password = request_data.get("password")
            role = request_data.get("role")
            agents = request_data.get("agents")
            if first_name and last_name and password and role and agents is not None:
                UsersService.get_instance().add_new_user(email, first_name, last_name, password, role, agents)
                return response_template(201, "User added successfully")
            else:
                return response_template(401, "Missing one or more mandatory fields")

@current_app.route("/users", methods=["GET"])
@jwt_required
def get_users():
    if (not UsersService.get_instance().is_user_super_admin(get_jwt_identity())):
        return response_template(401, "Unauthorized to get users")
    else:
        users = UsersService.get_instance().get_all_users()
        return jsonify(users)

@current_app.route("/users/<email>", methods=["GET"])
@jwt_required
def get_user_information(email):
    if get_jwt_identity() == email:
        user = UsersService.get_instance().get_user_information(email)
        return jsonify(user)
    else:
        return response_template(401, "Authorization token should be associated to user email")

@current_app.route("/users/<email>", methods=["PUT"])
@jwt_required
def update_user(email):
    if (get_jwt_identity() != email and not UsersService.get_instance().is_user_super_admin(get_jwt_identity())):
        return response_template(401, "Unauthorized to update user")
    else:
        request_data = json.loads((request.get_data()).decode())
        first_name = request_data.get("first_name")
        last_name = request_data.get("last_name")
        role = request_data.get("role")
        agents = request_data.get("agents")
        if first_name and last_name and role and agents is not None:
            UsersService.get_instance().update_user_information(email, first_name, last_name, role, agents)
            return response_template(201, "User updated successfully")
        else:
            return response_template(401, "Missing one or more mandatory fields")

@current_app.route("/users/<email>", methods=["DELETE"])
@jwt_required
def delete_user(email):
    if (not UsersService.get_instance().is_user_super_admin(get_jwt_identity())):
        return response_template(401, "Unauthorized to delete user") 
    else:
        UsersService.get_instance().delete_user(email)
        return response_template(200, "User {0} successfully deleted".format(email))

@current_app.route("/users/<email>/reset-password", methods=["POST"])
@jwt_required
def reset_password(email):
    if get_jwt_identity() == email:
        request_data = json.loads((request.get_data()).decode())
        new_password = request_data.get("new_password")
        if new_password is None:
            return response_template(401, "Missing new password field")
        UsersService.get_instance().reset_user_password(email, new_password)
        return response_template(200, "Password successfully reset for user {0}".format(email))
    else:
        return response_template(401, "Authorization token should be associated to user email")
