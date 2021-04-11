import json
from datetime import datetime
from persistence.contexts_repository import ContextsRepository
from persistence.mongo_encoder import MongoJSONEncoder

class ContextService(object):

    __instance = None

    @staticmethod 
    def get_instance():
      """ Static access method. """
      if ContextService.__instance is None:
         ContextService()
      return ContextService.__instance
      
    def __init__(self):
      """ Virtually private constructor. """
      if ContextService.__instance is not None:
         raise Exception("ContextService is a singleton")
      else:
         self.contexts_repository = ContextsRepository()
         ContextService.__instance = self

    def insert_user_context(self, agent_name, user_id, context_name, context_value):
        self.contexts_repository.insert_context({"agent_name": agent_name, "user_id": user_id, "context_name": context_name, "context_value": context_value, "date": datetime.utcnow()})

    def remove_user_context(self, agent_name, user_id, context_name):
        self.contexts_repository.remove_context(agent_name, user_id, context_name)

    def remove_all_user_context(self, agent_name, user_id):
        self.contexts_repository.remove_all_contexts(agent_name, user_id)

    def get_user_context(self, agent_name, user_id):
        db_contexts = self.contexts_repository.get_contexts(agent_name, user_id)
        context = []
        for entry in db_contexts:
            context.append(json.loads(MongoJSONEncoder().encode(entry)))
        return { 
            "context" : context
            }
    
    def get_user_context_key_value(self, agent_name, user_id):
        db_contexts = self.contexts_repository.get_contexts(agent_name, user_id)
        context = []
        for entry in db_contexts:
            data = json.loads(MongoJSONEncoder().encode(entry))
            context.append(
                {
                    "context_name": data.get("context_name"),
                    "context_value": data.get("context_value")
                }
            )
        return { 
            "context" : context
            }
