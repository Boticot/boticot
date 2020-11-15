import os
from typing import Optional, Text
from utils import createFolder
import logging

logger = logging.getLogger(__name__)

def get_loader(name: Text) -> Optional["ModelsLoader"]:
    """Returns an instance of the requested ModelRecorder. Currently, `mongodb`is supported"""

    if name == "mongodb":
        return MongodbLoader()

    return None


class ModelsLoader:

    def remove_all(self, agent_name: Text) -> None:
        models = self._list_models(agent_name)
        for model in models:
            self._remove_version(model)

    def retrieve(self, agent_name: Text, model_name: Text) -> Text:
        """Downloads a model that has been persisted"""
        download_dir = os.environ.get("MODELS_PATH") + agent_name + "/"
        if not os.path.exists(download_dir):
            createFolder(download_dir)
        download_path = download_dir + model_name + ".tar.gz"
        if os.path.exists(download_path):
            logger.info("Already existing model: {0} for agent {1}".format(model_name, agent_name))
        else:
            logger.info("Start retrieve model: {0} for agent {1}".format(model_name, agent_name))
            agent_prefix = "_"+agent_name+"_"
            file_name = agent_prefix + model_name
            self._retrieve_tar(file_name, download_path)
            logger.info("End retrieve model: {0} for agent {1}".format(model_name, agent_name))
        return download_path
    
    def _retrieve_tar(self, file_name: Text, tar_path: Text) -> None:
        raise NotImplementedError("")

    def _list_models(self, agent_name: Text):
        raise NotImplementedError("")
    
    def _remove_version(self, model_version: Text) -> None:
        raise NotImplementedError("")


class MongodbLoader(ModelsLoader):
    """Load models on Mongodb using gridfs"""

    def __init__(self) -> None:
        from pymongo import MongoClient
        import gridfs

        super().__init__()
        self.db = MongoClient(os.environ.get("MONGO_CONNECTION_STRING")).get_default_database()
        self.fs = gridfs.GridFS(self.db)

    def _retrieve_tar(self, file_name: Text, tar_path: Text) -> None:
        f = self.fs.find_one({"filename": file_name})
        fi = open(tar_path, "wb+")
        fi.write(f.read())
        fi.close()

    def _list_models(self, agent_name: Text):
        from persistence.mongodb import mongo
        agent_prefix = "_"+agent_name+"_"
        models = mongo.db.fs.files.find({"filename": { "$regex": "^{}".format(agent_prefix)}}).sort("filename", -1)
        model_names = []
        for model in models:
            model_names.append(model.get("filename"))
        return model_names

    def _remove_version(self, model_version: Text) -> None:
        from persistence.mongodb import mongo
        from persistence.mongo_encoder import MongoJSONEncoder
        from bson import ObjectId
        import json
        r1 = mongo.db.fs.files.find_one({"filename" : model_version})
        if r1 is not None:
            result = json.loads(MongoJSONEncoder().encode(r1))
            id_to_delete = result.get("_id")
            mongo.db.fs.files.delete_many({"filename" : model_version})
            mongo.db.fs.chunks.delete_many({"files_id" : ObjectId(id_to_delete)})