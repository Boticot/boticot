import os, time
from datetime import datetime
from agents_service import AgentsService
import logging
from persistence.mongodb import mongo
from flask import current_app

logger = logging.getLogger(__name__)

class TrainingCron:

    def __enter__(self):
        allModifiedAgents = AgentsService.get_instance().get_all_modified_agents()
        logger.info("Agents found for training: {0}".format(allModifiedAgents))
        for agent in allModifiedAgents:
            try :
                bot = agent.get("name")
                logger.info("Start train Agent: {0}".format(bot))
                AgentsService.get_instance().train_agent(bot)
            except Exception as e:
                logger.error("Exception when training agent {0}. {1}".format(bot, e), exc_info=True)


    def __exit__(self, type, value, traceback):
        logger.debug("Training Cron run at %s" % datetime.now())

def init_training_cron(minutes):
    """Init training Cron with schedule time"""
    while True:
        with TrainingCron():
            time.sleep(int(minutes)*60)

