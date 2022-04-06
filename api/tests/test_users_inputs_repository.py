import pytest
import sys
sys.path.append(".")
import persistence.users_inputs_repository as users_inputs_repository


class TestUsersInputsRepository:

    users_inputs_repository = None

    @pytest.fixture(scope="function", autouse=True)
    def mock_functions(self, mocker):
        mocker.patch("persistence.users_inputs_repository.mongo")
        self.users_inputs_repository = users_inputs_repository.UsersInputsRepository()

    def test_should_call_find_when_getting_agent_inputs(self):
        self.users_inputs_repository.get_agent_inputs("test1", None, None, 1, 0, 1, 20)
        self.users_inputs_repository.users_inputs_collection.find.assert_called_with({"agent_name": "test1", "intent.confidence": {"$lte": 1, "$gte": 0}}, {"agent_name": 0})

    def test_should_call_find_when_getting_agent_inputs_by_intent(self):
        self.users_inputs_repository.get_agent_inputs("test1", "greetings_hello", None, 1, 0, 1, 20)
        self.users_inputs_repository.users_inputs_collection.find.assert_called_with({"agent_name": "test1", "intent.confidence": {"$lte": 1, "$gte": 0}, "intent.name": "greetings_hello"}, {"agent_name": 0})

    def test_should_call_find_when_getting_agent_inputs_by_text(self):
        self.users_inputs_repository.get_agent_inputs("test1", None, "text", 1, 0, 1, 20)
        self.users_inputs_repository.users_inputs_collection.find.assert_called_with({"agent_name": "test1", "intent.confidence": {"$lte": 1, "$gte": 0}, "text": {"$regex": ".*" + "text" + ".*", "$options" : "-i"}}, {"agent_name": 0})

    def test_should_call_find_when_getting_agent_inputs_by_intent_and_by_text(self):
        self.users_inputs_repository.get_agent_inputs("test1", "greetings_hello", "text", 1, 0, 1, 20)
        self.users_inputs_repository.users_inputs_collection.find.assert_called_with({"agent_name": "test1", "intent.confidence": {"$lte": 1, "$gte": 0}, "intent.name": "greetings_hello", "text": {"$regex": ".*" + "text" + ".*", "$options" : "-i"}}, {"agent_name": 0})

    def test_should_call_count_when_counting_user_inputs(self):
        self.users_inputs_repository.count_user_inputs("test1", None, None)
        self.users_inputs_repository.users_inputs_collection.count.assert_called_with({"agent_name": "test1"})

    def test_should_call_count_when_counting_user_inputs_by_intent(self):
        self.users_inputs_repository.count_user_inputs("test1", "greetings_hello", None)
        self.users_inputs_repository.users_inputs_collection.count.assert_called_with({"agent_name": "test1", "intent.name": "greetings_hello"})

    def test_should_call_count_when_counting_user_inputs_by_text(self):
        self.users_inputs_repository.count_user_inputs("test1", None, "text")
        self.users_inputs_repository.users_inputs_collection.count.assert_called_with({"agent_name": "test1", "text": {"$regex": ".*" + "text" + ".*", "$options": "-i"}})

    def test_should_call_count_when_counting_user_inputs_by_intent_and_by_text(self):
        self.users_inputs_repository.count_user_inputs("test1", "greetings_hello", "text")
        self.users_inputs_repository.users_inputs_collection.count.assert_called_with({"agent_name": "test1", "intent.name": "greetings_hello", "text": {"$regex": ".*" + "text" + ".*", "$options" : "-i"}})
