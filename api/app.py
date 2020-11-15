import os, threading
from flask import Flask
from utils import get_instance_folder_path
from configuration import configure_app
from loader_cron import init_loader_cron

import logging
logger = logging.getLogger(__name__)

app = Flask(__name__, instance_path=get_instance_folder_path(), instance_relative_config=True)
configure_app(app)

with app.app_context():
    from routes import *
    app.register_blueprint(routes)

def runApp(msg):
    """Run Main Application"""
    logger.info(msg)
    app.run(os.environ['SERVER_HOST'], port=int(os.environ["SERVER_PORT"]))

def runCron(msg):
    """Run Loader Cron"""
    logger.info(msg)
    if os.environ.get("ACTIVATE_LOADER_CRON", 0) == "1":
        logger.info("Loader CRON is activated")
        init_loader_cron(os.environ.get("LOADER_CRON_SCHEDULE", 10))
    else:
        logger.info("Loader CRON is deactivated")

CronThread = threading.Thread(target=runCron, args=("Boticot Loader Cron starting",))
CronThread.start()

if __name__ == "__main__":
    runApp("Boticot API starting.")