from .mongodb import mongo
from random import randint
from bson import ObjectId

class ResponsesRepository():

    def __init__(self):
        self.responses_collection = mongo.db.responses

    def find_agent_responses(self, agent_name):
        return self.responses_collection.find({"agent_name": agent_name})

    def find_agent_responses_by_intent(self, agent_name, intent):
        return self.responses_collection.find({"agent_name": agent_name, "key": "INTENT_" + intent})

    def insert_response(self, agent_name, data):
        return self.responses_collection.update(
            {"agent_name": agent_name, "key": "INTENT_" + data["intent"], "fulfillment_text": data["fulfillment_text"]},
            {"agent_name": agent_name, "key": "INTENT_" + data["intent"], "fulfillment_text": data["fulfillment_text"]},
            upsert = True)
        
    def get_response_intent(self, agent_name, intent):
        N = self.responses_collection.count({"agent_name": agent_name,"key": "INTENT_" + intent, "fulfillment_text": {"$exists": True}})
        if N == 0:
            return [{"fulfillment_text":""}]
        else :
            R = randint(0, N - 1)
            return self.responses_collection.find({"agent_name": agent_name,"key": "INTENT_" + intent, "fulfillment_text": {"$exists": True}}, {"_id": 0, "fulfillment_text": 1}).limit(1).skip(R)

    def delete_all_agent_responses(self, agent_name):
        self.responses_collection.delete_many({"agent_name": agent_name})

    def delete_response_by_id(self, id):
        try:
            self.responses_collection.delete_one({"_id": ObjectId(id)})
            return True
        except:
            return False  
