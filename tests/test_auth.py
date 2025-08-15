import requests
from configuration import SERVICE_URL
from src.enums.globals_enums import GlobalErrorMessages
from jsonschema import validate

from src.schemas.get import GET_DEMO_SLOT_ID_SCHEMA


def test_list_slots():
    response = requests.get(url = f'{SERVICE_URL}/slots?offset&limit&filterByProvider&sortBy')
    recieved_resp = response.json()

    assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
    assert recieved_resp['totalItems']['count'] > 0, GlobalErrorMessages.NO_SLOTS.value

    print(recieved_resp['totalItems']['count'])
    print(recieved_resp)

def test_get_demo_slot_id():
    response = requests.get(url = f'{SERVICE_URL}/slots/demo_slot/1')
    received_resp = response.json()

    assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
    assert set(received_resp.keys()) == {"code", "codeText", "status", "data"}, GlobalErrorMessages.WRONG_ELEMENT_COUNT.value
    validate(received_resp, GET_DEMO_SLOT_ID_SCHEMA)
    print(len(received_resp))
