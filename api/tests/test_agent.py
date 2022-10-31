import pytest
import sys
sys.path.append(".")
import agent


class TestAgent:

    test_agent = None

    @pytest.fixture(scope="function", autouse=True)
    def mock_functions(self):
        self.test_agent = agent.Agent()

    def test_should_call_check_entity_overlap_when_handling_text(self, mocker):
        self.test_agent.interpreter = agent.Interpreter(list(), dict())
        mock_list = ["ResponsesRepository", "AgentsRepository"]
        for mock in mock_list:
             mocker.patch("responses_service.{}".format(mock))
        mock_list = ["TrainingDataRepository.__init__", "SynonymsRepository.__init__", "AgentsRepository.__init__",
                     "LookupsRepository.__init__", "UsersInputsRepository.__init__", "ResponsesRepository.__init__",
                     "UsersRepository.__init__", "ContextsRepository.__init__", "AnalyticsRepository.__init__"]
        for mock in mock_list:
             mocker.patch("agents_service.{}".format(mock), lambda x: None)
        nlu_data = {"intent": {"confidence": 0.98},
                    "entities": [{"value": "value1", "extractor": "CRFEntityExtractor", "start": 1, "end": 6},
                                 {"value": "demain", "extractor": "DucklingHTTPExtractor", "start": 8, "end": 13}]}
        mocker.patch("agents_service.AgentsService.get_intent_by_text", return_value=None)
        mocker.patch("responses_service.ResponsesService.get_response", return_value="response")
        mocker.patch("agent.Interpreter.parse", return_value=nlu_data)
        mocker.patch("agent.check_entity_overlap")
        mocker.patch("agents_service.AgentsService.is_fallback", return_value=False)
        self.test_agent.handle_text("text", "test1", None)
        agent.check_entity_overlap.assert_called()
