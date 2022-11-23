import sys
sys.path.append(".")
import security_decorator


def test_should_return_true_when_client_is_valid(mocker):
    mocker.patch("security_decorator.os")
    mocker.patch("security_decorator.json.loads", return_value={"my_client_id": "my_client_secret_key"})
    assert security_decorator.check_client("my_client_id", "my_client_secret_key") == True


def test_should_return_false_when_client_is_invalid(mocker):
    mocker.patch("security_decorator.os")
    mocker.patch("security_decorator.json.loads", return_value={"my_client_id": "my_client_secret_key"})
    assert security_decorator.check_client("my_client_i", "my_client_secret_key") == False


def test_should_succeed_when_client_credentials_are_valid(mocker):
    mocker.patch("security_decorator.request")
    mocker.patch("security_decorator.check_client", return_value=True)
    @security_decorator.api_auth_required
    def to_be_decorated():
        return True
    assert to_be_decorated() == True


def test_should_fail_when_client_credentials_are_not_valid(mocker):
    mocker.patch("security_decorator.request", return_value=None)
    mocker.patch("security_decorator.check_client", return_value=False)
    mocker.patch("security_decorator.response_template", return_value={401, "Not authorized, client id or client secret key is invalid"})
    @security_decorator.api_auth_required
    def to_be_decorated():
        return True
    assert to_be_decorated() == {401, "Not authorized, client id or client secret key is invalid"}


def test_should_fail_when_client_credentials_are_missing(mocker):
    request_mock = mocker.patch("security_decorator.request")
    request_mock.headers.get.return_value = None
    mocker.patch("security_decorator.response_template", return_value={400, "Missing client id or client secret key"})
    @security_decorator.api_auth_required
    def to_be_decorated():
        return True
    assert to_be_decorated() == {400, "Missing client id or client secret key"}
