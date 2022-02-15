import pytest
import sys
sys.path.append(".")
import analytics_service
from datetime import datetime


class TestAnalyticsService:

    @pytest.fixture(scope="function", autouse=True)
    def mock_functions(self, mocker):
        mocker.patch("analytics_service.AgentsRepository.__init__", lambda x: None)
        mocker.patch("analytics_service.UsersInputRepository.__init__", lambda x: None)
        mocker.patch("analytics_service.AnalyticsRepository.__init__", lambda x: None)

    def test_should_call_insert_analytics_when_storing_agent_analytics(self, mocker):
        mocker.patch("analytics_service.AnalyticsRepository.insert_analytics")
        mocker.patch("analytics_service.AnalyticsService.exist_agent_analytics", return_value=False)
        mocker.patch("analytics_service.UsersInputRepository.get_agent_unique_users_count", return_value=["user1"])
        mocker.patch("analytics_service.UsersInputRepository.get_agent_traffic", return_value=3)
        mocker.patch("analytics_service.UsersInputRepository.get_agent_intent_count", side_effect=[2, 3])
        mocker.patch("analytics_service.UsersInputRepository.get_agent_entities_count", return_value=[{"_id": "zip_code", "count": 1}, {"_id": "city", "count": 2}])
        analytics_service.AnalyticsService.get_instance().store_agent_analytics("test1", ["greetings_hello", "order"], datetime.today())
        analytics_service.AnalyticsRepository.insert_analytics.assert_called_with({
                "agent_name": "test1",
                "date": datetime.combine(datetime.today(), datetime.min.time()),
                "traffic": 3,
                "unique_users": 1,
                "intents_count": [{"intent" : "greetings_hello", "count": 2}, {"intent" : "order", "count": 3}],
                "entities_count":[{"entity" : "zip_code", "count": 1}, {"entity" : "city", "count": 2}]
            })
