import pytest
import sys
sys.path.append(".")
import responses_service


class TestResponsesService:

    @pytest.fixture(scope="function", autouse=True)
    def mock_functions(self, mocker):
        mocker.patch("agents_service.ResponsesRepository.__init__", lambda x: None)
        mocker.patch("agents_service.AgentsRepository.__init__", lambda x: None)

    def test_should_return_something_when_getting_agent_responses_by_intent(self, mocker):
        db_responses = [{"_id": 1, "response_type": "IMAGE", "data": {"image_name": "image_1", "image_url": "image_url"}},
                        {"_id": 2, "response_type": "LINK", "data": {"link_name": "link_1", "url": "link_url_1"}},
                        {"_id": 3, "response_type": "LINK", "data": {"link_name": "link_2", "url": "link_url_2"}},
                        {"_id": 4, "response_type": "SUGGESTION", "data": {"suggestion_text": "sugg_1", "linked_to": "INTENT", "suggestion_intent": "intent_2"}},
                        {"_id": 5, "response_type": "TEXT", "data": {"fulfillment_text": "text_1"}}]
        expected = {"texts": [{"_id": 5, "fulfillment_text": "text_1"}],
                    "suggestions": [{"_id": 4, "suggestion_text": "sugg_1", "linked_to": "INTENT", "suggestion_intent": "intent_2"}],
                    "links": [{"_id": 2, "link_name": "link_1", "url": "link_url_1"}, {"_id": 3, "link_name": "link_2", "url": "link_url_2"}],
                    "images": [{"_id": 1, "image_name": "image_1", "image_url": "image_url"}]}
        mocker.patch("responses_service.ResponsesRepository.find_agent_responses_by_intent", return_value=db_responses)
        assert responses_service.ResponsesService.get_instance().get_agent_responses_by_intent("test1", "intent_1") == expected
