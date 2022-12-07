from .mongodb import mongo
from random import randint
from bson import ObjectId
import logging
import os

logger = logging.getLogger(__name__)

class ResponsesRepository():

    def __init__(self):
        self.responses_collection = mongo.db.responses

    def find_agent_responses(self, agent_name, intent=None):
        filter = {"agent_name": agent_name}
        if intent:
            filter["intent"] = intent
        return self.responses_collection.find(filter)

    def find_agent_responses_by_intent(self, agent_name, intent):
        return self.responses_collection.find({"agent_name": agent_name, "intent": intent})
    
    def find_agent_suggestions_by_intent(self, agent_name, intent):
        return self.responses_collection.find({"agent_name": agent_name, "intent": intent, "response_type": "SUGGESTION"})

    def insert_response(self, agent_name, response):
        response_data = {
            "agent_name": agent_name, 
            "intent": response["intent"], 
            "response_type": response["response_type"], 
            "data": response["data"]
            }
        return self.responses_collection.update(response_data, response_data, upsert = True)
    
    def insert_responses(self, data):
        """Add sequentially multiple responses based on bulk size"""
        bulk_insert_size = int(os.environ.get("BULK_INSERT_SIZE", 500))
        q = len(data) // bulk_insert_size
        r = len(data) % bulk_insert_size
        try:
            for i in range(q):
                self.responses_collection.insert_many(data[bulk_insert_size*i:bulk_insert_size*(i+1)])
            return(self.responses_collection.insert_many(data[bulk_insert_size*q:(bulk_insert_size * q + r)+1]))
        except Exception as e:
            logger.error("Can't insert data {0}".format(e), exc_info=True)
            return(False)  
    
    def update_response_by_id(self, agent_name, response, id):
        response_data = {
            "response_type": response["response_type"], 
            "data": response["data"]
            }
        return self.responses_collection.update({"_id": ObjectId(id)}, {"$set": response_data})

    def delete_all_agent_responses(self, agent_name):
        self.responses_collection.delete_many({"agent_name": agent_name})

    def delete_agent_responses_by_intent(self, agent_name, intent_name):
        self.responses_collection.delete_many({"agent_name": agent_name, "intent": intent_name})
    
    def update_agent_responses_intent(self, agent_name, intent_name, new_intent_name):
        self.responses_collection.update_many({"agent_name": agent_name, "intent": intent_name}, {"$set": {"intent": new_intent_name}})

    def update_agent_suggestion_responses_intent(self, agent_name, intent_name, new_intent_name):
        self.responses_collection.update_many({"agent_name": agent_name, "response_type": "SUGGESTION", "data.suggestion_intent": intent_name,}, {"$set": {"data.suggestion_intent": new_intent_name}})


    def delete_response_by_id(self, id):
        try:
            self.responses_collection.delete_one({"_id": ObjectId(id)})
            return True
        except:
            return False  
