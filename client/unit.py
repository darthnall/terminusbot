from . import Session
from wialon import WialonError

class Unit(Session):
    def __init__(self, session, unit_id):
        self.session = session
        self._id = unit_id
        self.name = f'Unit-{self._id}'

    @property
    def id(self) -> int: return self._id

    @property
    def name(self) -> str: return self.name

    def assign(self, user) -> dict | bool:
        params = {
            "creatorId": user.id,
            "name": self.name,
            "hwTypeId": self.id,
            "dataFlags": 1
        }
        response = self.session.wialon_api.core_create_unit(**params)
        return response

    def unit_available(self) -> bool:
        params = {
            "spec": {
                "itemsType": "user",
                "propName": "sys_name",
                "propValueMask": f"*{self._id}*",
                "sortType": "sys_name"
            },
            "force": 1,
            "flags": 1,
            "from": 0,
            "to": 0
        }
        try:
            response = self.session.wialon_api.core_search_items(**params)
            self._id = response['item']
        except WialonError as e:
            print(f'Error code {e._code}, msg: {e._text}')
            return False
        return True
