from .mongodb import mongo

class LookupsRepository():
    
    def __init__(self):
        self.lookupCollection = mongo.db.lookup

    def find_agent_lookups(self, agentName):
        return self.lookupCollection.find({"agent_name": agentName})
