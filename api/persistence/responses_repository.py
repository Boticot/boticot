from .mongodb import mongo
from random import randint

class ResponsesRepository():

    def __init__(self):
        self.responses_collection = mongo.db.responses

    def find_agent_responses(self, agent_name):
        return self.responses_collection.find({"agentName": agent_name})

    def insert_response(self, data):
        return self.responses_collection.update(
            {"agentName": data["agentName"], "key": "INTENT_" + data["intent"], "fulfillment_text": data["fulfillment_text"]},
            {"agentName": data["agentName"], "key": "INTENT_" + data["intent"], "fulfillment_text": data["fulfillment_text"]},
            upsert = True)
        
    def get_response_intent(self, agent_name, intent):
        N = self.responses_collection.count({"agentName": agent_name,"key": "INTENT_" + intent, "fulfillment_text": {"$exists": True}})
        if N == 0:
            return [{"fulfillment_text":""}]
        else :
            R = randint(0, N - 1)
            return self.responses_collection.find({"agentName": agent_name,"key": "INTENT_" + intent, "fulfillment_text": {"$exists": True}}, {"_id": 0, "fulfillment_text": 1}).limit(1).skip(R)

    def delete_responses(self, agent_name):
        self.responses_collection.delete_many({"agentName": agent_name})
