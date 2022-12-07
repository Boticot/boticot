
import os
from datetime import datetime
from .mongodb import mongo
import logging

logger = logging.getLogger(__name__)

class AgentsRepository():
    
    def __init__(self):
        self.agents_collection = mongo.db.agents

    def get_all_agents(self):
        return self.agents_collection.find()

    def find_agent(self, name):
        return self.agents_collection.find_one({"name": name})
    
    def delete_agent(self, name):
        return self.agents_collection.delete_one({"name": name})

    def insert_agent(self, data):
        return self.agents_collection.insert_one(data)

    def update_agent(self, agent_name, data):
        self.agents_collection.update_one({"name": agent_name}, {"$set": data })

    def agent_modified(self, agent_name):
        """update last modified field by the current timestamp"""
        last_modified = int(datetime.timestamp(datetime.now()))
        return self.agents_collection.update_one({"name": agent_name}, {"$set": {"last_modified" : last_modified}})

    def update_model(self, agent_name, model_name):
        """Specify model to load"""
        return(self.agents_collection.update({"name": agent_name}, {"$set": {"current_version": model_name}}, upsert= True))

    def get_versions(self, agent_name):
        return(self.agents_collection.find_one({"name" : agent_name}, {"_id": 0, "versions": 1}))

    def get_fallback(self, agent_name):
        return(self.agents_collection.find_one({"name" : agent_name}, {"_id": 0, "fallback": 1}))
    
    def get_agent_intents(self, agent_name):
        return self.agents_collection.find_one({"name": agent_name}, {"_id": 0, "intents": 1})

    def update_agent_intents(self, agent_name, intents):
        """Add/update agent intents"""
        return self.agents_collection.update_one(
            {"name": agent_name}, 
            { "$addToSet": { "intents": {"$each":intents} } }
        )

    def delete_agent_intent(self, agent_name, intent):
        return self.agents_collection.update_one(
            {"name": agent_name},
            { "$pull": { "intents": intent } }
        )
    
    def update_agent_intent(self, agent_name, intent_name, new_intent_name):
        self.agents_collection.update_one(
            {"name": agent_name},
            { "$pull": { "intents": intent_name } }
        )
        return self.agents_collection.update_one(
            {"name": agent_name}, 
            { "$addToSet": { "intents": new_intent_name } }
        )
    
    def update_agent_entities(self, agent_name, entities):
        """Add/update agent entities"""
        return self.agents_collection.update_one(
            {"name": agent_name}, 
            { "$addToSet": { "entities": {"$each":entities} } }
        )