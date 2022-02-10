import pytest
import sys
sys.path.append(".")
import analytics_service


class TestAnalyticsService:

    @pytest.fixture(scope="function", autouse=True)
    def mock_functions(self, mocker):
        mocker.patch("analytics_service.AnalyticsRepository.__init__", lambda x: None)

    def test_should_return_something_when_getting_analytics(self, mocker):
        mocker.patch("analytics_service.AnalyticsRepository.find_agent_analytics", return_value=[{"_id": 0, "agent_name": "test1", "analytic" : ["analytic1"]},
                                                                                              {"_id": 1, "agent_name": "test1", "analytic" : ["analytic2"]}])
        assert analytics_service.AnalyticsService.get_instance().get_analytics("test1", 30, None, None) == {"agent_name": "test1", "analytics": [{'analytic': ['analytic1']}, {'analytic': ['analytic2']}]}
