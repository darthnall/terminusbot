from . import Searcher, Session


class Validator:
    def __init__(self, token: str) -> None:
        self._token = token

    def _has_banned_character(self, target: str) -> tuple[bool, list]:
        has_banned_character = False
        banned_characters = ["*"]

        matches = [char for char in list(target) if char in banned_characters]

        if any(matches):
            has_banned_character = True

        return (has_banned_character, matches)

    def validate_all(self, data: dict[str, str]) -> dict:
        results = {
            "firstName": {"name": "First name", "valid": self.validate_name(target=data["firstName"]), "target": data["firstName"] },
            "lastName": { "name": "Last name", "valid": self.validate_name(target=data["lastName"]), "target": data["lastName"] },
            "email": { "name": "Email", "valid": self.validate_email(target=data["email"]), "target": data["email"] },
            "assetName": { "name": "Asset name", "valid": self.validate_asset_name(target=data["assetName"]), "target": data["assetName"] },
            "phoneNumber": { "name": "Phone #", "valid": self.validate_phone(target=data["phoneNumber"]), "target": data["phoneNumber"] },
            "imei": { "name": "IMEI #", "valid": self.validate_imei(target=data["imei"]), "target": data["imei"] },
            "vin": { "name": "VIN #", "valid": self.validate_vin(target=data["vin"]), "target": data["vin"] },
        }

        return results

    def validate_test(self, target: str) -> bool:
        _valid: bool = False
        print(f"validating `{target}`")

        if target != "" and target.isnumeric():
            _valid = True
            print(f"`{target = }...OK`")

        return _valid

    def validate_name(self, target: str) -> bool:
        _valid: bool = False
        print(f"validating `{target}`")

        if target != "" and target.lower().isalpha():
            _valid = True
            print(f"`{target = }...OK`")

        return _valid

    def validate_asset_name(self, target: str) -> bool:
        _valid: bool = False
        print(f"validating `{target}`")

        if target != "" and len(target) < 60:
            _valid = True
            print(f"`{target = }...OK`")

        return _valid

    def validate_email(self, target: str) -> bool:
        _valid: bool = False
        print(f"validating `{target}`")

        if target == "":
            _valid = False

        valid_endings: tuple = (
            ".com",
            ".net",
            ".edu",
            ".org",
            ".gov",
            ".me",
            ".io",
        )

        try:
            addr: list[str] = target.split("@")
            if addr[0].lower().isalnum() and addr[1].endswith(valid_endings):
                print(f"`{target = }...OK`")
                _valid = True
        except AttributeError:
            _valid = False
        return _valid

    def validate_phone(self, target: str) -> bool:
        _valid: bool = False

        print(f"validating `{target}`")
        _valid = True

        print(f"`{target = }...OK`")
        return _valid

    def validate_imei(self, target: str) -> bool:
        _valid: bool = False

        print(f"validating `{target}`")
        if target == "":
            print(f"error: `{target = }` :: expected non-empty string")
            _valid = False

        search = Searcher(token=self._token)
        if search.by_imei(imei=target):
            print(f"`{target = }...OK`")
            _valid = True

        return _valid

    def validate_vin(self, target: str) -> bool:
        _valid: bool = False

        print(f"validating `{target}`")
        _valid = True
        print(f"`{target = }...OK`")
        return _valid
