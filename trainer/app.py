import os, threading
from flask import Flask
from utils import get_instance_folder_path
from configuration import configure_app
from training_cron import init_training_cron

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
    app.run(os.environ['SERVER_HOST'], port=int(os.environ.get("SERVER_PORT")), use_reloader=False)

def runCron(msg):
    """Run Training Cron"""
    logger.info(msg)
    init_training_cron(os.environ.get("TRAINING_CRON_SCHEDULE", 10))

CronThread = threading.Thread(target=runCron, args=("Boticot Training Cron starting",))
CronThread.start()

if __name__ == "__main__":
    runApp("Boticot trainer starting.")

