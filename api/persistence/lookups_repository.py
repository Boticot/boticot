from .mongodb import mongo
import logging

logger = logging.getLogger(__name__)
class LookupsRepository():
    
    def __init__(self):
        self.lookup_collection = mongo.db.lookup

    def find_agent_lookups(self, agentName):
        return self.lookup_collection.find({"agent_name": agentName})

    def insert_lookups(self, data):
        try:
            self.lookup_collection.insert_many(data)
            return True
        except Exception as e:
            logger.error("Exception when insert lookups {0}".format(e), exc_info=True)
            return False  
    
    def delete_lookups(self, agent_name):
        self.lookup_collection.delete_many({"agent_name": agent_name})
