import pytest
import sys
sys.path.append(".")
import agents_service


class TestAgentsService:

    agent_name = "test1"
    regex = ["regex"]
    id = 3
    nlu_data = {"regex_features": [{"name": "zipcode", "pattern": "[0-9]{5}"}]}

    @pytest.fixture(scope="function", autouse=True)
    def mock_functions(self, mocker):
        mock_list = ["TrainingDataRepository", "LookupsRepository", "ResponsesRepository", "UsersRepository",
                     "ContextsRepository", "AnalyticsRepository", "AgentsRepository.agent_modified"]
        for mock in mock_list:
            mocker.patch("agents_service.{}".format(mock))
        mocker.patch("agents_service.SynonymsRepository.__init__", lambda x: None)
        mocker.patch("agents_service.AgentsRepository.__init__", lambda x: None)
        mocker.patch("agents_service.RegexRepository.__init__", lambda x: None)

    def test_should_return_last_model_name(self, mocker):
        mocker.patch("os.environ.get", return_value="models")
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("os.listdir", return_value=["20220114-092705.tar.gz", "20220114-092005.tar.gz"])
        mocker.patch("os.path.isfile", return_value=True)
        assert agents_service.AgentsService.get_instance().retrieve_last_model_name(self.agent_name) == "20220114-092705"

    def test_should_return_something_when_get_agent_regex_is_called(self, mocker):
        mocker.patch("agents_service.RegexRepository.find_agent_regex",
                     return_value=[{"_id": 1, "regex": "reg1"}, {"_id": 2, "regex": "reg2"}])
        assert agents_service.AgentsService.get_instance().get_agent_regex(self.agent_name) == ["reg1", "reg2"]

    def test_should_call_agent_modified_when_insert_regex_returns_true(self, mocker):
        mocker.patch("agents_service.RegexRepository.insert_regex", return_value=True)
        agents_service.AgentsService.get_instance().add_agent_regex(self.agent_name, self.regex)
        agents_service.AgentsRepository.agent_modified.assert_called()

    def test_should_not_call_agent_modified_when_insert_regex_returns_false(self, mocker):
        mocker.patch("agents_service.RegexRepository.insert_regex", return_value=False)
        agents_service.AgentsService.get_instance().add_agent_regex(self.agent_name, self.regex)
        agents_service.AgentsRepository.agent_modified.assert_not_called()

    def test_should_call_add_agent_regex_when_regex_features_is_not_none(self, mocker):
        mocker.patch("agents_service.AgentsService.add_agent_regex")
        mocker.patch("agents_service.AgentsRepository.insert_agent")
        agents_service.AgentsService.get_instance().create_agent(self.agent_name, 0, "config", self.nlu_data,
                                                                     "fallback", "responses", "model_name")
        agents_service.AgentsService.add_agent_regex.assert_called()
        mocker.stopall()

    def test_should_call_delete_agent_regex_when_cleanup_agent_is_called(self, mocker):
        mocker.patch("agents_service.AgentsRepository.delete_agent")
        mocker.patch("agents_service.RegexRepository.delete_agent_regex")
        mocker.patch("agents_service.SynonymsRepository.delete_agent_synonyms")
        agents_service.AgentsService.get_instance().cleanup_agent(self.agent_name)
        agents_service.RegexRepository.delete_agent_regex.assert_called()

    def test_should_return_something_when_create_agent_file_is_called(self, mocker):
        mocker.patch("agents_service.AgentsService.get_agent")
        mocker.patch("agents_service.AgentsService.get_agent_regex", return_value=["reg1", "reg2"])
        mocker.patch("agents_service.ResponsesService")
        mocker.patch("agents_service.SynonymsService.get_agent_synonyms")
        agent = agents_service.AgentsService.get_instance().create_agent_file(self.agent_name)
        assert agent["rasa_nlu_data"]["regex_features"] == ["reg1", "reg2"]
        mocker.stopall()

    def test_should_regex_exist_when_find_regex_returns_something(self, mocker):
        mocker.patch("agents_service.ObjectId.is_valid", return_value=True)
        mocker.patch("agents_service.RegexRepository.find_regex", return_value="regex")
        assert agents_service.AgentsService.get_instance().regex_exist(self.id) == True

    def test_should_regex_not_exist_when_find_regex_returns_none(self, mocker):
        mocker.patch("agents_service.ObjectId.is_valid", return_value=True)
        mocker.patch("agents_service.RegexRepository.find_regex", return_value=None)
        assert agents_service.AgentsService.get_instance().regex_exist(self.id) == False

    def test_should_regex_not_exist_when_id_is_not_valid(self, mocker):
        mocker.patch("agents_service.ObjectId.is_valid", return_value=False)
        mocker.patch("agents_service.RegexRepository.find_regex", return_value="regex")
        assert agents_service.AgentsService.get_instance().regex_exist(self.id) == False

    def test_should_call_agent_modified_when_delete_regex_returns_true(self, mocker):
        mocker.patch("agents_service.RegexRepository.delete_regex", return_value=True)
        agents_service.AgentsService.get_instance().delete_agent_regex(self.agent_name, self.id)
        agents_service.AgentsRepository.agent_modified.assert_called()

    def test_should_not_call_agent_modified_when_delete_regex_returns_false(self, mocker):
        mocker.patch("agents_service.RegexRepository.delete_regex", return_value=False)
        agents_service.AgentsService.get_instance().delete_agent_regex(self.agent_name, self.id)
        agents_service.AgentsRepository.agent_modified.assert_not_called()

    def test_should_call_agent_modified_when_update_regex_returns_true(self, mocker):
        mocker.patch("agents_service.RegexRepository.update_regex", return_value=True)
        agents_service.AgentsService.get_instance().update_agent_regex(self.agent_name, self.id, self.regex)
        agents_service.AgentsRepository.agent_modified.assert_called()

    def test_should_not_call_agent_modified_when_update_regex_returns_false(self, mocker):
        mocker.patch("agents_service.RegexRepository.update_regex", return_value=False)
        agents_service.AgentsService.get_instance().update_agent_regex(self.agent_name, self.id, self.regex)
        agents_service.AgentsRepository.agent_modified.assert_not_called()

    def test_should_return_something_when_getting_regex(self, mocker):
        mocker.patch("agents_service.RegexRepository.get_agent_regex", return_value=["regex1", "regex2"])
        mocker.patch("agents_service.RegexRepository.count_agent_regex", return_value=2)
        assert agents_service.AgentsService.get_instance().get_regex(self.agent_name) == {"count": 2, "items": ["regex1", "regex2"]}
