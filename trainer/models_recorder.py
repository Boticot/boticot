import logging
import os
from typing import Optional, Text


logger = logging.getLogger(__name__)


def get_recorder(name: Text) -> Optional["ModelsRecorder"]:
    """Returns an instance of the requested ModelRecorder. Currently, `mongodb`is supported"""

    if name == "mongodb":
        return MongodbRecorder()

    return None


class ModelsRecorder:

    def remove(self, agent_name: Text, model_name: Text) -> None:
        self._remove_version("_"+agent_name+"_"+model_name)

    def save(self, agent_name: Text, model_directory: Text, model_name: Text, model_version: Text) -> None:
        if not os.path.isdir(model_directory):
            raise ValueError("Directory {0} not found".format(model_directory))
        tar_path = model_directory + model_name
        agent_prefix = "_"+agent_name+"_"
        self._save_tar(agent_prefix+model_version, tar_path)
        models = self._list_models(agent_name)
        model_persist_number = int(os.environ.get("MODEL_PERSIST_NUMBER"))
        if len(models) > model_persist_number:
            models_to_delete = models[model_persist_number:]
            for model in models_to_delete:
                self._remove_version(model)

    def list_versions(self, agent_name: Text):
        models = self._list_models(agent_name)
        versions = []
        for model in models:
            version = model[len(agent_name)+2:]
            versions.append(version)
        return versions

    def _save_tar(self, filekey: Text, tarname: Text) -> None:
        raise NotImplementedError("")

    def _list_models(self, agent_name: Text):
        raise NotImplementedError("")
    
    def _remove_version(self, model_version: Text) -> None:
        raise NotImplementedError("")


class MongodbRecorder(ModelsRecorder):
    """Store models on Mongodb using gridfs, Fetches them when needed."""

    def __init__(self) -> None:
        super().__init__()

    def _save_tar(self, file_key: Text, tar_path: Text) -> None:
        from persistence.mongodb import mongo
        import gridfs
        with open(tar_path, "rb+") as f:
            mongo.save_file(file_key, f)

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
        from persistence    .mongo_encoder import MongoJSONEncoder
        from bson import ObjectId
        import json
        r1 = mongo.db.fs.files.find_one({"filename" : model_version})
        if r1 is not None:
            result = json.loads(MongoJSONEncoder().encode(r1))
            id_to_delete = result.get("_id")
            mongo.db.fs.files.delete_many({"filename" : model_version})
            mongo.db.fs.chunks.delete_many({"files_id" : ObjectId(id_to_delete)})