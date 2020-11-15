import logging

LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOGGING_LEVEL = logging.DEBUG

def configure_app(app):
    logging.basicConfig(format=LOGGING_FORMAT)
    log = logging.getLogger()
    log.setLevel(LOGGING_LEVEL)

