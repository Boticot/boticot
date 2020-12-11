import time
from datetime import datetime
from agents_service import AgentsService
from utils import remove_file_or_dir
import logging

logger = logging.getLogger(__name__)

class LoaderSchedule:

    def __enter__(self):
        self.start = datetime.now()
        all_trained_agents = list(AgentsService.get_instance().get_trained_agents())
        logger.info("Agents found for Loading: {0}".format(all_trained_agents))
        for agent in all_trained_agents:
            try :
                logger.info("Start loading Agent: {0}".format(agent.get("name")))
                AgentsService.get_instance().load_agent(agent.get("name"), agent.get("last_version"))
            except Exception as e:
                logger.error("Exception when loading agent {0} with version {1} inside Cron Loader. {2}".format(agent.get("name"), agent.get("last_version"), e), exc_info=True)
                remove_file_or_dir(modelName)

    def __exit__(self, type, value, traceback):
        logger.debug("Loading Cron run at %s" % datetime.now())

def init_loader_cron(minutes):
    while True:
        with LoaderSchedule():
            time.sleep(int(minutes)*60)
