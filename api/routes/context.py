from . import routes
from utils import response_template
from flask import request, jsonify
import sys
import json
sys.path.append('..')
from flask import current_app
from context_service import ContextService
from security_decorator import api_auth_required

@current_app.route('/context/agents/<agent_name>/users/<user_id>', methods=["PUT"])
@api_auth_required
def add_context(agent_name, user_id):
    if request.get_data():
        body = json.loads((request.get_data()).decode())
        ContextService.get_instance().insert_user_context(agent_name, user_id, body.get('context_name'), body.get('context_value'))
        return response_template(200, "Context successfully added for agent {0} and user_id {1}".format(agent_name, user_id))
    else:
        return response_template(400, "A body is mandatory inside the request")

@current_app.route('/context/agents/<agent_name>/users/<user_id>/contexts/<context_name>', methods=["DELETE"])
@api_auth_required
def remove_context(agent_name, user_id, context_name):
    ContextService.get_instance().remove_user_context(agent_name, user_id, context_name)
    return response_template(200, "Context '{0}' successfully deleted for agent {1} and user_id {2}".format(context_name, agent_name, user_id))

@current_app.route('/context/agents/<agent_name>/users/<user_id>', methods=["DELETE"])
@api_auth_required
def remove_all_contexts(agent_name, user_id):
    ContextService.get_instance().remove_all_user_context(agent_name, user_id)
    return response_template(200, "All Contexts are successfully deleted for agent {0} and user_id {1}".format(agent_name, user_id))

@current_app.route('/context/agents/<agent_name>/users/<user_id>', methods=["GET"])
@api_auth_required
def get_all_contexts(agent_name, user_id):
    contexts = ContextService.get_instance().get_user_context(agent_name, user_id)
    return jsonify(contexts)
