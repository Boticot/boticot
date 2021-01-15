from rasa.nlu.model import Interpreter
from rasa.model import unpack_model
from utils import remove_file_or_dir
import os
import logging

logger = logging.getLogger(__name__)
class Agent(object):
    def __init__(self, **kwargs):
        model_path = kwargs.get("model", None)
        try:
            if model_path is not None:
                logger.info("Loading model " + model_path)
                if os.path.isdir(model_path):
                    self.interpreter = Interpreter.load(model_path)
                elif model_path.endswith(".tar.gz"):
                    model = unpack_model(model_path)
                    if os.path.isdir(model + "/nlu"):
                        self.interpreter = Interpreter.load(model + "/nlu")
                    else:
                        self.interpreter = Interpreter.load(model)
                self.interpreter.parse("ok")

                """Cleanup tmp files and directories"""
                try :
                    if model is not None:
                        remove_file_or_dir(model)
                    tmp_dir = "/tmp/"
                    for root, dirs, files in os.walk(tmp_dir):
                        for file in files:
                            if file.startswith("tmp") and file.endswith(".py"):
                                remove_file_or_dir(tmp_dir+file)
                except Exception as e:
                    logger.error("Exception when cleanup tmp files and directories.", exc_info=True)
            else:
                self.interpreter = None
        except Exception as e:
            logger.error("Error when loading model {0}, exception {1}".format(model_path, e), exc_info=True)
            remove_file_or_dir(model_path)
            raise

    def handle(self, message, agent_name):
        from agents_service import AgentsService
        from responses_service import ResponsesService
        nlu_data = {}
        nlu_data["intent"] = {}
        nlu_data["text"] = message
        intent_from_base = AgentsService.get_instance().get_intent_by_text(message, agent_name)
        if intent_from_base is not None:
            intent = intent_from_base["data"]["intent"]
            nlu_data["intent"]["name"] = intent
            nlu_data["intent"]["confidence"] = 1
            nlu_data["entities"] = intent_from_base["data"].get("entities")
        else:
            if self.interpreter is None:
                intent = "UNKNOWN"
                nlu_data["intent"]["name"] = "UNKNOWN"
                nlu_data["intent"]["confidence"] = 1
            else:
                nlu_data = self.interpreter.parse(message)
                confidence = float(nlu_data.get("intent").get("confidence"))
                intent = nlu_data.get("intent").get("name")
                if AgentsService.get_instance().is_fallback(agent_name, confidence):
                    intent = "FALLBACK"
                    nlu_data["intent"]["name"] = intent
                    nlu_data["intent"]["confidence"] = 1
        nlu_data["fulfillment_text"] = ResponsesService.get_instance().get_response(agent_name, intent)
        return nlu_data


