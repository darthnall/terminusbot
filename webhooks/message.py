from enum import Enum


class PhoneMessage(Enum):
    IGNITION_ON = "Hello! At {pos_time} your vehicle {unit} switched its ignition on near {location}."
    IGNITION_OFF = "Hello! At {pos_time} your vehicle {unit} switched its ignition off near {location}."
    IGNITION_TOGGLE = "Hello! At {pos_time} your vehicle {unit} switched its ignition state near {location}."

    GEOFENCE_ENTER = "Hello! At {pos_time} your vehicle {unit} was detected entering {geo_name} near {location}."
    GEOFENCE_EXIT = "Hello! At {pos_time} your vehicle {unit} was detected exiting {geo_name} near {location}."
    GEOFENCE_LEGAL = "Hello! At {pos_time} your vehicle {unit} was detected within {geo_name} near {location}."
    GEOFENCE_ILLEGAL = "Hello! At {pos_time} your vehicle {unit} was detected outside of {geo_name} near {location}."

    def format_message(self, **kwargs) -> str:
        return self.value.format(**kwargs)
