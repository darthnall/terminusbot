from . import Searcher, Session

from client.form import Field

def init_validation(target: str | None) -> tuple[bool, str]:
    return False, f"Invalid input: {target}"

class Validator:
    def __init__(self, token: str) -> None:
        self._token = token

    def _has_banned_character(self, target: str) -> bool:
        has_banned_character = False
        banned_characters = ["*"]

        match target:
            case target if any(char in target for char in banned_characters):
                has_banned_character = True

        return has_banned_character

    def validate_all(self, form: dict[str, Field]) -> dict[str, Field]:
        for id, field in form.items():
            valid, msg = False, f"Invalid input {field.user_input}"
            if id == "firstName":
                valid, msg = self.validate_name(target=field.user_input)
            if id == "lastName":
                valid, msg = self.validate_name(target=field.user_input)
            if id == "email":
                valid, msg = self.validate_email(target=field.user_input)
            if id == "assetName":
                valid, msg = self.validate_asset_name(target=field.user_input)
            if id == "imeiNumber":
                valid, msg = self.validate_imei_number(target=field.user_input)
            if id == "phoneNumber":
                valid, msg = self.validate_phone_number(target=field.user_input)
            if id == "vinNumber":
                valid, msg = self.validate_vin_number(target=field.user_input)
            field.validation_result = valid
            field.validation_msg = msg

        return form

    def validate_name(self, target: str | None) -> tuple[bool, str]:
        _valid, msg = init_validation(target=target)

        match target:
            case "" | None:
                _valid, msg = False, "Please input a name."
            case target if self._has_banned_character(target=target) == True:
                _valid, msg = False, f"Name contains invalid character."
            case target if not target.lower().isalpha():
                _valid, msg = False, "Name can only contain letters."
            case target if target.lower().isalpha():
                _valid, msg = True, "Looks good!"

        return _valid, msg

    def validate_asset_name(self, target: str | None) -> tuple[bool, str]:
        _valid, msg = init_validation(target=target)

        match target:
            case "" | None:
                _valid, msg = False, "Please input a name for your new asset."
            case target if len(target) > 60:
                _valid, msg = False, f"Name must be under 60 characters. Input was {len(target)} characters."
            case target if self._has_banned_character(target=target) == True:
                _valid, msg = False, f"Name contains invalid character."
            case target if len(target) <= 60 and target != "" and target is not None:
                _valid, msg = True, "Looks good!"

        return _valid, msg

    def validate_email(self, target: str | None) -> tuple[bool, str]:
        _valid, msg = init_validation(target=target)

        valid_endings: tuple = (
            ".com",
            ".net",
            ".edu",
            ".org",
            ".gov",
            ".me",
            ".io",
        )

        match target:
            case "" | None:
                _valid, msg = False, "Please input your email address."
            case target if len(target) > 60:
                _valid, msg = False, f"Email must be less than 60 characters. Length: {len(target)}"
            case target if len(target) <= 60 and target != "" and target is not None:
                addr = target.split("@")
                if addr[1].endswith(valid_endings):
                    _valid, msg = True, "Looks good!"
                else:
                    _valid, msg = False, f"Email must contain a valid domain. Valid domains: {valid_endings}"

        return _valid, msg

    def validate_phone_number(self, target: str | None) -> tuple[bool, str]:
        _valid, msg = init_validation(target=target)

        match target:
            case "" | None:
                _valid, msg = False, "Please input a phone number."
            case target if target.isdigit() is False:
                _valid, msg = False, f"Phone # must be digits only."
            case target if len(target) > 15:
                _valid, msg = False, f"Phone number must be less than 15 characters. Length: {len(target)}"
            case target if len(target) <= 15 and target != "" and target is not None:
                _valid, msg = True, "Looks good!"

        return _valid, msg

    def validate_imei_number(self, target: str | None) -> tuple[bool, str]:
        _valid, msg = init_validation(target=target)

        match target:
            case "" | None:
                _valid, msg = False, "Please input your IMEI #."
            case target if target.isdigit() is False:
                _valid, msg = False, f"IMEI # must be digits only."
            case target if len(target) != 15:
                _valid, msg = False, f"IMEI # must be exactly 15 characters. Length: {len(target)}"
            case target if len(target) == 15 and target != "" and target is not None:
                search = Searcher(token=self._token)
                if search.unit_was_previously_assigned(imei=target):
                    _valid, msg = False, "Invalid unit. support@terminusgps.com has been notified of this error."
                    # TODO: Email myself this error.
                    if search.by_imei(imei=target):
                        _valid, msg = True, "Looks good!"
                else:
                    _valid, msg = False, "Couldn't find associated unit. Try again or call if issue persists."

        return _valid, msg

    def validate_vin_number(self, target: str | None) -> tuple[bool, str]:
        _valid, msg = init_validation(target=target)
        _valid, msg = True, "Looks good!"
        return _valid, msg
