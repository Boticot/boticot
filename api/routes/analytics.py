import os
from flask import request, jsonify
from flask_jwt_extended import jwt_required
import sys
sys.path.append("..")
from analytics_service import AnalyticsService
from flask import current_app
from utils import string_to_date
from utils import response_template
import logging

logger = logging.getLogger(__name__)

@current_app.route("/analytics/<agent_name>", methods=["GET"])
@jwt_required
def get_all_analytics(agent_name):
    days_number = request.args.get("days_number", default=60, type=int)
    start_date = request.args.get("start_date", default=None, type=str)
    end_date = request.args.get("end_date", default=None, type=str)
    start_datetime = None
    end_datetime = None
    if start_date or end_date:
        if start_date:
            start_datetime = string_to_date(start_date)
            if start_datetime is None:
                return response_template(400, "Not valid start date parameter, should be with DD-MM-YYYY format")
        if end_date:
            end_datetime = string_to_date(end_date)
            if not end_datetime:
                return response_template(400, "Not valid end date parameter, should be with DD-MM-YYYY format")
        analytics = AnalyticsService.get_instance().get_analytics(agent_name, days_number, start_datetime, end_datetime)
    else:
        analytics = AnalyticsService.get_instance().get_analytics(agent_name, days_number)
    return jsonify(analytics)
