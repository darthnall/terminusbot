from . import Session


class Search(Session):
    def __init__(self, session: Session):
        self.session = session

    def imei_to_id(self, imei: str) -> int | None:
        params = {
            "spec": {
                "itemsType": "avl_unit",
                "propName": "sys_unique_id,sys_id",
                "propValueMask": f"*{imei}*",
                "sortType": "sys_unique_id,sys_id",
            },
            "force": 1,
            "flags": 1,
            "from": 0,
            "to": 0,
        }

        response = self.session.wialon_api.core_search_items(**params)
        return int(response["items"][0]["id"])
