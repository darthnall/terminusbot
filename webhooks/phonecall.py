import os
import sys
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from config import Config
from twilio.rest import Client
from enum import Enum


class PhoneMessage(Enum):
    IGNITION_ON = "Hello! At {pos_time} your vehicle {unit} switched its ignition on near {location}."
    IGNITION_OFF = "Hello! At {pos_time} your vehicle {unit} switched its ignition off near {location}."
    IGNITION_TOGGLE = "Hello! At {pos_time} your vehicle {unit} switched its ignition state near {location}."

    GEOFENCE_ENTER = "Hello! At {pos_time} your vehicle {unit} was detected entering {geo_name} near {location}."
    GEOFENCE_EXIT = "Hello! At {pos_time} your vehicle {unit} was detected exiting {geo_name} near {location}."
    GEOFENCE_LEGAL = "Hello! At {pos_time} your vehicle {unit} was detected within {geo_name} near {location}."
    GEOFENCE_ILLEGAL = "Hello! At {pos_time} your vehicle {unit} was detected outside of {geo_name} near {location}."

    POSSIBLE_TOW = "Hello! At {pos_time} your vehicle {unit} was detected in-tow near {location}."

    ERROR = "Hello! An error occured while attempting to dial '{to_number}', alert type: {alert_type}."

    def format_message(self, after_hours=False, **kwargs) -> str:
        base_message = self.value.format(**kwargs)
        if after_hours:
            base_message += " This occured after hours."
        return base_message


def create_message(alert_type: str = None, data: dict = None) -> tuple:
    if data.get("phone", None) is None:
        raise ValueError("No phone number provided.")

    after_hours = bool(data.get("after_hours", False))

    match alert_type:
        case "ignition_on":
            msg = PhoneMessage.IGNITION_ON.format_message(after_hours, **data)
        case "ignition_off":
            msg = PhoneMessage.IGNITION_OFF.format_message(after_hours, **data)
        case "ignition_toggle":
            msg = PhoneMessage.IGNITION_TOGGLE.format_message(after_hours, **data)
        case "geofence_enter":
            msg = PhoneMessage.GEOFENCE_ENTER.format_message(after_hours, **data)
        case "geofence_exit":
            msg = PhoneMessage.GEOFENCE_EXIT.format_message(after_hours, **data)
        case "geofence_legal":
            msg = PhoneMessage.GEOFENCE_LEGAL.format_message(after_hours, **data)
        case "geofence_illegal":
            msg = PhoneMessage.GEOFENCE_ILLEGAL.format_message(after_hours, **data)
        case "possible_tow":
            msg = PhoneMessage.POSSIBLE_TOW.format_message(after_hours, **data)
        case None:
            msg = PhoneMessage.ERROR.format_message(after_hours, **data)
        case _:
            msg = PhoneMessage.ERROR.format_message(after_hours, **data)

    return phone, msg




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
