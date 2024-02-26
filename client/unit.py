from . import Session
from wialon import WialonError
from vininfo import Vin

class Unit(Session):
    def __init__(self, unit_id, user, session):
        # Set session
        self.session = session

        # Define properties
        self._id = unit_id
        self._name = user.creds['assetName']
        self._vin = None

    @property
    def id(self) -> int: return self._id
    @property
    def name(self) -> str: return self._name
    @property
    def vin(self) -> str: return self._vin

    def assign(self) -> dict | bool:
        params = {
            "creatorId": self.user.id,
            "name": self.name,
            "hwTypeId": self.id,
            "dataFlags": 1
        }
        response = self.session.wialon_api.core_create_unit(**params)
        return response

    def set_vin(self, _vin: str) -> bool:
        self.vin = Vin(_vin)
        if self.vin.verify_checksum():
            return True
        else:
            return False
