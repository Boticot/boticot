import pytest
import sys
sys.path.append(".")
import persistence.users_inputs_repository as users_inputs_repository


class TestUsersInputsRepository:

    users_inputs_repository = None

    @pytest.fixture(scope="function", autouse=True)
    def mock_functions(self, mocker):
        mocker.patch("persistence.users_inputs_repository.mongo")
        self.users_inputs_repository = users_inputs_repository.UsersInputRepository()

    def test_should_call_aggregate_when_getting_agent_entities_count(self):
        self.users_inputs_repository.get_agent_entities_count("test1", "15-02-2022", "16-02-2022")
        aggregate_arguments = [{"$match": {"agent_name": "test1", "date": {"$gte": "15-02-2022", "$lt": "16-02-2022"}}},
                               {"$unwind": {"path": "$entities"}}, {"$group": {"_id": "$entities.entity", "count": {"$sum": 1}}}]
        users_inputs_repository.mongo.db.usersInputs.aggregate.assert_called_with(aggregate_arguments)
