from . import Session


class Searcher():
    def __init__(self, session: Session):
        self.session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"exc_type: {exc_type}, exc_val: {exc_val}, exc_tb: {exc_tb}")
            return False
        return True

    def imei_to_id(self, imei: str) -> int | None:
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

        response = self.session.wialon_api.core_search_items(**params)
        try:
            return int(response["items"][0]["id"])
        except IndexError:
            return None
