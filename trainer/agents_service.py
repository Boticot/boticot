import json
import os
from datetime import datetime
from itertools import groupby
from agent import Agent
from utils import create_file, remove_file_or_dir
from persistence.agents_repository import AgentsRepository
from persistence.training_data_repository import TrainingDataRepository
from persistence.lookups_repository import LookupsRepository
from persistence.synonyms_repository import SynonymsRepository
from models_recorder import get_recorder
import logging

logger = logging.getLogger(__name__)

class AgentsService(object):

    __instance = None

    @staticmethod 
    def get_instance():
      """Static access method."""
      if AgentsService.__instance == None:
         AgentsService()
      return AgentsService.__instance
    def __init__(self):
      """Virtually private constructor."""
      if AgentsService.__instance != None:
         raise Exception("AgentsService is a singleton!")
      else:
         self.agents_repository = AgentsRepository()
         self.training_data_repository = TrainingDataRepository()
         self.lookups_repository = LookupsRepository()
         self.synonyms_repository = SynonymsRepository()
         AgentsService.__instance = self

    def _get_agent_training_data(self, agent_name):
        tmp_data = []
        train_data = self.training_data_repository.find_agent_training_data(agent_name)
        for entry in train_data:    
            del entry["_id"]
            tmp_data.append(entry["data"])
        return tmp_data

    def _get_agent_lookups(self, agent_name):
        data = []
        lookups_db = self.lookups_repository.find_agent_lookups(agent_name)
        for entry in lookups_db:    
            del entry["_id"]
            data.append(entry["lookups"])
        lookups = []
        if len(data) > 0 :
            data.sort(key=lambda x: x["name"])
            groups = []
            for k, g in groupby(data, lambda x: x["name"]):
                groups.append(list(g))
            for entry in groups:
                lookup_entry = {}
                lookup_entry["name"] = entry[0].get("name")
                lookup_entry["elements"] = []
                for sub_entry in entry:
                    lookup_entry["elements"].extend(sub_entry.get("elements"))
                lookups.append(lookup_entry)
        return lookups

    def _get_agent_synonyms(self, agent_name):
        tmp_data = []
        synonyms = self.synonyms_repository.find_agent_synonyms(agent_name)
        for entry in synonyms:    
            del entry["_id"]
            tmp_data.append(entry["synonyms"])
        return tmp_data
    
    def get_all_agents(self):
        return list(self.agents_repository.get_all_agents())

    def _has_at_list_two_intents(self, training) -> bool:
        first_intent = training[0]["intent"]
        second_intent = next((item for item in training if item["intent"] != first_intent),None)
        return second_intent is None

    def train_agent(self, agent_name):
        try :
            train_data = {}
            train_data["rasa_nlu_data"] = {}
            training = self._get_agent_training_data(agent_name)
            train_data["rasa_nlu_data"]["common_examples"] = training
            if training in [[],None] :
                logger.warn("Agent {0} has no training data".format(agent_name))
                return("Could not found training data for Agent {0}".format(agent_name))
            if self._has_at_list_two_intents(training) : 
                logger.warn("Agent {0} has only one intent, while a minimum of two intents are needed".format(agent_name))
                return("Could not train Agent {0}, only found 1 intent".format(agent_name))
            else:
                try:
                    os.makedirs("./models/" + agent_name)
                except FileExistsError:
                    """directory already exists"""
                    pass
                train_data["rasa_nlu_data"]["lookup_tables"] = self._get_agent_lookups(agent_name)
                train_data["rasa_nlu_data"]["entity_synonyms"] = self._get_agent_synonyms(agent_name)
                config = self.agents_repository.get_agent_config(agent_name).get("config")
                training_data_file = os.environ.get("MODELS_PATH") + agent_name + ".json"
                config_file = os.environ.get("MODELS_PATH") +  agent_name + "_config.json"                
                create_file(training_data_file, json.dumps(train_data))
                create_file(config_file, json.dumps(config))
                agent = Agent(agentName = agent_name ,  botconfig = config_file ,data = training_data_file)
                model_recorder = get_recorder(os.environ.get("MODEL_RECORDER"))
                model_recorder.save(agent_name, agent.model_path, agent.model_name, agent.model_version)
                versions = model_recorder.list_versions(agent_name)
                now = int(datetime.timestamp(datetime.now()))
                self.agents_repository.update_trained_agent(agent_name, agent, versions, now)
                """Clean Up"""
                remove_file_or_dir(training_data_file)
                remove_file_or_dir(config_file)
                remove_file_or_dir(os.environ.get("MODELS_PATH") + agent_name)
                logger.info("Bot {0}, successfully trained, and model {1} persisted. ".format(agent_name, agent.model_name))
        except Exception as e :
            logger.error("Exception when training agent {0}. {1}".format(agent_name, e), exc_info=True)
