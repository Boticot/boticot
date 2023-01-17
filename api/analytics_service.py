from persistence.analytics_repository import AnalyticsRepository
import logging

logger = logging.getLogger(__name__)

class AnalyticsService(object):

    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if AnalyticsService.__instance is None:
            AnalyticsService()
        return AnalyticsService.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if AnalyticsService.__instance is not None:
            raise Exception("AnalyticsService is a singleton!")
        else:
            self.analytics_repository = AnalyticsRepository()
            AnalyticsService.__instance = self

    def get_analytics(self, agent_name, days_number, start_date=None, end_date=None):
        analytics = self.analytics_repository.find_agent_analytics(agent_name, days_number, start_date, end_date)
        analytics_response = {
            "agent_name": agent_name,
            "analytics": []
        }
        for analytic in analytics:
            del analytic["_id"]
            del analytic["agent_name"]
            analytics_response.get("analytics").append(analytic)
        return analytics_response
