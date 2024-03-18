from . import Session
from config import Config

from functools import cache


class Searcher:
    """
    Search the Wialon database via the Wialon API.
    """

    def __init__(self) -> None:
        self._token = Config.WIALON_HOSTING_API_TOKEN

    def search(self, params: dict, session: Session) -> dict:
        return session.wialon_api.core_search_items(**params)

    def by_imei(self, imei: int) -> int | None:
        """
        Search for an item by its IMEI number.

        Parameters
        ----------
        imei: <int>
            The IMEI number to search for.

        Returns
        -------
        __id: <int | None>
            The ID of the item if found, otherwise None.
        """
        __id: int | None = None

        params = {
            "spec": {
                "itemsType": "avl_unit",
                "propName": "sys_unique_id",
                "propValueMask": imei,
                "sortType": "sys_unique_id",
            },
            "force": 1,
            "flags": 1,
            "from": 0,
            "to": 0,
        }

        # Open a session and search for the item
        with Session() as session:
            response = self.search(params=params, session=session)
            __id = int(response["items"][0]["id"])

        return __id

    @cache
    def unit_is_available(self, imei: str) -> bool:
        unit_is_available = False
        params = {
            "spec": {
                "itemsType": "avl_unit",
                "propName": "sys_name",
                "propValueMask": imei,
                "sortType": "sys_name",
            },
            "force": 1,
            "flags": 1,
            "from": 0,
            "to": 0,
        }
        with Session() as session:
            # TODO: Simplify this logic
            response = self.search(params=params, session=session)
            if response["totalItemsCount"] == 0:
                unit_is_available = False
            elif response["items"][0]["nm"] == imei:
                unit_is_available = True
            else:
                unit_is_available = False

        return unit_is_available
