import os
import sys
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from config import Config
from twilio.rest import Client
from .message import PhoneMessage


def create_message(alert_type: str, data: dict) -> tuple[str, str]:
    match alert_type:
        case "ignition_on":
            phone, msg = (
                data.get("to_number"),
                PhoneMessage.IGNITION_ON.format_message(**data),
            )

        case "ignition_off":
            phone, msg = (
                data.get("to_number"),
                PhoneMessage.IGNITION_OFF.format_message(**data),
            )

        case "ignition_toggle":
            phone, msg = (
                data.get("to_number"),
                PhoneMessage.IGNITION_TOGGLE.format_message(**data),
            )

        case "geofence_enter":
            phone, msg = (
                data.get("to_number"),
                PhoneMessage.GEOFENCE_ENTER.format_message(**data),
            )

        case "geofence_exit":
            phone, msg = (
                data.get("to_number"),
                PhoneMessage.GEOFENCE_EXIT.format_message(**data),
            )

        case "geofence_legal":
            phone, msg = (
                data.get("to_number"),
                PhoneMessage.GEOFENCE_LEGAL.format_message(**data),
            )

        case "geofence_illegal":
            phone, msg = (
                data.get("to_number"),
                PhoneMessage.GEOFENCE_ILLEGAL.format_message(**data),
            )

        case "passenger_detected":
            phone, msg = (
                data.get("to_number"),
                PhoneMessage.PASSENGER_DETECTED.format_message(**data),
            )

        case _:
            phone, msg = (
                None,
                PhoneMessage.ERROR.format_message(**data),
            )  # Logs error message and doesn't call

    return phone, msg


class TwilioCaller:
    def __init__(self) -> None:
        self._token = Config.TWILIO_TOKEN
        self._sid = Config.TWILIO_SID
        self.client = Client(self._sid, self._token)

    def send(self, to_number: str, msg: str) -> str:
        if not to_number:
            return "No phone number provided."
        return self.client.calls.create(
            twiml=f"<Response><Say>{msg}</Say></Response>",
            to=to_number,
            from_="+18447682706",
        )


if __name__ == "__main__":
    caller = TwilioCaller()
    data = {
        "to_number": "+17133049421",
        "pos_time": "2021-09-01 12:00:00",
        "unit": "123456",
        "location": "123 Main St",
        "geo_name": "Home",
    }
    phone, msg = create_message(alert_type="geofence_illegal", data=data)
    caller.send(phone, msg)
