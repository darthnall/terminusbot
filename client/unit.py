from vininfo import Vin

from auth import Searcher, Session


class Unit:
    def __init__(self, imei: str, name: str, session: Session) -> None:
        self.session = session
        search = Searcher(token=session._token)

        self._imei_number = int(imei)
        self._name = name
        self._id = search.by_imei(self.imei_number)

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
            1,  # View item and basic properties
            2,  # View detailed item properties
            16,  # Rename item
            256,  # Change icon
            4194304,  # Edit counters
            33554432,  # Register events
            268435456,  # View service intervals
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
