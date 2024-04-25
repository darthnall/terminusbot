import os
import sys
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from config import Config
from twilio.rest import Client

def create_message(alert_type: str, args: dict) -> tuple[str, str]:
    match alert_type:
        case "ignition_on":
            phone, msg = args["to_number"], f"Hello! At {args['pos_time']}, your vehicle {args['unit']} had its ignition turned on near {args['loc']}."

        case "ignition_off":
            phone, msg = args["to_number"], f"Hello! At {args['pos_time']}, your vehicle {args['unit']} had its ignition turned off near {args['loc']}."

        case "ignition_toggle":
            phone, msg = args["to_number"], f"Hello! At {args['pos_time']}, your vehicle {args['unit']} had its ignition state changed near {args['loc']}."

        case "geofence_enter":
            phone, msg = args["to_number"], f"Hello! At {args['pos_time']}, your vehicle {args['unit']} was detected entering {args['geo_name']} near {args['loc']}."

        case "geofence_exit":
            phone, msg = args["to_number"], f"Hello! At {args['pos_time']}, your vehicle {args['unit']} was detected exiting {args['geo_name']} near {args['loc']}."

        case "geofence_legal":
            phone, msg = args["to_number"], f"Hello! At {args['pos_time']}, your vehicle {args['unit']} was detected inside of {args['geo_name']} near {args['loc']}."

        case "geofence_illegal":
            phone, msg = args["to_number"], f"Hello! At {args['pos_time']}, your vehicle {args['unit']} was detected outside of {args['geo_name']} near {args['loc']}."

        case _:
            phone, msg = "+17133049421", "Alert handled improperly. Please check the logs." # Calls Blake when alert_type is not recognized

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
