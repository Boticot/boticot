from .mongodb import mongo

class SynonymsRepository():
    
    def __init__(self):
        self.synonymsCollection = mongo.db.synonyms

    def find_agent_synonyms(self, agentName):
        return self.synonymsCollection.find({"agentName": agentName})
