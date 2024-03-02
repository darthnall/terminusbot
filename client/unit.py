from vininfo import Vin

from auth import Search, Session
from wialon import WialonError


class Unit():
    def __init__(self, creds: dict, session: Session):
        self.session = session

        search = Search(self.session)
        self._imei = creds["imei"]
        if search.imei_to_id(self._imei):
            self._id = search.imei_to_id(self._imei)
        else:
            self._id = None

        self._name = creds["assetName"]

    def __repr__(self) -> str:
        return f"{self = }"

    @property
    def id(self) -> int | None:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    def assign(self, user_id: str) -> dict:
        flags = [
            1,  # View item and basic properties
            2,  # View detailed item properties
            16,  # Rename item
            256,  # Change icon
            4194304,  # Edit counters
            33554432,  # Register events
            268435456,  # View service intervals
            # 0x0400000000, # View commands
            # 0x8000000000,  # Use unit in jobs, notifications, routes, retranslators
        ]

        params = {"userId": user_id, "itemId": self.id, "accessMask": sum(flags)}

        response = self.session.wialon_api.user_update_item_access(**params)
        if self.rename():
            print(f"Unit renamed successfully to {self.name}")
        return response

    def rename(self) -> bool:
        params = {"itemId": self.id, "name": self.name}
        response = self.session.wialon_api.item_update_name(**params)
        if response["nm"] == self.name:
            return True
        return False
