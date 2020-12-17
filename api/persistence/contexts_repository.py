import os
from bson import json_util
from .mongodb import mongo

class ContextsRepository():
    
    def __init__(self):
        self.context_collection = mongo.db.context
        ttl_context = 30*60 # 30 minutes in seconds
        if os.environ.get("MONGODB_PROVIDER", "") == "CosmosDB":
            self.context_collection.ensure_index("_ts", expireAfterSeconds=ttl_context) 
        else:
            self.context_collection.ensure_index("date", expireAfterSeconds=ttl_context) 
    
    def insert_context(self, data):
        return self.context_collection.insert_one(data)

    def remove_context(self, agent_name, user_id, context_name):
        return self.context_collection.delete_many({"agent_name": agent_name, "user_id": user_id, "context_name": context_name})

    def remove_all_contexts(self, agent_name, user_id):
        return self.context_collection.delete_many({"agent_name": agent_name, "user_id": user_id})

    def get_contexts(self, agent_name, user_id):
        return self.context_collection.find({"agent_name": agent_name, "user_id": user_id})

    def delete_contexts(self, agent_name):
        self.context_collection.delete_many({"agent_name": agent_name})
