import pytest
import sys
import os
import json
from copy import deepcopy

sys.path.append(".")
import agents_service


class TestAgentsService:

    lookup_json_max = [{"name": "lookup1", "elements": ["e1"] * 5000},
                       {"name": "lookup2", "elements": ["e3"] * 5000}]

    with open("tests/mock_data/agents_service.json") as json_file:
        mock_data = json.load(json_file)

    @pytest.fixture(scope="function", autouse=True)
    def mock_functions(self, mocker):
        mock_list = ["ContextsRepository", "AnalyticsRepository", "AgentsRepository.agent_modified"]
        for mock in mock_list:
            mocker.patch("agents_service.{}".format(mock))
        mocker.patch("agents_service.SynonymsRepository.__init__", lambda x: None)
        mocker.patch("agents_service.AgentsRepository.__init__", lambda x: None)
        mocker.patch("agents_service.LookupsRepository.__init__", lambda x: None)
        mocker.patch("agents_service.TrainingDataRepository.__init__", lambda x: None)
        mocker.patch("agents_service.UsersRepository.__init__", lambda x: None)
        mocker.patch("agents_service.UsersInputsRepository.__init__", lambda x: None)
        mocker.patch("agents_service.ResponsesRepository.__init__", lambda x: None)

    def test_should_return_last_model_name(self, mocker):
        mocker.patch("os.environ.get", return_value="models")
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("os.listdir", return_value=["20220114-092705.tar.gz", "20220114-092005.tar.gz"])
        mocker.patch("os.path.isfile", return_value=True)
        assert agents_service.AgentsService.get_instance().retrieve_last_model_name(self.mock_data["agent_name"]) == "20220114-092705"

    def test_should_return_something_when_getting_agent_lookups(self, mocker):
        mocker.patch("agents_service.LookupsRepository.find_agent_lookups",
                     return_value=deepcopy(self.mock_data["lookup_db"]))
        assert agents_service.AgentsService.get_instance().get_agent_lookups(self.mock_data["agent_name"]) == self.mock_data["lookup_json"]

    def test_should_call_agent_modified_when_deleting_lookup(self, mocker):
        mocker.patch("agents_service.LookupsRepository.delete_lookup", return_value=True)
        agents_service.AgentsService.get_instance().delete_agent_lookup(self.mock_data["agent_name"], self.mock_data["lookup_name"])
        agents_service.AgentsRepository.agent_modified.assert_called()

    def test_should_not_call_agent_modified_when_not_deleting_lookup(self, mocker):
        mocker.patch("agents_service.LookupsRepository.delete_lookup", return_value=False)
        agents_service.AgentsService.get_instance().delete_agent_lookup(self.mock_data["agent_name"], self.mock_data["lookup_name"])
        agents_service.AgentsRepository.agent_modified.assert_not_called()

    def test_should_lookup_exist_when_find_lookup_returns_something(self, mocker):
        mocker.patch("agents_service.LookupsRepository.find_lookup", return_value=["lookup1"])
        assert agents_service.AgentsService.get_instance().lookup_exist(self.mock_data["agent_name"], self.mock_data["lookup_name"]) == True

    def test_should_lookup_not_exist_when_find_lookup_returns_nothing(self, mocker):
        mocker.patch("agents_service.LookupsRepository.find_lookup", return_value=[])
        assert agents_service.AgentsService.get_instance().lookup_exist(self.mock_data["agent_name"], self.mock_data["lookup_name"]) == False

    def test_should_call_agent_modified_when_inserting_lookups(self, mocker):
        mocker.patch("agents_service.LookupsRepository.insert_lookups", return_value=True)
        agents_service.AgentsService.get_instance().add_agent_lookups(self.mock_data["agent_name"], self.mock_data["lookup_json"])
        agents_service.AgentsRepository.agent_modified.assert_called()

    def test_should_not_call_agent_modified_when_not_inserting_lookups(self, mocker):
        mocker.patch("agents_service.LookupsRepository.insert_lookups", return_value=False)
        agents_service.AgentsService.get_instance().add_agent_lookups(self.mock_data["agent_name"], self.mock_data["lookup_json"])
        agents_service.AgentsRepository.agent_modified.assert_not_called()

    def test_should_call_agent_modified_when_overflowing_lookups_size_limit(self, mocker):
        mocker.patch("agents_service.LookupsRepository.insert_lookups",side_effect = [True, True, False])
        agents_service.AgentsService.get_instance().add_agent_lookups(self.mock_data["agent_name"], self.lookup_json_max)
        agents_service.AgentsRepository.agent_modified.assert_called()

    def test_should_return_something_when_getting_lookups(self, mocker):
        mocker.patch("agents_service.LookupsRepository.get_agent_lookups", return_value=["lookup1", "lookup2"])
        mocker.patch("agents_service.LookupsRepository.count_agent_lookups", return_value=2)
        assert agents_service.AgentsService.get_instance().get_lookups(self.mock_data["agent_name"]) == {"count": 2, "items": ["lookup1", "lookup2"]}

    def test_should_return_something_when_getting_training_data(self, mocker):
        mocker.patch("agents_service.TrainingDataRepository.get_agent_training_data", return_value=["data1", "data2"])
        mocker.patch("agents_service.TrainingDataRepository.count_agent_training_data", return_value=4)
        assert agents_service.AgentsService.get_instance().get_training_data("test1") == {"count" : 4,"items": ["data1", "data2"]}

    def test_should_return_something_when_getting_agent_inputs(self, mocker):
        mocker.patch("agents_service.UsersInputsRepository.get_agent_inputs", return_value=["data1", "data2"])
        mocker.patch("agents_service.UsersInputsRepository.count_user_inputs", return_value=4)
        assert agents_service.AgentsService.get_instance().get_agent_inputs("test1", None, None, 1, 0, 1, 20) == {"count" : 4,"items": ["data1", "data2"]}

    def test_should_create_agent_data_file(self, mocker):
        mocker.patch("os.environ.get", return_value="./models/")
        mocker.patch("agents_service.AgentsRepository.find_agent", return_value=deepcopy(self.mock_data["agent_db"]))
        mocker.patch("agents_service.TrainingDataRepository.find_agent_training_data", return_value=deepcopy(self.mock_data["training_data_db"]))
        mocker.patch("agents_service.LookupsRepository.find_agent_lookups", return_value=deepcopy(self.mock_data["lookup_db"]))
        mocker.patch("agents_service.SynonymsRepository.find_agent_synonyms", return_value=deepcopy(self.mock_data["synonyms_db"]))
        mocker.patch("agents_service.ResponsesRepository.find_agent_responses", return_value=deepcopy(self.mock_data["responses_db"]))
        agent_file = agents_service.AgentsService.get_instance().create_agent_file("Agent1")
        assert agent_file[0] == "./models/export/"
        assert agent_file[1] == "Agent1.json"
        assert agent_file[1] in os.listdir("./models/export/")

    def test_should_create_agent_data_intent_file(self, mocker):
        mocker.patch("os.environ.get", return_value="./models/")
        mocker.patch("agents_service.TrainingDataRepository.find_agent_training_data", return_value=deepcopy(self.mock_data["training_data_db"]))
        mocker.patch("agents_service.ResponsesRepository.find_agent_responses", return_value=deepcopy(self.mock_data["responses_db"]))
        agent_file = agents_service.AgentsService.get_instance().create_agent_file(agent_name= "Agent1", intent="Hello")
        assert agent_file[0] == "./models/export/"
        assert agent_file[1] == "Agent1_intent.json"
        assert agent_file[1] in os.listdir("./models/export/")

    def test_should_get_agent_data(self, mocker):
        mocker.patch("agents_service.AgentsRepository.find_agent", return_value=deepcopy(self.mock_data["agent_db"]))
        mocker.patch("agents_service.TrainingDataRepository.find_agent_training_data", return_value=deepcopy(self.mock_data["training_data_db"]))
        mocker.patch("agents_service.LookupsRepository.find_agent_lookups", return_value=deepcopy(self.mock_data["lookup_db"]))
        mocker.patch("agents_service.SynonymsRepository.find_agent_synonyms", return_value=deepcopy(self.mock_data["synonyms_db"]))
        mocker.patch("agents_service.ResponsesRepository.find_agent_responses", return_value=deepcopy(self.mock_data["responses_db"]))
        agent_data = agents_service.AgentsService.get_instance().get_agent_data(agent_name = "Agent1")
        assert all(key in agent_data for key in ["config", "rasa_nlu_data", "responses"])
        assert all(key in agent_data["rasa_nlu_data"] for key in ["common_examples", "lookup_tables", "entity_synonyms"])
        assert agent_data["config"] == {'language': 'en', 'pipeline': 'supervised_embeddings'}
        assert agent_data["rasa_nlu_data"]["common_examples"] == self.mock_data["expected_agent_data"]["rasa_nlu_data"]["common_examples"]
        assert agent_data["rasa_nlu_data"]["lookup_tables"] == self.mock_data["expected_agent_data"]["rasa_nlu_data"]["lookup_tables"]
        assert agent_data["rasa_nlu_data"]["entity_synonyms"] == self.mock_data["expected_agent_data"]["rasa_nlu_data"]["entity_synonyms"]
        assert agent_data["responses"] == self.mock_data["expected_agent_data"]["responses"]

    def test_should_get_agent_intent_data(self, mocker):
        mocker.patch("agents_service.TrainingDataRepository.find_agent_training_data", return_value=deepcopy(self.mock_data["training_data_intent_db"]))
        mocker.patch("agents_service.ResponsesRepository.find_agent_responses", return_value=deepcopy(self.mock_data["responses_intent_db"]))
        agent_data = agents_service.AgentsService.get_instance().get_agent_intent_data(agent_name = "Agent1", intent="greetings_hello")
        assert all(key in agent_data for key in ["rasa_nlu_data", "responses"])
        assert "common_examples" in agent_data["rasa_nlu_data"]
        assert agent_data["rasa_nlu_data"]["common_examples"] == self.mock_data["expected_agent_intent_data"]["rasa_nlu_data"]["common_examples"]
        assert agent_data["responses"] == self.mock_data["expected_agent_intent_data"]["responses"]
        
    def test_should_get_agent_intent_data_recursive(self, mocker):
        training_data_values = [deepcopy(self.mock_data["training_data_intent_db"]), deepcopy(self.mock_data["training_data_intent1_db"]), deepcopy(self.mock_data["training_data_intent2_db"])]
        responses_values = [deepcopy(self.mock_data["responses_intent_db"]), deepcopy(self.mock_data["responses_intent1_db"]), deepcopy(self.mock_data["responses_intent2_db"])]
        mocker.patch("agents_service.TrainingDataRepository.find_agent_training_data", side_effect=training_data_values)
        mocker.patch("agents_service.ResponsesRepository.find_agent_responses", side_effect=responses_values)
        agent_data = agents_service.AgentsService.get_instance().get_agent_intent_data_recursive(agent_name = "Agent1", intent="greetings_hello", visited=[])
        assert all(key in agent_data for key in ["rasa_nlu_data", "responses"])
        assert "common_examples" in agent_data["rasa_nlu_data"]
        assert agent_data["rasa_nlu_data"]["common_examples"] == self.mock_data["expected_agent_intent_data_recursive"]["rasa_nlu_data"]["common_examples"]
        assert agent_data["responses"] == self.mock_data["expected_agent_intent_data_recursive"]["responses"]
        