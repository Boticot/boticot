import pytest
import sys
sys.path.append(".")
import persistence.regex_repository as regex_repository


class TestRegexRepository:

    agent_name = "test1"
    data = ["data"]
    id = 3
    regex_repository = None

    @pytest.fixture(scope="function", autouse=True)
    def mock_functions(self, mocker):
        mocker.patch("persistence.regex_repository.mongo")
        mocker.patch("persistence.regex_repository.ObjectId")
        self.regex_repository = regex_repository.RegexRepository()

    def test_should_call_find_one_when_find_regex_is_called(self):
        self.regex_repository.find_regex(self.id)
        regex_repository.mongo.db.regex.find_one.assert_called()

    def test_should_call_find_when_find_agent_regex_is_called(self):
        self.regex_repository.find_agent_regex(self.agent_name)
        regex_repository.mongo.db.regex.find.assert_called()

    def test_should_return_true_when_insert_many_does_not_fail(self):
        assert self.regex_repository.insert_regex(self.data) == True

    def test_should_return_false_when_insert_many_fails(self, mocker):
        mocker.patch("persistence.regex_repository.mongo.db.regex.insert_many", side_effect=Exception("Mock error"))
        assert self.regex_repository.insert_regex(self.data) == False

    def test_should_call_delete_many_when_delete_agent_regex_is_called(self):
        self.regex_repository.delete_agent_regex(self.agent_name)
        regex_repository.mongo.db.regex.delete_many.assert_called()

    def test_should_return_true_when_delete_one_does_not_fail(self):
        assert self.regex_repository.delete_regex(self.agent_name, self.id) == True

    def test_should_return_false_when_delete_one_fails(self, mocker):
        mocker.patch("persistence.regex_repository.mongo.db.regex.delete_one", side_effect=Exception("Mock error"))
        assert self.regex_repository.delete_regex(self.agent_name, self.id) == False

    def test_should_return_true_when_update_one_does_not_fail(self):
        assert self.regex_repository.update_regex(self.agent_name, self.id, self.data) == True

    def test_should_return_false_when_update_one_fails(self, mocker):
        mocker.patch("persistence.regex_repository.mongo.db.regex.update_one", side_effect=Exception("Mock error"))
        assert self.regex_repository.update_regex(self.agent_name, self.id, self.data) == False

    def test_should_call_count_when_counting_agent_regex(self):
        self.regex_repository.count_agent_regex(self.agent_name)
        regex_repository.mongo.db.regex.count.assert_called()

    def test_should_call_find_when_getting_agent_regex(self):
        self.regex_repository.get_agent_regex(self.agent_name)
        regex_repository.mongo.db.regex.find.assert_called_with({"agent_name": self.agent_name}, {"agent_name": 0})
