import pytest
import sys
sys.path.append(".")
import synonyms_service


class TestAgentsService:

    agent_name = "test1"
    id = 3
    synonym = "good"

    @pytest.fixture(scope="function", autouse=True)
    def mock_functions(self, mocker):
        mock_list = ["AgentsRepository.agent_modified"]
        for mock in mock_list:
            mocker.patch("synonyms_service.{}".format(mock))
        mocker.patch("synonyms_service.SynonymsRepository.__init__", lambda x: None)
        mocker.patch("synonyms_service.AgentsRepository.__init__", lambda x: None)

    def test_should_call_agent_modified_when_delete_synonym_returns_true(self, mocker):
        mocker.patch("synonyms_service.SynonymsRepository.delete_synonym", return_value=True)
        synonyms_service.SynonymsService.get_instance().delete_agent_synonym(self.agent_name, self.id)
        synonyms_service.AgentsRepository.agent_modified.assert_called()

    def test_should_not_call_agent_modified_when_delete_synonym_returns_false(self, mocker):
        mocker.patch("synonyms_service.SynonymsRepository.delete_synonym", return_value=False)
        synonyms_service.SynonymsService.get_instance().delete_agent_synonym(self.agent_name, self.id)
        synonyms_service.AgentsRepository.agent_modified.assert_not_called()

    def test_should_call_agent_modified_when_update_synonym_returns_true(self, mocker):
        mocker.patch("synonyms_service.SynonymsRepository.update_synonym", return_value=True)
        synonyms_service.SynonymsService.get_instance().update_agent_synonym(self.agent_name, self.id, self.synonym)
        synonyms_service.AgentsRepository.agent_modified.assert_called()

    def test_should_not_call_agent_modified_when_update_synonym_returns_false(self, mocker):
        mocker.patch("synonyms_service.SynonymsRepository.update_synonym", return_value=False)
        synonyms_service.SynonymsService.get_instance().update_agent_synonym(self.agent_name, self.id, self.synonym)
        synonyms_service.AgentsRepository.agent_modified.assert_not_called()

    def test_should_synonym_exist_when_find_synonym_returns_something(self, mocker):
        mocker.patch("synonyms_service.ObjectId.is_valid", return_value=True)
        mocker.patch("synonyms_service.SynonymsRepository.find_synonym", return_value="synonym")
        assert synonyms_service.SynonymsService.get_instance().synonym_exist(self.id) == True

    def test_should_synonym_not_exist_when_find_synonym_returns_none(self, mocker):
        mocker.patch("synonyms_service.ObjectId.is_valid", return_value=True)
        mocker.patch("synonyms_service.SynonymsRepository.find_synonym", return_value=None)
        assert synonyms_service.SynonymsService.get_instance().synonym_exist(self.id) == False

    def test_should_synonym_not_exist_when_id_is_not_valid(self, mocker):
        mocker.patch("synonyms_service.ObjectId.is_valid", return_value=False)
        mocker.patch("synonyms_service.SynonymsRepository.find_synonym", return_value="synonym")
        assert synonyms_service.SynonymsService.get_instance().synonym_exist(self.id) == False
