import os

from dotenv import load_dotenv

from . import Session


class Searcher(Session):
    def __init__(self) -> None:
        load_dotenv()
        token = os.environ["WIALON_HOSTING_API_TOKEN_DEV"]
        super().__init__(token=token)

    def __enter__(self):
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> str | None:
        super().__exit__(exc_type, exc_val, exc_tb)
        return None

    def by_imei(self, imei: str) -> int | None:
        """
        Search for an item by its IMEI number.

        Parameters
        ----------
        imei : str
            The IMEI number to search for.

        Returns
        -------
        int | None
            The ID of the item if found, otherwise None.
        """

        __id: int | None = None
        params = {
            "spec": {
                "itemsType": "avl_unit",
                "propName": "sys_unique_id,sys_id",
                "propValueMask": int(imei),
                "sortType": "sys_unique_id,sys_id",
            },
            "force": 1,
            "flags": 1,
            "from": 0,
            "to": 0,
        }

        response = self.wialon_api.core_search_items(**params)

        try:
            print(f"{response = }")

            for index, item in enumerate(response["items"]):
                print(f'{response["items"][index]["id"]}')
            __id = int(response["items"][0]["id"])
        except IndexError:
            print(f"IndexError: {response = }")
            __id = None

        return __id
