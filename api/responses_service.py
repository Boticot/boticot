import json
from random import randint
from persistence.responses_repository import ResponsesRepository
from persistence.agents_repository import AgentsRepository
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
         self.agents_repository = AgentsRepository()
         ResponsesService.__instance = self
    
    def get_agent_responses(self, agent_name, intent=None):
        tmp_data = []
        responses = self.responses_repository.find_agent_responses(agent_name, intent)
        for entry in responses: 
            tmp_data.append({
                    "intent": entry.get("intent"),
                    "response_type": entry.get("response_type"), 
                    "data": entry.get("data")
                })
        return tmp_data

    def get_agent_responses_by_intent(self, agent_name, intent):
        db_responses = self.responses_repository.find_agent_responses_by_intent(agent_name, intent)
        responses = {}
        text_responses = []
        suggestion_responses = []
        link_responses = []
        image_responses = []
        for entry in db_responses:    
            if (entry.get("response_type") == "TEXT"):
                db_text = json.loads(MongoJSONEncoder().encode(entry))
                text = db_text.get("data")
                text["_id"] = db_text.get("_id")
                text_responses.append(text)
            elif (entry.get("response_type") == "SUGGESTION"):
                db_suggestion = json.loads(MongoJSONEncoder().encode(entry))
                suggestion = db_suggestion.get("data")
                suggestion["_id"] = db_suggestion.get("_id")
                suggestion_responses.append(suggestion)
            elif (entry.get("response_type") == "LINK"):
                db_link = json.loads(MongoJSONEncoder().encode(entry))
                link = db_link.get("data")
                link["_id"] = db_link.get("_id")
                link_responses.append(link)
            elif (entry.get("response_type") == "IMAGE"):
                db_image = json.loads(MongoJSONEncoder().encode(entry))
                image = db_image.get("data")
                image["_id"] = db_image.get("_id")
                image_responses.append(image)
        responses["texts"] = text_responses
        responses["suggestions"] = suggestion_responses
        responses["links"] = link_responses
        responses["images"] = image_responses
        return responses

    def add_agent_responses(self, agent_name, responses):
        for response in responses: 
            data = response.get("data")
            if data.get("suggestion_intent"):
                self.agents_repository.update_agent_intents(agent_name, [response.get("intent"), data.get("suggestion_intent")])
            else:
                self.agents_repository.update_agent_intents(agent_name, [response.get("intent")])
            self.responses_repository.insert_response(agent_name, response)

    def get_response(self, agent_name, intent):
        response = {}
        responses = self.get_agent_responses_by_intent(agent_name, intent)
        if (len(responses.get("texts")) != 0):
            random_position = randint(0, len(responses.get("texts")) - 1)
            response["fulfillment_text"] = responses.get("texts")[random_position].get("fulfillment_text")
        if (len(responses.get("suggestions")) != 0):
            response["suggestions"] = responses.get("suggestions")
        if (len(responses.get("links")) != 0):
            response["links"] = responses.get("links")
        if (len(responses.get("images")) != 0):
            response["images"] = responses.get("images")
        return response
    
    def delete_response(self, id):
        self.responses_repository.delete_response_by_id(id)
