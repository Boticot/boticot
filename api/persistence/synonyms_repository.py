from .mongodb import mongo
from bson import ObjectId

class SynonymsRepository():
    
    def __init__(self):
        self.synonyms_collection = mongo.db.synonyms

    def find_synonym(self, id):
        return self.synonyms_collection.find_one({"_id": ObjectId(id)})

    def find_agent_synonyms(self, agent_name):
        return self.synonyms_collection.find({"agent_name": agent_name})

    def insert_synonyms(self, data):
        try:
            self.synonyms_collection.insert_many(data)
            return True
        except:
            return False 

    def delete_agent_synonyms(self, agent_name):
        self.synonyms_collection.delete_many({"agent_name": agent_name})

    def delete_synonym(self, agent_name, id):
        try:
            self.synonyms_collection.delete_one({"agent_name": agent_name, "_id": ObjectId(id)})
            return True
        except:
            return False

    def update_synonym(self, agent_name, id, data):
        try:
            self.synonyms_collection.update_one({"agent_name": agent_name, "_id": ObjectId(id)}, {"$set": {"data": data}}, upsert = True)
            return True
        except:
            return False
