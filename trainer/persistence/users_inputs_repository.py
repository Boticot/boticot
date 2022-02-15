import logging
from .mongodb import mongo

logger = logging.getLogger(__name__)

class UsersInputRepository():
    
    def __init__(self):
        self.users_inputs_repository = mongo.db.usersInputs

    def get_agent_traffic(self, agent_name, from_date, to_date):
        return self.users_inputs_repository.count(
            {
                "agent_name" : agent_name,
                "date": 
                {
                    "$gte": from_date, 
                    "$lt": to_date
                }
            })

    def get_agent_intent_count(self, agent_name, intent, from_date, to_date):
        return self.users_inputs_repository.count(
            {
                "agent_name" : agent_name,
                "intent.name": intent,
                "date": 
                {
                    "$gte": from_date, 
                    "$lt": to_date
                }
            })

    def get_agent_entities_count(self, agent_name, from_date, to_date):
        return self.users_inputs_repository.aggregate(
                [{"$match": {"agent_name": agent_name,
                             "date": {"$gte": from_date,
                                      "$lt": to_date}}},
                 {"$unwind": {"path": "$entities"}},
                 {"$group": {"_id": "$entities.entity",
                             "count": {"$sum": 1}}}])

    def get_agent_unique_users_count(self, agent_name, from_date, to_date):
        return self.users_inputs_repository.distinct(
            "user_id", 
            {
                "agent_name" : agent_name, 
                "date": 
                {
                    "$gte": from_date, 
                    "$lt": to_date
                }
            })
