import os
from flask import request, jsonify
from flask_jwt_extended import jwt_required
import sys
sys.path.append("..")
from agents_service import AgentsService
from flask import current_app

@current_app.route("/analytics/<agent_name>", methods=["GET"])
@jwt_required
def get_all_analytics(agent_name):
    days_number = request.args.get("days_number", default = 30, type = int)
    analytics = AgentsService.get_instance().get_analytics(agent_name, days_number)
    return jsonify(analytics)
