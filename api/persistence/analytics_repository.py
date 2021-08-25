import logging
from .mongodb import mongo

logger = logging.getLogger(__name__)

class AnalyticsRepository():
    
    def __init__(self):
        self.analytics_repository = mongo.db.analytics

    def find_agent_analytics(self, agent_name, days_number):
        return self.analytics_repository.find({"agent_name": agent_name}).sort("date", -1).limit(days_number)
