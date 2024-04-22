import time
import os
import sys
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from config import Config
from .events import WialonEventHandler, WialonEventListener
from twilio.rest import Client
from auth import Session


class TwilioCaller:
    def __init__(self) -> None:
        self._token = Config.TWILIO_TOKEN
        self._sid = Config.TWILIO_SID
        self.client = Client(self._sid, self._token)

        return None

    def get_number(self, id: str) -> str:
        params = {
            "id": id,
            "flags": 0x10,
        }
        with Session() as session:
            results = session.wialon_api.core_search_item(**params)
            print(results)

    def send(self, to_number: str, msg: str) -> str:
        return self.client.calls.create(
            twiml=f"<Response><Say>{msg}</Say></Response>",
            to=to_number,
            from_="+18447682706",
        )


def start_loop():
    with WialonEventListener(token=Config.WIALON_HOSTING_API_TOKEN) as listener:
        caller = TwilioCaller()
        handler = WialonEventHandler(listener=listener)

        units = listener.get_units()
        listener.add_units_to_session(units)
        while True:
            events = listener.listen()
            handler(events)
            time.sleep(1.1)


if __name__ == "__main__":
    caller = TwilioCaller()
