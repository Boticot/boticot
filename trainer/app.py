import os, threading
from datetime import datetime, timedelta
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from utils import get_instance_folder_path
from configuration import configure_app
from training_cron import init_training_cron
from analytics_service import AnalyticsService

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

tomorrow = datetime.today() + timedelta(days = 1)
tomorrow_midnight = datetime.combine(tomorrow, datetime.min.time())
tomorrow_analytics = tomorrow_midnight + timedelta(hours= 2)

scheduler = BackgroundScheduler()
# Run each night at 2 AM
scheduler.add_job(id = 'Analytics job', func = AnalyticsService.get_instance().run_analytics_job, trigger = 'interval', next_run_time = tomorrow_analytics, days = 1)
scheduler.start()

if __name__ == "__main__":
    runApp("Boticot trainer starting.")
