import os, time
from datetime import datetime
from agents_service import AgentsService
import logging
from persistence.mongodb import mongo
from flask import current_app

logger = logging.getLogger(__name__)

class TrainingCron:

    def __enter__(self):
        all_agents = AgentsService.get_instance().get_all_agents()
        trained_agents = []
        for agent in all_agents:
            bot = agent.get("name")
            try :
                if (agent.get("last_modified") > agent.get("last_train")):
                    logger.info("Start training Agent: {0}".format(bot))
                    AgentsService.get_instance().train_agent(bot)
                    trained_agents.append(bot)
            except Exception as e:
                logger.error("Exception when training agent {0}. {1}".format(bot, e), exc_info=True)
        logger.info("Trained Agents: {0}".format(trained_agents))


    def __exit__(self, type, value, traceback):
        logger.debug("Training Cron run at %s" % datetime.now())

def init_training_cron(minutes):
    """Init training Cron with schedule time"""
    while True:
        with TrainingCron():
            time.sleep(int(minutes)*60)

