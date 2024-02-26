from . import Session
from wialon import WialonError
from vininfo import Vin

class Unit(Session):
    def __init__(self, unit_id, session):
        # Set session
        self.session = session

        # Define properties
        self._id = unit_id
        self._name = user.creds['assetName']
        self._vin = None

    def __repr__(self) -> str: return f"Unit({self.id}, {self.name}, {self.vin})"

    @property
    def id(self) -> int: return self._id

    @property
    def name(self) -> str: return self._name

    @property
    def vin(self): return self._vin

    def assign(self, user) -> dict | bool:
        # Create unit
        params = {
            "creatorId": user.id,
            "name": self.name,
            "hwTypeId": self.id,
            "dataFlags": 1
        }
        response = self.session.wialon_api.core_create_unit(**params)
        return response

    def set_vin(self, vin: str | None) -> bool:
        self._vin = Vin(vin)
        if self.vin.verify_checksum():
            return True
        else:
            return False
