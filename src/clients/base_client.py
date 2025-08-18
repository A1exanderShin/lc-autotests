from jsonschema import validate
from src.enums.globals_enums import GlobalErrorMessages

class Response:

    def __init__(self, response):
        self.response = response
        self.response_json = response.json()
        self.response_status = response.status_code

    def validate_data(self, schema):
        data = self.response_json
        if isinstance(data, list):
            for item in data:
                validate(item, schema)
        else:
            validate(data, schema)
        return self

    def assert_status_code(self, status_code):
        if isinstance(status_code, list):
            assert self.response_status in status_code, GlobalErrorMessages.WRONG_STATUS_CODE.value
        else:
            assert self.response_status == status_code, GlobalErrorMessages.WRONG_STATUS_CODE.value
        return self

    def assert_slot_count(self, min_count = 1):
        assert self.response_json['totalItems']['count'] >= min_count, GlobalErrorMessages.NO_SLOTS.value
        return self
