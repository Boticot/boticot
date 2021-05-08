import logging
from .mongodb import mongo

logger = logging.getLogger(__name__)

class AgentsRepository():
    
    def __init__(self):
        self.agents_collection = mongo.db.agents

    def get_all_agents(self):
        return self.agents_collection.find({}, {"_id": 0, "name": 1, "last_modified":1, "last_train":1})
        
    def update_trained_agent(self, agentName, agent, versions, timestamp):
        try:
            return self.agents_collection.update({"name": agentName}, {"$set": {"last_version" : agent.model_version, "versions": versions, "last_train" : timestamp, "trained_intents" : agent.intents, "entities" : agent.entities}}, upsert = True)
        except Exception as e:
            logger.error("Agent {0} Not updated in database with Exception {1}".format(agentName, e))

    def get_agent_config(self, agentName):
        return self.agents_collection.find_one({"name": agentName}, {"_id" : 0, "config": 1})