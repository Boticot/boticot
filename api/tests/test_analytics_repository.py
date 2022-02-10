import pytest
import sys
sys.path.append(".")
import persistence.analytics_repository as analytics_repository
from utils import string_to_date


class TestAnalyticsRepository:

    analytics_repository = None

    @pytest.fixture(scope="function", autouse=True)
    def mock_functions(self, mocker):
        mocker.patch("persistence.analytics_repository.mongo")
        self.analytics_repository = analytics_repository.AnalyticsRepository()

    def test_should_call_find_when_getting_analytics(self):
        self.analytics_repository.find_agent_analytics("test1", 30, None, None)
        self.analytics_repository.analytics_repository.find.assert_called_with({"agent_name": "test1"})

    def test_should_call_find_when_getting_analytics_from_such_date(self):
        self.analytics_repository.find_agent_analytics("test1", 30, string_to_date("05-02-2022"), None)
        self.analytics_repository.analytics_repository.find.assert_called_with({"agent_name": "test1", "date": {"$gte": string_to_date("05-02-2022")}})

    def test_should_call_find_when_getting_analytics_until_such_date(self):
        self.analytics_repository.find_agent_analytics("test1", 30, None, string_to_date("07-02-2022"))
        self.analytics_repository.analytics_repository.find.assert_called_with({"agent_name": "test1", "date": {"$lte": string_to_date("07-02-2022")}})

    def test_should_call_find_when_getting_analytics_for_a_period(self):
        self.analytics_repository.find_agent_analytics("test1", 30, string_to_date("05-02-2022"), string_to_date("07-02-2022"))
        self.analytics_repository.analytics_repository.find.assert_called_with({"agent_name": "test1", "date": {"$gte": string_to_date("05-02-2022"), "$lte": string_to_date("07-02-2022")}})
