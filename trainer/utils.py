import os, shutil
from os import listdir
from os.path import isfile, join
import json
import logging

logger = logging.getLogger(__name__)

def get_app_base_path():
    return os.path.dirname(os.path.realpath(__file__))

def get_instance_folder_path():
    return os.path.join(get_app_base_path(), "instance")

def create_file(filePath, content):
    try:
        f = open(filePath,"w+")
        f.write(content)
        f.close()
        logger.info("Create " + filePath)
    except OSError:
        logger.error("Error: Creating file %s", (OSError))

def remove_file_or_dir(path):
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
    else:
        logger.warn("file {} is not a file or dir.".format(path))