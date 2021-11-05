import pytest
import sys
sys.path.append(".")
import agents_service


class TestAgentsService:

    agent_name = "test1"
    lookup_name = "city"
    lookup_json = [{"name": "lookup1", "elements": ["e1", "e2"]},
                   {"name": "lookup2", "elements": ["e3", "e4"]}]
    lookup_json_max = [{"name": "lookup1", "elements": ["e1"] * 5000},
                       {"name": "lookup2", "elements": ["e3"] * 5000}]
    lookup_db = [{"_id": 1, "lookups": {"name": "lookup1", "elements": ["e1", "e2"]}},
                {"_id": 2, "lookups": {"name": "lookup2", "elements": ["e3", "e4"]}}]
    id = 3

    @pytest.fixture(scope="function", autouse=True)
    def mock_functions(self, mocker):
        mock_list = ["TrainingDataRepository", "ResponsesRepository",
                     "UsersRepository", "ContextsRepository", "AnalyticsRepository", "AgentsRepository.agent_modified"]
        for mock in mock_list:
            mocker.patch("agents_service.{}".format(mock))
        mocker.patch("agents_service.SynonymsRepository.__init__", lambda x: None)
        mocker.patch("agents_service.AgentsRepository.__init__", lambda x: None)
        mocker.patch("agents_service.LookupsRepository.__init__", lambda x: None)

    def test_should_return_last_model_name(self, mocker):
        mocker.patch("os.environ.get", return_value="models")
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("os.listdir", return_value=["20220114-092705.tar.gz", "20220114-092005.tar.gz"])
        mocker.patch("os.path.isfile", return_value=True)
        assert agents_service.AgentsService.get_instance().retrieve_last_model_name(self.agent_name) == "20220114-092705"

    def test_should_return_something_when_getting_agent_lookups(self, mocker):
        mocker.patch("agents_service.LookupsRepository.find_agent_lookups",
                     return_value=self.lookup_db)
        assert agents_service.AgentsService.get_instance().get_agent_lookups(self.agent_name) == self.lookup_json

    def test_should_call_agent_modified_when_deleting_lookup(self, mocker):
        mocker.patch("agents_service.LookupsRepository.delete_lookup", return_value=True)
        agents_service.AgentsService.get_instance().delete_agent_lookup(self.agent_name, self.lookup_name)
        agents_service.AgentsRepository.agent_modified.assert_called()

    def test_should_not_call_agent_modified_when_not_deleting_lookup(self, mocker):
        mocker.patch("agents_service.LookupsRepository.delete_lookup", return_value=False)
        agents_service.AgentsService.get_instance().delete_agent_lookup(self.agent_name, self.lookup_name)
        agents_service.AgentsRepository.agent_modified.assert_not_called()

    def test_should_lookup_exist_when_find_lookup_returns_something(self, mocker):
        mocker.patch("agents_service.LookupsRepository.find_lookup", return_value=["lookup1"])
        assert agents_service.AgentsService.get_instance().lookup_exist(self.agent_name, self.lookup_name) == True

    def test_should_lookup_not_exist_when_find_lookup_returns_nothing(self, mocker):
        mocker.patch("agents_service.LookupsRepository.find_lookup", return_value=[])
        assert agents_service.AgentsService.get_instance().lookup_exist(self.agent_name, self.lookup_name) == False

    def test_should_call_agent_modified_when_inserting_lookups(self, mocker):
        mocker.patch("agents_service.LookupsRepository.insert_lookups", return_value=True)
        agents_service.AgentsService.get_instance().add_agent_lookups(self.agent_name, self.lookup_json)
        agents_service.AgentsRepository.agent_modified.assert_called()

    def test_should_not_call_agent_modified_when_not_inserting_lookups(self, mocker):
        mocker.patch("agents_service.LookupsRepository.insert_lookups", return_value=False)
        agents_service.AgentsService.get_instance().add_agent_lookups(self.agent_name, self.lookup_json)
        agents_service.AgentsRepository.agent_modified.assert_not_called()

    def test_should_call_agent_modified_when_overflowing_lookups_size_limit(self, mocker):
        mocker.patch("agents_service.LookupsRepository.insert_lookups",side_effect = [True, True, False])
        agents_service.AgentsService.get_instance().add_agent_lookups(self.agent_name, self.lookup_json_max)
        agents_service.AgentsRepository.agent_modified.assert_called()

    def test_should_return_something_when_getting_lookups(self, mocker):
        mocker.patch("agents_service.LookupsRepository.get_agent_lookups", return_value=["lookup1", "lookup2"])
        mocker.patch("agents_service.LookupsRepository.count_agent_lookups", return_value=2)
        assert agents_service.AgentsService.get_instance().get_lookups(self.agent_name) == {"count": 2, "items": ["lookup1", "lookup2"]}
