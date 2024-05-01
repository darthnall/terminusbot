from twilio.rest import Client
from config import Config

class TwilioCaller:
    def __init__(self) -> None:
        self._token = Config.TWILIO_TOKEN
        self._sid = Config.TWILIO_SID
        self.client = Client(self._sid, self._token)

        return None

    def batch_send(self, to_number: list[str], msg: str) -> None:
        for phone in range(len(to_number)):
            self.send(phone, msg)

        return None

    def send(self, phone: str, msg: str) -> None:
        self.client.calls.create(
            twiml=f"<Response><Say>{msg}</Say></Response>",
            to=phone,
            from_="+18447682706",
        )

        return None
