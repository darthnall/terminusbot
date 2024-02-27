from . import Session
from wialon import WialonError
from vininfo import Vin

class Unit(Session):
    def __init__(self, data, session):
        # Set session
        self.session = session

        # Define properties
        self._id = None
        self._name = data['assetName']
        self._vin = None

    def __repr__(self) -> str: return f"Unit({self.id}, {self.name}, {self.vin})"

    @property
    def id(self) -> int: return self._id

    @property
    def name(self) -> str: return self._name

    @property
    def vin(self): return self._vin

    def assign(self, user) -> dict | bool:
        if self._id is None:
            # Create unit
            params = {
                "creatorId": user.id,
                "name": self.name,
                "hwTypeId": "tracker",
                "dataFlags": 1
            }

            response = self.session.wialon_api.core_create_unit(**params)
            self._id = response['item']['id']

            if self.validate():
                return response
            else:
                return False
        else:
            return True

    def set_vin(self, vin: str | None) -> bool:
        self._vin = Vin(vin)
        if self.vin.verify_checksum():
            return True
        else:
            return False

    def validate(self) -> bool:
        params = {
            "spec": {
                "itemsType": "avl_unit",
                "propName": "name",
                "propValueMask": f"*{self.name}*",
                "sortType": "sys_name",
                "propType": ""
            },
            "force": 1,
            "flags": 1,
            "from": 0,
            "to": 0
        }
        response = self.session.wialon_api.core_search_items(**params)
        if response:
            return True
        return False
