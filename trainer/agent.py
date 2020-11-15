from rasa.nlu.training_data.loading import load_data
from rasa.nlu import config
from rasa.nlu.model import Trainer
from rasa.model import package_model
import logging

logger = logging.getLogger(__name__)

class Agent(object):
    def __init__(self, agentName, botconfig, data,**kwargs):
        logger.info("Training Agent " + agentName + " in progress")
        trainingData = load_data(data)
        self.intents = list(trainingData.intents)
        self.entities = list(trainingData.entities)
        trainer = Trainer(config.load(botconfig))
        self.interpreter = trainer.train(trainingData)
        self.model_path = "./models/" + agentName + "/"
        persist_path = trainer.persist(self.model_path)
        self.tar_path = package_model(fingerprint = None, train_path = persist_path, output_directory = self.model_path)
        self.model_name = self.tar_path.replace(self.model_path,"")
        self.model_version = self.model_name[:self.model_name.index(".tar.gz")]

