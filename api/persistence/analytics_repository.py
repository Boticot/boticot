import logging
from .mongodb import mongo

logger = logging.getLogger(__name__)

class AnalyticsRepository():
    
    def __init__(self):
        self.analytics_repository = mongo.db.analytics

    def find_agent_analytics(self, agent_name, days_number, start_date, end_date):
        if start_date and end_date:
            return self.analytics_repository.find({"agent_name": agent_name, "date": {"$gte": start_date, "$lte": end_date}}).sort("date", -1).limit(days_number)
        elif start_date:
            return self.analytics_repository.find({"agent_name": agent_name, "date": {"$gte": start_date}}).sort("date", -1).limit(days_number)
        elif end_date:
            return self.analytics_repository.find({"agent_name": agent_name, "date": {"$lte": end_date}}).sort("date", -1).limit(days_number)
        else:
            return self.analytics_repository.find({"agent_name": agent_name}).sort("date", -1).limit(days_number)
