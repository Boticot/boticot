import logging
from .mongodb import mongo

logger = logging.getLogger(__name__)

class AgentsRepository():
    
    def __init__(self):
        self.agentsCollection = mongo.db.agents
        
    def update_trained_agent(self, agentName, agent, versions, timestamp):
        try:
            return self.agentsCollection.update({"name": agentName}, {"$set": {"lastVersion" : agent.model_version, "versions": versions, "lastTrain" : timestamp, "intents" : agent.intents, "entities" : agent.entities}}, upsert = True)
        except Exception as e:
            logger.error("Agent {0} Not updated in database with Exception {1}".format(agentName, e))

    def get_agent_config(self, agentName):
        return self.agentsCollection.find_one({"name": agentName}, {"_id" : 0, "config": 1})
    
    def get_all_modified_agents(self):
        return self.agentsCollection.find({"$expr":{"$gt":["$lastModified", "$lastTrain"]}}, {"_id": 0, "name": 1} )