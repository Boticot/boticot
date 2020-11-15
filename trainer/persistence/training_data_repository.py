from .mongodb import mongo

class TrainingDataRepository():

    def __init__(self):
        self.trainingDataCollection = mongo.db.trainingData
        
    def find_agent_training_data(self, agentName):
        return self.trainingDataCollection.find({"agentName": agentName})
