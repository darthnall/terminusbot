from vininfo import Vin

from auth import Searcher, Session


class Unit:
    def __init__(self, imei: str, name: str, session: Session) -> None:
        self.session = session
        search = Searcher(token=session._token)

        self._imei_number = int(imei)
        self._name = name
        self._id = search.by_imei(self._imei_number)

    def __repr__(self) -> str:
        return f"{self = }"

    @property
    def id(self) -> int | None:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def imei_number(self) -> int:
        return self._imei_number

    def assign(self, user_id: str) -> dict:
        flags = [
            0x0001,  # View item and its basic properties
            0x0002,  # View detailed item properties
            0x0004,  # Manage access to this item
            0x0010,  # Rename item
            0x0020,  # View custom fields
            0x0100,  # Change icon
            0x4000,  # View attached files
        ]

        params = {"userId": user_id, "itemId": self.id, "accessMask": sum(flags)}

        response = self.session.wialon_api.user_update_item_access(**params)
        if self.rename():
            print(f"Unit renamed successfully to {self.name}")
        return response

    def rename(self) -> bool:
        params = {"itemId": self.id, "name": self.name}

        response = self.session.wialon_api.item_update_name(**params)
        return response["nm"] == self.name
