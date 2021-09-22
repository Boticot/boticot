import json, os
from bson import ObjectId
from datetime import datetime
import numpy as np
from itertools import groupby
from agent import Agent
from utils import remove_file_or_dir
from responses_service import ResponsesService
from persistence.agents_repository import AgentsRepository
from persistence.lookups_repository import LookupsRepository
from persistence.synonyms_repository import SynonymsRepository
from persistence.training_data_repository import TrainingDataRepository
from persistence.responses_repository import ResponsesRepository
from persistence.users_repository import UsersRepository
from persistence.contexts_repository import ContextsRepository
from persistence.analytics_repository import AnalyticsRepository
from persistence.mongo_encoder import MongoJSONEncoder
from models_loader import get_loader
import logging

logger = logging.getLogger(__name__)

class AgentsService(object):
    
    __instance = None

    @staticmethod 
    def get_instance():
      """ Static access method. """
      if AgentsService.__instance is None:
         AgentsService()
      return AgentsService.__instance

    def __init__(self):
      """ Virtually private constructor. """
      if AgentsService.__instance is not None:
         raise Exception("AgenService is a singleton!")
      else:
         self.bots = {}
         self.agents_repository = AgentsRepository()
         self.training_data_repository = TrainingDataRepository()
         self.lookups_repository = LookupsRepository()
         self.synonyms_repository = SynonymsRepository()
         self.responses_repository = ResponsesRepository()
         self.users_repository = UsersRepository()
         self.contexts_repository = ContextsRepository()
         self.analytics_repository = AnalyticsRepository()
         AgentsService.__instance = self

    def starting_load_agents(self):
        agents = self.agents_repository.get_all_agents()
        botsList = []
        for agent in agents:
            try:
                agent_name = agent.get("name")
                logger.info("Start loading Agent {0}".format(agent_name))
                model_name = agent.get("current_version")
                botsList.append(agent_name)
                bot_dir = os.environ.get("MODELS_PATH") + agent_name + "/"
                if model_name is None or model_name == "None" or model_name == "":
                    models = self.get_models(agent_name)
                    if not models:
                        logger.info("No models exist for agent {0}".format(agent_name))
                        self.bots[agent_name] = Agent()
                        continue
                    else:
                        models.sort(reverse=True)
                        model_name = models[0]
                self.load_agent(agent_name, model_name)
            except Exception as e:
                logger.error("Agent {0} could not be loaded at starting with exception: {1}".format(agent_name, e), exc_info=True)

    def get_agent_training_data(self, agent_name):
        tmp_data = []
        train_data = self.training_data_repository.find_agent_training_data(agent_name)
        for entry in train_data:    
            del entry["_id"]
            tmp_data.append(entry["data"])
        return tmp_data

    def get_agent_lookups(self, agent_name):
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

    def get_agent_synonyms(self, agent_name):
        tmp_data = []
        synonyms = self.synonyms_repository.find_agent_synonyms(agent_name)
        for entry in synonyms:    
            del entry["_id"]
            tmp_data.append(entry["synonyms"])
        return tmp_data

    def get_bots(self):
        """Get Bots loaded in memory""" 
        return self.bots

    def get_agents(self):
        db_agents = self.agents_repository.get_all_agents()
        agents = []
        for entry in db_agents:
            agents.append(json.loads(MongoJSONEncoder().encode(entry)))
        return agents

    def get_training_data(self, agent_name, intent=None, pageNumber=30, pageSize=30):
        db_training_data = self.training_data_repository.get_agent_training_data(agent_name, intent, pageNumber, pageSize)
        trainingData = []
        for entry in db_training_data:
            trainingData.append(json.loads(MongoJSONEncoder().encode(entry)))
        count_training_data = self.training_data_repository.count_agent_training_data(agent_name)
        return { 
            "count" : count_training_data,
            "items": trainingData
            }

    def get_agent(self, agent_name):
        agent = self.agents_repository.find_agent(agent_name)
        try:
            return json.loads(MongoJSONEncoder().encode(agent))
        except:
            return None

    def agent_exist(self, agent_name):
        agent = self.get_agent(agent_name)
        if agent is None:
            return False
        else:
            return True
    
    def map_multiple_training(self, agent_name, data):
        training_data = []
        intents = set()
        entities = set()
        for entry in data:
            training_data.append({"agent_name": agent_name, "data": entry})
            if entry.get("intent") is not None:
                intents.add(entry.get("intent"))
            if entry.get("entities") is not None:
                for entity in entry.get("entities"):
                    entities.add(entity.get("entity"))
        data = {
            "training_data" : training_data,
            "intents": list(intents),
            "entities": list(entities)
        }
        return data

    def map_intent_and_entities(self, entry):
        intent = ""
        entities = set()
        if entry.get("intent") is not None:
            intent = entry.get("intent")
        if entry.get("entities") is not None:
            for entity in entry.get("entities"):
                entities.add(entity.get("entity"))
        intent_entities = {
            "intent": intent,
            "entities": list(entities)
        }
        return intent_entities

    def create_agent(self, agent_name, last_train, config, nlu_data, fallback, responses, model_name):
        try:
            last_train = 0
            last_modified = 1
            intents = ["FALLBACK"]

            """Insert agent"""
            mappedData = {
                "name": agent_name,
                "last_train": last_train,
                "config": config,
                "fallback": fallback,
                "current_version": "",
                "last_version": "",
                "last_modified": last_modified,
                "intents": intents
            }
            self.agents_repository.insert_agent(mappedData)

            """Add nlu data"""
            if nlu_data is not None:
                """Add Common examples"""
                if nlu_data.get("common_examples") is not None:
                    self.add_agent_training_data(agent_name, nlu_data.get("common_examples"))

                """Add lookup tables"""
                if nlu_data.get("lookup_tables") is not None:
                    self.add_agent_lookups(agent_name, nlu_data.get("lookup_tables"))

                """Add Synonyms"""
                if nlu_data.get("entity_synonyms") is not None:
                    self.add_agent_synonyms(agent_name, nlu_data.get("entity_synonyms"))

            """Add responses"""
            if responses is not None:
                ResponsesService.get_instance().add_agent_responses(agent_name, responses)

            if model_name is None:
                model_name = "None"

            self.bots[agent_name] = Agent()
        except Exception as e:
            logger.error("Exception when creating agent {0}. {1}".format(agent_name, e), exc_info=True)

    def delete_agent(self, agent_name):
        """ Remove entries in database """
        self.cleanup_agent(agent_name)

        """ Remove persisted models """
        model_loader = get_loader(os.environ.get("MODEL_LOADER"))
        model_loader.remove_all(agent_name)
        
        """ Remove model file """
        remove_file_or_dir(os.environ.get("MODELS_PATH") + agent_name)
        
        self.delete_agent_from_memory(agent_name)

    def cleanup_agent(self, agent_name):
        self.agents_repository.delete_agent(agent_name)
        counter = 0
        maxTries = int(os.environ.get("MAX_DELETE_RETRY", 50))
        while True:
            try:
                self.training_data_repository.delete_all_training_data(agent_name)
                self.lookups_repository.delete_lookups(agent_name)
                self.synonyms_repository.delete_agent_synonyms(agent_name)
                self.responses_repository.delete_all_agent_responses(agent_name)
                self.contexts_repository.delete_contexts(agent_name)
                self.agents_repository.delete_agent(agent_name)
                return True
            except Exception as e:
                if e.__class__.__name__ == "OperationFailure":
                    counter = counter + 1
                    logger.debug("Retry number {0} to remove agent {1} due to operation exception".format(counter, agent_name))
                    if counter == maxTries:
                        logger.error("Exception Max retries reached when deleting agent from database. {0}".format(e))
                        return False 
                else:
                    logger.error("Exception when deleting agent {0} from database. {1}".format(agent_name, e))
                    return False
    
    def delete_agent_from_memory(self, agent_name):
        try:
            if agent_name in self.bots:
                self.bots.pop(agent_name)
        except Exception as e:
            logger.error("Error deleting agent {0} from memory. {1}".format(agent_name, e), exc_info=True)

    def training_data_exist(self, id):
        if not ObjectId.is_valid(id) or self.training_data_repository.find_training_data(id) is None:
            return False
        else:
            return True

    def delete_agent_training_data(self, agent_name, id):
        if (self.training_data_repository.delete_training_data(agent_name, id)):
            self.agents_repository.agent_modified(agent_name)

    def update_agent_training_data(self, agent_name, id, train_data):
        if (self.training_data_repository.update_training_data(agent_name, id, train_data)):
            intents_entities = self.map_intent_and_entities(train_data)
            self.agents_repository.update_agent_intents(agent_name, [intents_entities.get("intent")])
            self.agents_repository.update_agent_entities(agent_name, intents_entities.get("entities"))
            self.agents_repository.agent_modified(agent_name)

    def add_agent_training_data(self, agent_name, train_data):
        mappedData = self.map_multiple_training(agent_name, train_data)
        if self.training_data_repository.insert_training_data(mappedData.get("training_data")):
            self.agents_repository.update_agent_intents(agent_name, mappedData.get("intents"))
            self.agents_repository.update_agent_entities(agent_name, mappedData.get("entities"))
            self.agents_repository.agent_modified(agent_name)

    def load_agent(self, agent_name, model_name):
        model_loader = get_loader(os.environ.get("MODEL_LOADER"))
        download_path = model_loader.retrieve(agent_name, model_name)

        self.bots[agent_name] = Agent(model = download_path)
        self.agents_repository.update_model(agent_name, model_name)
        logger.info("Agent {0} loaded with version {1}, ".format(agent_name, model_name))

        try :
            downloadDir = os.environ.get("MODELS_PATH") + agent_name + "/"
            for root, dirs, files in os.walk(downloadDir):
                for file in files:
                    if not file == model_name + ".tar.gz":
                        remove_file_or_dir(os.path.join(root, file))
        except Exception as e:
            logger.error("Exception when deleting models for agent {0}, after loading model {1}.  {2}".format(agent_name, model_name, e), exc_info=True)

    def is_fallback(self, agent_name, confidence):
        fallback = self.agents_repository.get_fallback(agent_name).get("fallback")
        if fallback is None:
            fallback = 0
        if confidence <= fallback:
            return(True)
        else:
            return(False)

    def add_agent_lookups(self, agent_name, lookups):
        data = []
        lookup_limit_size = int(os.environ.get("LOOKUP_LIMIT_SIZE", 5000))
        is_agent_modified = False
        for entry in lookups:
            elements_size = len(entry.get("elements"))
            logger.debug("Lookup {0} insertion for agent {1} with size {2} and size limit {3}.".format(entry.get("name"), agent_name, elements_size, lookup_limit_size))
            if (elements_size < lookup_limit_size):
                data.append({"agent_name": agent_name, "lookups": entry})
            else:
                split_size = int(elements_size / lookup_limit_size)
                splitted_arr = np.array_split(entry.get("elements"), split_size)
                for splitted_entry in splitted_arr:
                    splitted_lookup = [{"agent_name": agent_name, "lookups": {"name": entry.get("name"),"elements": splitted_entry.tolist()}}]
                    is_agent_modified = self.lookups_repository.insert_lookups(splitted_lookup)
        if self.lookups_repository.insert_lookups(data) or is_agent_modified:
            self.agents_repository.agent_modified(agent_name)

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

    def create_agent_file(self, agent_name):
        agent_data = self.get_agent(agent_name)
        agent = {}
        agent["config"] = agent_data.get("config")
        agent["rasa_nlu_data"] = {}
        agent["rasa_nlu_data"]["common_examples"] = self.get_agent_training_data(agent_name)
        agent["rasa_nlu_data"]["lookup_tables"] = self.get_agent_lookups(agent_name)
        agent["rasa_nlu_data"]["entity_synonyms"] = self.get_agent_synonyms(agent_name)
        agent["responses"] = ResponsesService.get_instance().get_agent_responses(agent_name)
        return agent

    def store_user_input(self, agent_name, nlu_data, userId):
        try:
            user_input = {}
            user_input["agent_name"] = agent_name 
            user_input["user_id"] = userId
            user_input["text"] = nlu_data.get("text") 
            user_input["intent"] = nlu_data.get("intent") 
            user_input["entities"] = nlu_data.get("entities") 
            user_input["fulfillment_text"] = nlu_data.get("fulfillment_text") 
            user_input["date"] = datetime.utcnow()
            self.users_repository.insert_user_input(user_input)
        except:
            logger.error("Can't insert user input for agent {0}. {1}".format(agent_name, e), exc_info=True)
    
    def get_agent_inputs(self,agent_name, max_confidence, min_confidence, page_number, page_size):
        db_user_inputs = self.users_repository.get_agent_inputs(agent_name, max_confidence, min_confidence, page_number, page_size)
        users_inputs = []
        for db_user_input in db_user_inputs:
                users_inputs.append(json.loads(MongoJSONEncoder().encode(db_user_input)))
        count_inputs = self.users_repository.count_user_inputs(agent_name)
        return { 
            "count" : count_inputs,
            "items": users_inputs
            }
    
    def get_user_inputs(self,agent_name, userId, maxConfidence, minConfidence, pageNumber, pageSize):
        return(self.users_repository.get_user_inputs(agent_name, userId, maxConfidence, minConfidence, pageNumber, pageSize))

    def delete_agent_user_input(self,agent_name, input_id):
        return(self.users_repository.delete_user_input(agent_name, input_id))

    def get_intent_by_text(self, text, agent_name):
        return(self.training_data_repository.get_intent_by_text(text, agent_name))

    def get_trained_agents(self):
        trained_agents = []
        agents = self.agents_repository.get_all_agents()
        for agent in agents:
            try:
                if (agent.get("last_train") > agent.get("last_modified")) and (agent.get("last_version") != agent.get("current_version")):
                    trained_agents.append({
                        "name": agent.get("name"),
                        "last_version": agent.get("last_version")
                    })
            except Exception:
                logger.error("Exception when get trained agent {0}.".format(agent.get("name")), exc_info=True)
        return trained_agents

    def get_models(self, agent_name):
        return self.agents_repository.get_versions(agent_name).get("versions")

    def get_analytics(self, agent_name, days_number):
        analytics_response = {
            "agent_name": agent_name,
            "analytics": []
        }
        analytics = self.analytics_repository.find_agent_analytics(agent_name, days_number)
        for analytic in analytics:    
            del analytic["_id"]
            del analytic["agent_name"]
            analytics_response.get("analytics").append(analytic)
        return analytics_response
