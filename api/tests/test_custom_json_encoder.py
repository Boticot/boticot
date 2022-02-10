import sys
sys.path.append(".")
import custom_json_encoder
from datetime import datetime


class TestCustomJSONEncoder:

    def test_should_call_http_date_when_giving_datetime(self, mocker):
        mocker.patch("custom_json_encoder.http_date")
        custom_json_encoder.CustomJSONEncoder().custom_default(datetime(2022, 4, 22, 0, 0, 0, 0))
        custom_json_encoder.http_date.assert_called()

    def test_should_call_json_encoder_default_when_not_giving_datetime(self, mocker):
        mocker.patch("custom_json_encoder.JSONEncoder.default")
        custom_json_encoder.CustomJSONEncoder().custom_default("string")
        custom_json_encoder.JSONEncoder.default.assert_called()
