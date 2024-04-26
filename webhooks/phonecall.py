import os
import sys
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from config import Config
from twilio.rest import Client


def create_message(alert_type: str, data) -> tuple[str, str]:
    match alert_type:
        case "ignition_on":
            phone, msg = (
                data.get("to_number"),
                f"Hello! At {data.get('pos_time')}, your vehicle {data.get('unit')} had its ignition turned on near {data.get('location')}.",
            )

        case "ignition_off":
            phone, msg = (
                data.get("to_number"),
                f"Hello! At {data.get('pos_time')}, your vehicle {data.get('unit')} had its ignition turned off near {data.get('location')}.",
            )

        case "ignition_toggle":
            phone, msg = (
                data.get("to_number"),
                f"Hello! At {data.get('pos_time')}, your vehicle {data.get('unit')} had its ignition state changed near {data.get('location')}.",
            )

        case "geofence_enter":
            phone, msg = (
                data.get("to_number"),
                f"Hello! At {data.get('pos_time')}, your vehicle {data.get('unit')} was detected entering {data.get('geo_name')} near {data.get('location')}.",
            )

        case "geofence_exit":
            phone, msg = (
                data.get("to_number"),
                f"Hello! At {data.get('pos_time')}, your vehicle {data.get('unit')} was detected exiting {data.get('geo_name')} near {data.get('location')}.",
            )

        case "geofence_legal":
            phone, msg = (
                data.get("to_number"),
                f"Hello! At {data.get('pos_time')}, your vehicle {data.get('unit')} was detected within {data.get('geo_name')} near {data.get('location')}.",
            )

        case "geofence_illegal":
            phone, msg = (
                data.get("to_number"),
                f"Hello! At {data.get('pos_time')}, your vehicle {data.get('unit')} was detected outside of {data.get('geo_name')} near {data.get('location')}.",
            )

        case _:
            phone, msg = (
                "+17133049421",
                "Alert handled improperly. Please check the logs.",
            )  # Calls Blake when alert_type is not recognized

    print(f"create_message: Calling {phone} with message: {msg}")

    return phone, msg


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
