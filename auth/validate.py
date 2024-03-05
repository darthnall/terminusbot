import os

from dotenv import load_dotenv

from . import Searcher, Session


class Validator:
    def __init__(self, session: Session) -> None:
        self.session = session

    def validate(self, data: dict) -> dict | bool:
        results = {
            "firstName": self.validate_name(target=data["firstName"]),
            "lastName": self.validate_name(target=data["lastName"]),
            "email": self.validate_email(target=data["email"]),
            "assetName": self.validate_asset_name(target=data["assetName"]),
            "phoneNumber": self.validate_phone(target=data["phoneNumber"]),
            "imei": self.validate_imei(target=data["imei"]),
            "vin": self.validate_vin(target=data["vin"]),
        }
        bad_items = [key for key, value in results.items() if value is not True]
        if bad_items:
            return {"error": "bad validation", "items": bad_items}
        return True

    def validate_name(self, target: str) -> bool:
        print(f"validating `{target}`")
        if target.lower().isalpha():
            print(f"`{target = }...OK`")
            return True
        return False

    def validate_asset_name(self, target: str) -> bool:
        print(f"validating `{target}`")
        if len(target) < 60:
            print(f"`{target = }...OK`")
            return True
        return False

    def validate_email(self, target: str) -> bool:
        print(f"validating `{target}`")
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
                return True
        except AttributeError:
            return False
        return False

    def validate_phone(self, target: str) -> bool:
        print(f"validating `{target}`")
        print(f"`{target = }...OK`")
        return True

    def validate_imei(self, target: str) -> bool:
        print(f"validating `{target}`")
        if target == "":
            print(f"error: `{target = }` :: expected non-empty string")
            return False
        with Searcher(session=self.session) as search:
            if search.imei_to_id(target):
                print(f"`{target = }...OK`")
                return True
            return False

    def validate_vin(self, target: str) -> bool:
        print(f"validating `{target}`")
        print(f"`{target = }...OK`")
        return True
