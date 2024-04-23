import os
import sys
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from config import Config
from twilio.rest import Client

def create_message(data: dict) -> tuple[str, str]:
    return data["to_number"], f"Hello! Your vehicle {data['unit']} changed its ignition state at {data['msg_time']}."


class TwilioCaller:
    def __init__(self) -> None:
        self._token = Config.TWILIO_TOKEN
        self._sid = Config.TWILIO_SID
        self.client = Client(self._sid, self._token)

        return None

    def send(self, to_number: str, msg: str) -> str:
        return self.client.calls.create(
            twiml=f"<Response><Say>{msg}</Say></Response>",
            to=to_number,
            from_="+18447682706",
        )


if __name__ == "__main__":
    caller = TwilioCaller()
