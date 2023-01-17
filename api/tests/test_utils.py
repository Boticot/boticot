import sys
sys.path.append(".")
import utils


def test_should_return_a_date_when_giving_a_string():
    assert utils.string_to_date("08-02-2022") == utils.datetime.strptime("08-02-2022", "%d-%m-%Y")


def test_should_fail_when_date_format_is_not_valid():
    assert utils.string_to_date("08/02/2022") is None
