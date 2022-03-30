import pytest
import sys
sys.path.append(".")
import persistence.training_data_repository as training_data_repository


class TestTrainingDataRepository:

    training_data_repository = None

    @pytest.fixture(scope="function", autouse=True)
    def mock_functions(self, mocker):
        mocker.patch("persistence.training_data_repository.mongo")
        self.training_data_repository = training_data_repository.TrainingDataRepository()

    def test_should_call_find_when_getting_training_data(self):
        self.training_data_repository.get_agent_training_data("test1", None, None, 30, 30)
        self.training_data_repository.training_data_collection.find.assert_called_with({"agent_name": "test1"}, {"agent_name": 0})

    def test_should_call_find_when_getting_training_data_by_intent(self):
        self.training_data_repository.get_agent_training_data("test1", "greetings_hello", None, 30, 30)
        self.training_data_repository.training_data_collection.find.assert_called_with({"agent_name": "test1", "data.intent": "greetings_hello"}, {"agent_name": 0})

    def test_should_call_find_when_getting_training_data_by_text(self):
        self.training_data_repository.get_agent_training_data("test1", None, "text", 30, 30)
        self.training_data_repository.training_data_collection.find.assert_called_with({"agent_name": "test1", "data.text": {"$regex": ".*" + "text" + ".*", "$options" : "-i"}}, {"agent_name": 0})

    def test_should_call_find_when_getting_training_data_by_intent_and_by_text(self):
        self.training_data_repository.get_agent_training_data("test1", "greetings_hello", "text", 30, 30)
        self.training_data_repository.training_data_collection.find.assert_called_with({"agent_name": "test1", "data.intent": "greetings_hello", "data.text": {"$regex": ".*" + "text" + ".*", "$options" : "-i"}}, {"agent_name": 0})

    def test_should_call_count_when_counting_training_data(self):
        self.training_data_repository.count_agent_training_data("test1", None, None)
        self.training_data_repository.training_data_collection.count.assert_called_with({"agent_name": "test1"})

    def test_should_call_count_when_counting_training_data_by_intent(self):
        self.training_data_repository.count_agent_training_data("test1", "greetings_hello", None)
        self.training_data_repository.training_data_collection.count.assert_called_with({"agent_name": "test1", "data.intent": "greetings_hello"})

    def test_should_call_count_when_counting_training_data_by_text(self):
        self.training_data_repository.count_agent_training_data("test1", None, "text")
        self.training_data_repository.training_data_collection.count.assert_called_with({"agent_name": "test1", "data.text": {"$regex": ".*" + "text" + ".*", "$options": "-i"}})

    def test_should_call_count_when_counting_training_data_by_intent_and_by_text(self):
        self.training_data_repository.count_agent_training_data("test1", "greetings_hello", "text")
        self.training_data_repository.training_data_collection.count.assert_called_with({"agent_name": "test1", "data.intent": "greetings_hello", "data.text": {"$regex": ".*" + "text" + ".*", "$options" : "-i"}})
