from enum import Enum
from .errors import PhoneNumberNotFoundError

class PhoneMessage(Enum):
    IGNITION_ON = "Hello! At {pos_time} your vehicle {unit} switched its ignition on near {location}."
    IGNITION_OFF = "Hello! At {pos_time} your vehicle {unit} switched its ignition off near {location}."
    IGNITION_TOGGLE = "Hello! At {pos_time} your vehicle {unit} switched its ignition state near {location}."

    GEOFENCE_ENTER = "Hello! At {pos_time} your vehicle {unit} was detected entering {geo_name} near {location}."
    GEOFENCE_EXIT = "Hello! At {pos_time} your vehicle {unit} was detected exiting {geo_name} near {location}."
    GEOFENCE_LEGAL = "Hello! At {pos_time} your vehicle {unit} was detected within {geo_name} near {location}."
    GEOFENCE_ILLEGAL = "Hello! At {pos_time} your vehicle {unit} was detected outside of {geo_name} near {location}."

    POSSIBLE_TOW = "Hello! At {pos_time} your vehicle {unit} was detected possibly in-tow near {location}."

    ERROR = "Hello! An error occured while attempting to dial '{to_number}', alert type: {alert_type}."

    def format_message(self, was_after_hours: bool = False, **kwargs) -> str:
        base_message = self.value.format(**kwargs)
        if was_after_hours:
            base_message += " This occured after hours."
        return base_message


def create_message(alert_type: str = None, data: dict = None) -> tuple:
    phone = data.get("to_number", None)
    after_hours = bool(data.get("after_hours", False))

    if phone is None:
        raise PhoneNumberNotFoundError("Phone number is not provided.")

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
        case _:
            msg = PhoneMessage.ERROR.format_message(after_hours, **data)

    return phone, msg
