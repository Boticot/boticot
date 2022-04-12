from datetime import datetime, timedelta
from utils import create_file, remove_file_or_dir
from persistence.agents_repository import AgentsRepository
from persistence.users_inputs_repository import UsersInputRepository
from persistence.analytics_repository import AnalyticsRepository
import logging

logger = logging.getLogger(__name__)

class AnalyticsService(object):

    __instance = None

    @staticmethod 
    def get_instance():
      """Static access method."""
      if AnalyticsService.__instance == None:
         AnalyticsService()
      return AnalyticsService.__instance
    def __init__(self):
      """Virtually private constructor."""
      if AnalyticsService.__instance != None:
         raise Exception("AnalyticsService is a singleton!")
      else:
         self.agents_repository = AgentsRepository()
         self.users_inputs_repository = UsersInputRepository()
         self.analytics_repository = AnalyticsRepository()
         AnalyticsService.__instance = self

    def run_analytics_job(self):
        """Run Analytics Job"""
        agents = self.agents_repository.get_all_agents_with_intents()
        for agent in agents:    
            self.store_agent_last_day_analytics(agent.get("name"), agent.get("intents"))
    
    def exist_agent_analytics(self, agent_name, date):
        if self.analytics_repository.find_agent_analytics_by_date(agent_name, date):
            return True
        else:
            return False

    def store_agent_last_day_analytics(self, agent_name, intents):
        today = datetime.today()
        yesterday = today - timedelta(days = 1)
        self.store_agent_analytics(agent_name, intents, yesterday)
        

    def store_agent_analytics(self, agent_name, intents, date):
        date_midnight = datetime.combine(date, datetime.min.time())
        if self.exist_agent_analytics(agent_name, date_midnight):
            logger.debug("Already existing analytics for agent {0} and date {1}".format(agent_name, date_midnight))
        else:
            one_day_after_date_midnight = date_midnight + timedelta(days = 1)
            unique_users = self.users_inputs_repository.get_agent_unique_users_count(agent_name, date_midnight, one_day_after_date_midnight)
            unique_users_count = len(unique_users)
            agent_traffic = self.users_inputs_repository.get_agent_traffic(agent_name, date_midnight, one_day_after_date_midnight)
            intents_count = []
            entities_count = []
            if intents:
                for intent in intents:
                    intent_count = self.users_inputs_repository.get_agent_intent_count(agent_name, intent, date_midnight, one_day_after_date_midnight)
                    intents_count.append({
                        "intent" : intent,
                        "count": intent_count
                    })
            entities = self.users_inputs_repository.get_agent_entities_count(agent_name, date_midnight, one_day_after_date_midnight)
            if entities is not None:
                for entity in entities:
                    entities_count.append({
                        "entity": entity["_id"],
                        "count": entity["count"]
                    })
            agent_analytics = {
                "agent_name": agent_name,
                "date": date_midnight,
                "traffic": agent_traffic,
                "unique_users": unique_users_count,
                "intents_count": intents_count,
                "entities_count": entities_count
            }
            logger.debug("Insert analytics for agent {0} and date {1}".format(agent_name, date_midnight))
            self.analytics_repository.insert_analytics(agent_analytics)
