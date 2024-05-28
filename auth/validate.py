from typing import Callable, List, Tuple, Dict
from . import Searcher
import phonenumbers
from vininfo import Vin


class Validator:
    def __init__(
        self, target: str, validators: List[Callable[[str], Tuple[bool, str]]]
    ) -> None:
        self.target = target
        self.validators = validators
        self.results = self.validate()

    def validate(self) -> Dict[str, Dict[str, str]]:
        results = {}
        for validator in self.validators:
            is_valid, msg = validator(self.target)
            results[validator.__name__] = {"is_valid": is_valid, "msg": msg}
        return results

    def is_valid(self) -> bool:
        return all(result["is_valid"] for result in self.results.values())


def validate_is_digit(target: str) -> Tuple[bool, str]:
    is_valid, msg = True, "Good to go!"
    if not target.isdigit():
        is_valid, msg = False, "Must be digits only."
    return is_valid, msg


def validate_min_length(target: str, length: int = 4) -> Tuple[bool, str]:
    is_valid, msg = True, "Good to go!"
    if len(target) < length:
        is_valid, msg = False, f"Must be longer than {length} characters."
    return is_valid, msg


def validate_max_length(target: str, length: int = 64) -> Tuple[bool, str]:
    is_valid, msg = True, "Good to go!"
    if len(target) > length:
        is_valid, msg = False, f"Must be shorter than {length} characters."
    return is_valid, msg


def validate_vin(target) -> Tuple[bool, str]:
    is_valid, msg = True, "Good to go!"
    vin = Vin(target)
    return is_valid, msg


def validate_unit(target: str) -> Tuple[bool, str]:
    is_valid, msg = True, "Good to go!"
    searcher = Searcher()

    id = searcher.by_imei(target)
    if not id:
        is_valid, msg = False, "Unit not found."

    if not searcher.unit_is_available(target):
        is_valid, msg = False, "Unit is not available."

    return is_valid, msg


def validate_phone(target) -> Tuple[bool, str]:
    is_valid, msg = True, "Good to go!"
    try:
        num = phonenumbers.parse(target, None)

        if not phonenumbers.is_possible_number(num):
            is_valid, msg = False, "Unavailable phone number."

        if not phonenumbers.is_valid_number(num):
            is_valid, msg = False, "Invalid phone number."

    except phonenumbers.phonenumberutil.NumberParseException:
        is_valid, msg = False, "Invalid phone number."

    return is_valid, msg
