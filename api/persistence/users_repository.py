import os
from .mongodb import mongo

class UsersRepository():

    def __init__(self):
        self.users_collection = mongo.db.users
        self.users_inputs_collection = mongo.db.usersInputs
        ttl_users_inputs = 30*60*60*24 # 30 days in seconds
        if os.environ.get("MONGODB_PROVIDER", "") == "CosmosDB":
            self.users_inputs_collection.ensure_index("_ts", expireAfterSeconds=ttl_users_inputs)
        else:
            self.users_inputs_collection.ensure_index("date", expireAfterSeconds=ttl_users_inputs)

    def insert_user_input(self, data):
        return(self.users_inputs_collection.insert_one(data))
    
    def count_user_inputs(self, agent_name):
        return self.users_inputs_collection.count({"agentName": agent_name})

    def get_agent_inputs(self, agent_name, max_confidence, min_confidence, page_number, page_size):
        max_page_size = int(os.environ.get("MAX_PAGE_SIZE", 200))
        if page_size > max_page_size:
            page_size = max_page_size
        return(self.users_inputs_collection.find({"agentName": agent_name, "intent.confidence": {"$lte": max_confidence, "$gte": min_confidence}}, {"agentName": 0}).sort("timestamp", -1).skip((page_number - 1) * page_size).limit(page_size))

    def delete_users_inputs(self, agent_name):
        self.users_inputs_collection.delete_many({"agentName": agent_name})

    def get_user_inputs(self, agent_name, user_id, max_confidence, min_confidence, page_number, page_size):
        max_page_size = int(os.environ.get("MAX_PAGE_SIZE", 200))
        if page_size > max_page_size:
            page_size = max_page_size
        return(self.users_inputs_collection.find({"agentName": agent_name, "user_id": user_id, "intent.confidence": {"$lt": max_confidence, "$gt": min_confidence}}, {"agentName": 0}).skip((page_number - 1) * page_size).limit(page_size))

    def add_user(self, user):
        return(self.users_collection.insert_one(user))

    def get_user(self, email):
        return self.users_collection.find_one({"email": email})

    def get_one_user(self):
        return self.users_collection.find_one({})