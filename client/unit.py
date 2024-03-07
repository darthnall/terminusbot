from vininfo import Vin

from auth import Searcher, Session


class Unit:
    def __init__(self, creds: dict, session: Session) -> None:
        self.search = Searcher(token=session.token)

        self._imei = creds["imei"]
        self._name = creds["assetName"]
        self._id = self.search.by_imei(creds["imei"])

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
