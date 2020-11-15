import os
from .mongodb import mongo

class UsersRepository():

    def __init__(self):
        self.users_inputs_collection = mongo.db.usersInputs
        self.users_collection = mongo.db.users

    def insert_user_input(self, data):
        return(self.users_inputs_collection.insert_one(data))
    
    def count_user_inputs(self, agent_name):
        return self.users_inputs_collection.count({"agentName": agent_name})

    def get_agent_inputs(self, agent_name, max_confidence, min_confidence, page_number, page_size):
        if page_size > int(os.environ.get("MAX_PAGE_SIZE")):
            page_size = int(os.environ.get("MAX_PAGE_SIZE"))
        return(self.users_inputs_collection.find({"agentName": agent_name, "intent.confidence": {"$lte": max_confidence, "$gte": min_confidence}}, {"agentName": 0}).sort("timestamp", -1).skip((page_number - 1) * page_size).limit(page_size))

    def get_user_inputs(self, agent_name, user_id, max_confidence, min_confidence, page_number, page_size):
        if page_size > int(os.environ.get("MAX_PAGE_SIZE")):
            page_size = int(os.environ.get("MAX_PAGE_SIZE"))
        return(self.users_inputs_collection.find({"agentName": agent_name, "user_id": user_id, "intent.confidence": {"$lt": max_confidence, "$gt": min_confidence}}, {"agentName": 0}).skip((page_number - 1) * page_size).limit(page_size))

    def add_user(self, user):
        return(self.users_collection.insert_one(user))

    def get_user(self, email):
        return self.users_collection.find_one({"email": email})

    def get_one_user(self):
        return self.users_collection.find_one({})