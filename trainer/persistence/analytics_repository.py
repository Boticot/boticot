import logging
from .mongodb import mongo

logger = logging.getLogger(__name__)

class AnalyticsRepository():
    
    def __init__(self):
        self.analytics_repository = mongo.db.analytics

    def insert_analytics(self, data):
        return self.analytics_repository.insert_one(data)

    def find_agent_analytics_by_date(self, agent_name, date):
        return self.analytics_repository.find_one({"agent_name": agent_name, "date": date})
