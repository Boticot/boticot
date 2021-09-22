import pytest
import api.persistence.synonyms_repository as synonyms_repository


class TestSynonymsRepository:

    agent_name = "test1"
    data = ["data"]
    id = 3
    synonyms_repository = None

    @pytest.fixture(scope="function", autouse=True)
    def mock_functions(self, mocker):
        mocker.patch("api.persistence.synonyms_repository.mongo")
        self.synonyms_repository = synonyms_repository.SynonymsRepository()
        mocker.patch("api.persistence.synonyms_repository.ObjectId")

    def test_should_return_true_when_insert_many_does_not_fail(self):
        assert self.synonyms_repository.insert_synonyms(self.data) == True

    def test_should_return_false_when_insert_many_fails(self, mocker):
        mocker.patch("api.persistence.synonyms_repository.mongo.db.synonyms.insert_many", side_effect=Exception("Mock error"))
        assert self.synonyms_repository.insert_synonyms(self.data) == False

    def test_should_call_find_one_when_find_synonym_is_called(self):
        self.synonyms_repository.find_synonym(self.id)
        synonyms_repository.mongo.db.synonyms.find_one.assert_called()

    def test_should_call_delete_many_when_delete_agent_synonyms_is_called(self):
        self.synonyms_repository.delete_agent_synonyms(self.agent_name)
        synonyms_repository.mongo.db.synonyms.delete_many.assert_called()

    def test_should_return_true_when_delete_one_does_not_fail(self):
        assert self.synonyms_repository.delete_synonym(self.agent_name, self.id) == True

    def test_should_return_false_when_delete_one_fails(self, mocker):
        mocker.patch("api.persistence.synonyms_repository.mongo.db.synonyms.delete_one", side_effect=Exception("Mock error"))
        assert self.synonyms_repository.delete_synonym(self.agent_name, self.id) == False

    def test_should_return_true_when_update_one_does_not_fail(self):
        assert self.synonyms_repository.update_synonym(self.agent_name, self.id, self.data) == True

    def test_should_return_false_when_update_one_fails(self, mocker):
        mocker.patch("api.persistence.synonyms_repository.mongo.db.synonyms.update_one", side_effect=Exception("Mock error"))
        assert self.synonyms_repository.update_synonym(self.agent_name, self.id, self.data) == False
