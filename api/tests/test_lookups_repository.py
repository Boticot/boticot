import pytest
import sys
sys.path.append(".")
import persistence.lookups_repository as lookups_repository


class TestLookupsRepository:

    agent_name = "test1"
    lookup_name = "city"
    data = ["data"]
    lookups_repository = None

    @pytest.fixture(scope="function", autouse=True)
    def mock_functions(self, mocker):
        mocker.patch("persistence.lookups_repository.mongo")
        self.lookups_repository = lookups_repository.LookupsRepository()

    def test_should_call_find_when_finding_agent_lookups(self):
        self.lookups_repository.find_agent_lookups(self.agent_name)
        lookups_repository.mongo.db.lookup.find.assert_called()

    def test_should_call_find_when_finding_lookup(self):
        self.lookups_repository.find_lookup(self.agent_name, self.lookup_name)
        lookups_repository.mongo.db.lookup.find.assert_called_with({'agent_name': self.agent_name, 'lookups.name': self.lookup_name})

    def test_should_insert_lookups_when_insert_many_does_not_fail(self):
        assert self.lookups_repository.insert_lookups(self.data) == True

    def test_should_not_insert_lookups_when_insert_many_fails(self, mocker):
        mocker.patch("persistence.lookups_repository.mongo.db.lookup.insert_many", side_effect=Exception("Mock error"))
        assert self.lookups_repository.insert_lookups(self.data) == False

    def test_should_call_delete_many_when_deleting_agent_lookups(self):
        self.lookups_repository.delete_agent_lookups(self.agent_name)
        lookups_repository.mongo.db.lookup.delete_many.assert_called()

    def test_should_delete_lookup_when_delete_many_does_not_fail(self):
        assert self.lookups_repository.delete_lookup(self.agent_name, self.lookup_name) == True

    def test_should_not_delete_lookup_when_delete_many_fails(self, mocker):
        mocker.patch("persistence.lookups_repository.mongo.db.lookup.delete_many", side_effect=Exception("Mock error"))
        assert self.lookups_repository.delete_lookup(self.agent_name, self.lookup_name) == False

    def test_should_call_count_when_counting_agent_lookups(self):
        self.lookups_repository.count_agent_lookups(self.agent_name)
        lookups_repository.mongo.db.lookup.count.assert_called()

    def test_should_call_find_when_getting_agent_lookups(self):
        self.lookups_repository.get_agent_lookups(self.agent_name)
        lookups_repository.mongo.db.lookup.find.assert_called_with({"agent_name": self.agent_name}, {"agent_name": 0})
