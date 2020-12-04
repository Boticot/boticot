import os, shutil
from flask import jsonify
import logging

logger = logging.getLogger(__name__)

def get_app_base_path():
    return os.path.dirname(os.path.realpath(__file__))

def get_instance_folder_path():
    return os.path.join(get_app_base_path(), "instance")

def response_template(code, message):
    response = jsonify({
            "message": message
    })
    response.status_code = code
    return response

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory, mode=0o777)
    except OSError:
        logger.error("Error when creating directory %s", (OSError))

def remove_file_or_dir(path):
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
    else:
        logger.warn("file {} is not a file or dir.".format(path))