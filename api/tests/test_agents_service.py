import pytest
import sys
sys.path.append(".")
import agents_service


class TestAgentsService:

    agent_name = "test1"

    @pytest.fixture(scope="function", autouse=True)
    def mock_functions(self, mocker):
        mock_list = ["TrainingDataRepository", "LookupsRepository", "ResponsesRepository", "UsersRepository",
                     "ContextsRepository", "AnalyticsRepository", "AgentsRepository.agent_modified"]
        for mock in mock_list:
            mocker.patch("agents_service.{}".format(mock))
        mocker.patch("agents_service.SynonymsRepository.__init__", lambda x: None)
        mocker.patch("agents_service.AgentsRepository.__init__", lambda x: None)

    def test_should_return_last_model_name(self, mocker):
        mocker.patch("os.environ.get", return_value="models")
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("os.listdir", return_value=["20220114-092705.tar.gz", "20220114-092005.tar.gz"])
        mocker.patch("os.path.isfile", return_value=True)
        assert agents_service.AgentsService.get_instance().retrieve_last_model_name(self.agent_name) == "20220114-092705"
