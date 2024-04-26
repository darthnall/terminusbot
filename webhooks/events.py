from wialon import Wialon


class WialonEventListener:
    def __init__(self, token: str) -> None:
        self.wialon_api = Wialon()
        self._token = token

    def __enter__(self):
        login = self.wialon_api.token_login(token=self._token)
        self.wialon_api.sid = login["eid"]
        self._sid = login["eid"]

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.wialon_api.events_unload()
        self.wialon_api.core_logout()

        __err = f"{exc_type = }, {exc_val = }, {exc_tb = }"
        if exc_type is not None:
            return __err
        return None

    def get_events(self) -> dict:
        return self.wialon_api.avl_evts()

    def listen(self) -> dict:
        params = {
            "lang": "en",
            "measure": 1,
            "detalization": 20,
        }
        results = self.wialon_api.events_check_updates(**params)
        return results

    def get_units(self) -> list[str]:
        units = []
        params = {
            "spec": {
                "itemsType": "avl_unit",
                "propName": "sys_unique_id",
                "propValueMask": "*",
                "sortType": "sys_unique_id",
            },
            "force": 0,
            "flags": 9,
            "from": 0,
            "to": 0,
        }
        results = self.wialon_api.core_search_items(**params)

        for unit in results.get("items", []):
            if not unit.get("flds"):
                continue

            id = self.process_field(unit)
            if id is not None:
                units.append(id)

        return units

    def process_field(self, unit, attr: str = "to_number") -> str:
        id = None

        for field in unit.get("flds", {}).values():
            if field.get("n") == f"{attr}":
                id = unit["id"]

        return id

    def format_id(self, id: str) -> dict:
        return {"id": id, "detect": {"ignition,sensors":0}}

    def add_units_to_session(self, units: list[str]) -> None:
        params = {"mode": "add", "units": [self.format_id(unit) for unit in units]}
        self.wialon_api.events_update_units(**params)


class WialonEventHandler:
    def __init__(self, listener) -> None:
        self.listener = listener
        self._events = {}

    def __call__(self, events: dict) -> None:
        ids = set(events.keys())
        if ids:
            print(f"Events detected: {ids}")
            print(events)
        else:
            print("No events detected")
        for key, value in events.items():
            # Handle events
            pass

    def create_msg(self, data: dict) -> str:
        pass

    def get_number(self, id: str) -> str:
        num = None
        params = {
            "id": id,
            "flags": 9,
        }
        results = self.listener.wialon_api.core_search_item(**params)
        fields = results["item"]["flds"].items()

        for field in fields:
            field = field[1]
            if field.get("n") == "to_number":
                num = field.get("v")

        return num
