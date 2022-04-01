from .mongodb import mongo
import logging

logger = logging.getLogger(__name__)

class UsersRepository():

    def __init__(self):
        self.users_collection = mongo.db.users

    def find_all_users(self):
        return self.users_collection.find({})

    def add_user(self, user):
        return(self.users_collection.insert_one(user))

    def get_user(self, email):
        return self.users_collection.find_one({"email": email})

    def get_users_by_agent_access(self, agent_name):
        return self.users_collection.find({"agents": agent_name})

    def get_one_user_by_role(self, role):
        return self.users_collection.find_one({"role": role})

    def update_user_password(self, email, new_password):
        return self.users_collection.update_one(
            {"email": email}, 
            {"$set": 
                {
                    "password": new_password, 
                    "is_first_login": False
                }
            }
        )
    
    def update_user_agent_access(self, email, agent_name):
        return self.users_collection.update_one(
            {"email": email}, 
            {"$addToSet": 
                { "agents": agent_name } 
            }
        )

    def delete_user_agent(self, email, agent_name):
        return self.users_collection.update_one(
            {"email": email}, 
            {"$pull": 
                { "agents": agent_name } 
            }
        )
    
    def update_user_data(self, email, first_name, last_name, role, agents):
        return self.users_collection.update_one(
            {"email": email}, 
            {"$set": 
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "role": role,
                    "agents": agents
                }
            }
        )

    def delete_user(self, email):
        self.users_collection.delete_one({"email": email})
