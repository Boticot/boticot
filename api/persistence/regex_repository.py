import os
from .mongodb import mongo
from bson import ObjectId


class RegexRepository:

    def __init__(self):
        self.regex_collection = mongo.db.regex

    def find_regex(self, id):
        return self.regex_collection.find_one({"_id": ObjectId(id)})

    def find_agent_regex(self, agent_name):
        return self.regex_collection.find({"agent_name": agent_name})

    def insert_regex(self, data):
        try:
            self.regex_collection.insert_many(data)
            return True
        except:
            return False

    def delete_agent_regex(self, agent_name):
        self.regex_collection.delete_many({"agent_name": agent_name})

    def delete_regex(self, agent_name, id):
        try:
            self.regex_collection.delete_one({"agent_name": agent_name, "_id": ObjectId(id)})
            return True
        except:
            return False

    def update_regex(self, agent_name, id, data):
        try:
            self.regex_collection.update_one({"agent_name": agent_name, "_id": ObjectId(id)}, {"$set": {"regex": data}}, upsert = True)
            return True
        except:
            return False

    def count_agent_regex(self, agent_name):
        return self.regex_collection.count({"agent_name": agent_name})

    def get_agent_regex(self, agent_name):
        return self.regex_collection.find({"agent_name": agent_name}, {"agent_name": 0})
