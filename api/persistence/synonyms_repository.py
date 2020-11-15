from .mongodb import mongo

class SynonymsRepository():
    
    def __init__(self):
        self.synonyms_collection = mongo.db.synonyms

    def find_agent_synonyms(self, agent_name):
        return self.synonyms_collection.find({"agentName": agent_name})

    def insert_synonyms(self, data):
        try:
            self.synonyms_collection.insert_many(data)
            return True
        except:
            return False 
    
    def delete_synonyms(self, agent_name):
        self.synonyms_collection.delete_many({"agentName": agent_name})
