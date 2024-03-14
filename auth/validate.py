from . import Searcher

import asyncio

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

    async def validate_all(self, data: dict[str, str]) -> list[str | None]:
        tasks = [
            asyncio.create_task(self.validate_name(target=data["firstName"])),
            asyncio.create_task(self.validate_name(target=data["lastName"])),
            asyncio.create_task(self.validate_email(target=data["email"])),
            asyncio.create_task(self.validate_asset_name(target=data["assetName"])),
            asyncio.create_task(self.validate_imei_number(target=data["imeiNumber"])),
            asyncio.create_task(self.validate_phone_number(target=data["phoneNumber"])),
            asyncio.create_task(self.validate_vin_number(target=data["vinNumber"])),
        ]
        results = await asyncio.gather(*tasks)
        return [result[1] for result in results if result[0] is False]

    async def validate_name(self, target: str | None) -> tuple[bool, str]:
        _valid, msg = init_validation(target=target)

        match target:
            case "" | None:
                _valid, msg = False, "Please input a name."
            case target if self._has_banned_character(target=target):
                _valid, msg = False, "Name contains invalid character."
            case target if not target.lower().isalpha():
                _valid, msg = False, "Name can only contain letters."
            case _:
                _valid, msg = True, "Looks good!"

        return _valid, msg

    async def validate_asset_name(self, target: str | None) -> tuple[bool, str]:
        _valid, msg = init_validation(target=target)

        match target:
            case "" | None:
                _valid, msg = False, "Please input a name for your new asset."
            case target if len(target) > 60:
                _valid, msg = False, f"Name must be under 60 characters. Input was {len(target)} characters."
            case target if self._has_banned_character(target=target):
                _valid, msg = False, "Name contains invalid character."
            case _:
                _valid, msg = True, "Looks good!"

        return _valid, msg

    async def validate_email(self, target: str | None) -> tuple[bool, str]:
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
            case _:
                addr = target.split("@")
                if addr[1].endswith(valid_endings):
                    _valid, msg = True, "Looks good!"
                else:
                    _valid, msg = False, f"Email must contain a valid domain. Valid domains: {valid_endings}"

        return _valid, msg

    async def validate_phone_number(self, target: str | None) -> tuple[bool, str]:
        _valid, msg = init_validation(target=target)

        match target:
            case "" | None:
                _valid, msg = False, "Please input a phone number."
            case target if target.isdigit() is False:
                _valid, msg = False, "Phone # must be digits only."
            case target if len(target) > 15:
                _valid, msg = False, f"Phone number must be less than 15 characters. Length: {len(target)}"
            case _:
                _valid, msg = True, "Looks good!"

        return _valid, msg

    async def validate_imei_number(self, target: str | None) -> tuple[bool, str]:
        _valid, msg = init_validation(target=target)
        search = Searcher(token=self._token)

        match target:
            case "" | None:
                _valid, msg = False, "Please input your IMEI #."
            case target if target.isdigit() is False:
                _valid, msg = False, "IMEI # must be digits only."
            case target if len(target) != 15:
                _valid, msg = False, f"IMEI # must be exactly 15 characters. Length: {len(target)}"
            case _:
                """unit_is_available = await search.unit_is_available(imei=target)
                if unit_is_available:
                    unit_id = await search.by_imei(imei=target)
                    if unit_id:
                        _valid, msg = True, "Looks good!"
                    else:
                        _valid, msg = False, "Couldn't find associated unit. Try again or call if issue persists."
                else:
                    """
                print(search.by_imei(imei=target))
                _valid, msg = False, "Invalid unit. support@terminusgps.com has been notified of this error."
                    # TODO: Email myself this error.

        return _valid, msg

    async def validate_vin_number(self, target: str | None) -> tuple[bool, str]:
        _valid, msg = init_validation(target=target)
        _valid, msg = True, "Looks good!"
        return _valid, msg
