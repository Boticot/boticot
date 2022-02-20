import os
from .mongodb import mongo
import logging

logger = logging.getLogger(__name__)
class LookupsRepository():
    
    def __init__(self):
        self.lookup_collection = mongo.db.lookup

    def find_agent_lookups(self, agent_name):
        return self.lookup_collection.find({"agent_name": agent_name})

    def find_lookup(self, agent_name, lookup_name):
        return self.lookup_collection.find({"agent_name": agent_name, "lookups.name": lookup_name})

    def insert_lookups(self, data):
        try:
            self.lookup_collection.insert_many(data)
            return True
        except Exception as e:
            logger.error("Exception when insert lookups {0}".format(e), exc_info=True)
            return False  
    
    def delete_agent_lookups(self, agent_name):
        self.lookup_collection.delete_many({"agent_name": agent_name})

    def delete_lookup(self, agent_name, lookup_name):
        try:
            self.lookup_collection.delete_many({"agent_name": agent_name, "lookups.name": lookup_name})
            return True
        except:
            return False

    def count_agent_lookups(self, agent_name):
        return self.lookup_collection.count({"agent_name": agent_name})

    def get_agent_lookups(self, agent_name):
        return self.lookup_collection.find({"agent_name": agent_name}, {"agent_name": 0})
