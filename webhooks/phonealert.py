from twilio.rest import Client

from config import Config

from typing import Self

class WialonEventListener:
    def __init__(self, token: str) -> None:
        self._token = token

    def __enter__(self) -> Self:
        login = self.wialon_api.token_login(token=self._token)
        self.wialon_api.sid = login["eid"]
        self._sid = login["eid"]

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.wialon_api.core_logout()

        __err = f"{exc_type = }, {exc_val = }, {exc_tb = }"
        if exc_type is not None:
            return __err
        return None

    def format_id(self, id: str) -> dict:
        return {
            "id": id,
            "detect": {
                "*":0
            }
        }

    def add_units_to_session(self, units: list[dict]) -> None:
        params = {
            "mode": "add",
            "units": [self.format_id(unit) for unit in units]
        }
        self.wialon_api.events_update_units(**params)

class WialonEventHandler:
    def __init__(self) -> None:
        return None

    def create_message(self, event) -> str:
        match event:
            case ""


class TwilioCaller:
    def __init__(self) -> None:
        self._token = Config.TWILIO_TOKEN
        self._sid = Config.TWILIO_SID

        return None

    def __enter__(self) -> Self:
        self.client = Client(self._sid, self._token)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def call(self, to_number: str, msg: str) -> str:
        return self.client.calls.create(
            twiml=f"<Response><Say>{msg}</Say></Response>",
            to=to_number,
            from_="+18447682706",
        ).sid

if __name__ == "__main__":
    with TwilioCaller() as phone:
        phone.call("+17133049421", "Hello, this is a test call from TerminusGPS.")
