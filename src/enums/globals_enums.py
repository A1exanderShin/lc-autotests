from enum import Enum

class GlobalErrorMessages(Enum):
    WRONG_STATUS_CODE = 'Статус-код отличается от ожидаемого'
    NO_SLOTS = 'Нет доступных слотов'
    WRONG_ELEMENT_COUNT = 'Кол-во элементов в ответе не соответствует ожидаемому'