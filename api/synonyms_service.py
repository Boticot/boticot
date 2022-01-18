import json
from bson import ObjectId
from persistence.agents_repository import AgentsRepository
from persistence.synonyms_repository import SynonymsRepository
from persistence.mongo_encoder import MongoJSONEncoder
import logging

logger = logging.getLogger(__name__)

class SynonymsService(object):
    
    __instance = None

    @staticmethod 
    def get_instance():
      """ Static access method. """
      if SynonymsService.__instance is None:
         SynonymsService()
      return SynonymsService.__instance

    def __init__(self):
      """ Virtually private constructor. """
      if SynonymsService.__instance is not None:
         raise Exception("SynonymsService is a singleton!")
      else:
         self.synonyms_repository = SynonymsRepository()
         self.agents_repository = AgentsRepository()
         SynonymsService.__instance = self

    def get_agent_synonyms(self, agent_name):
        tmp_data = []
        synonyms = self.synonyms_repository.find_agent_synonyms(agent_name)
        for entry in synonyms:    
            del entry["_id"]
            tmp_data.append(entry["synonyms"])
        return tmp_data

    def get_synonyms(self, agent_name):
        db_synonyms = self.synonyms_repository.find_agent_synonyms(agent_name)
        synonyms = []
        for entry in db_synonyms:  
            del entry["agent_name"]
            synonyms.append(json.loads(MongoJSONEncoder().encode(entry)))
        count_synonyms = self.synonyms_repository.count_agent_synonyms(agent_name)
        return { 
            "count" : count_synonyms,
            "items": synonyms
            }

    def add_agent_synonyms(self, agent_name, synonyms):
        data = []
        for entry in synonyms:
            data.append({"agent_name": agent_name, "synonyms": entry})
        if self.synonyms_repository.insert_synonyms(data):
            self.agents_repository.agent_modified(agent_name)

    def synonym_exist(self, id):
        if not ObjectId.is_valid(id) or self.synonyms_repository.find_synonym(id) is None:
            return False
        else:
            return True

    def delete_agent_synonym(self, agent_name, id):
        if self.synonyms_repository.delete_synonym(agent_name, id):
            self.agents_repository.agent_modified(agent_name)

    def update_agent_synonym(self, agent_name, id, synonym):
        if self.synonyms_repository.update_synonym(agent_name, id, synonym):
            self.agents_repository.agent_modified(agent_name)