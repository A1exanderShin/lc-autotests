import requests
from src.utils.config import SERVICE_URL

from src.schemas.get import GET_DEMO_SLOT_ID_SCHEMA
from src.clients.base_client import Response

def test_list_slots():
    r = requests.get(url = f'{SERVICE_URL}/slots?offset&limit&filterByProvider&sortBy')
    response = Response(r)
    response.assert_slot_count(1)
    response.assert_status_code(200).validate_data(GET_DEMO_SLOT_ID_SCHEMA)
    #recieved_resp = response.json()
    #assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
    #assert recieved_resp['totalItems']['count'] > 0, GlobalErrorMessages.NO_SLOTS.value


def test_get_demo_slot_id():
    r = requests.get(url = f'{SERVICE_URL}/slots/demo_slot/1')
    response = Response(r)
    response.assert_status_code(200).validate_data(GET_DEMO_SLOT_ID_SCHEMA)

