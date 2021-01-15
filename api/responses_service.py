import json
from persistence.responses_repository import ResponsesRepository
from persistence.mongo_encoder import MongoJSONEncoder
import logging

logger = logging.getLogger(__name__)

class ResponsesService(object):
    
    __instance = None

    @staticmethod 
    def get_instance():
      """ Static access method. """
      if ResponsesService.__instance is None:
         ResponsesService()
      return ResponsesService.__instance

    def __init__(self):
      """ Virtually private constructor. """
      if ResponsesService.__instance is not None:
         raise Exception("ResponsesService is a singleton!")
      else:
         self.responses_repository = ResponsesRepository()
         ResponsesService.__instance = self
    
    def get_agent_responses(self, agent_name):
        tmp_data = []
        responses = self.responses_repository.find_agent_responses(agent_name)
        for entry in responses:    
            del entry["_id"]
            del entry["agent_name"]
            intent = entry["key"].replace("INTENT_","")
            fulfillment_text = entry["fulfillment_text"]
            tmp_data.append({"intent": intent, "fulfillment_text": fulfillment_text})
        return tmp_data

    def get_agent_responses_by_intent(self, agent_name, intent):
        db_responses = self.responses_repository.find_agent_responses_by_intent(agent_name, intent)
        responses = []
        for entry in db_responses:    
            intent = entry["key"].replace("INTENT_","")
            del entry["key"]
            del entry["agent_name"]
            entry["intent"] = intent
            responses.append(json.loads(MongoJSONEncoder().encode(entry)))
        return responses

    def add_agent_responses(self, agent_name, responses):
        for response in responses: 
            self.responses_repository.insert_response(agent_name, response)

    def get_response(self, agent_name, intent):
        """Get agent responses for an intent"""
        try:
            response = self.responses_repository.get_response_intent(agent_name, intent)[0]["fulfillment_text"]
            return(response)
        except Exception as e:
            logger.warning("No response for agent {0} intent {1}, \n {2}".format(agent_name, intent, e))
            return("")
    
    def delete_response(self, id):
        self.responses_repository.delete_response_by_id(id)
