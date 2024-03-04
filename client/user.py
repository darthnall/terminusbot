import random
import string

from auth import Session

from . import EmailUser

class User():
    def __init__(self, data: dict, session: Session):
        self.session = session
        self.creds = {key: value for key, value in data.items()}
        self.creds.update({"password": self.generate_password(length=12)})

    def __repr__(self) -> str:
        return f"User credentials: {self.creds}"

    def create(self, name: str, password: str) -> dict:
        params = {
            "creatorId": 27881459,  # Terminus-1000's user id
            "name": name,  # User's email
            "password": password,  # Generated password
            "dataFlags": 1,  # Default flags
        }

        response = self.session.wialon_api.core_create_user(**params)

        self.creds["userId"] = response["item"]["id"]
        self.set_default_flags()
        # self.set_default_perms(unit_id=self.id)

        return response

    def set_default_perms(self, unit_id: str | int | None) -> None:
        # TODO: Convert hexadecimals to integers
        flags = [
            0x0001,  # View item and basic properties
            0x0002,  # View detailed item properties
            0x0004,  # Manage access to this item
            0x0010,  # Rename item
            0x0100,  # Change icon
            0x0200,  # Query reports or messages
            0x4000,  # View attached files
        ]
        params = {
            "userId": self.creds["userId"],
            "itemId": unit_id,
            "accessMask": sum(flags),
        }
        self.session.wialon_api.user_update_item_access(**params)

    def set_default_flags(self) -> None:
        params = {"userId": self.creds["userId"], "flags": 0x02, "flagsMask": 0x00}
        self.session.wialon_api.user_update_user_flags(**params)

    def email_creds(self, creds: dict) -> bool:
        email = EmailUser(creds=creds)
        return email.send(to_addr=creds["email"])

    def assign_phone(self, phone_number: str) -> bool:
        params = {"itemId": self.creds["userId"], "phoneNumber": phone_number}
        response = self.session.wialon_api.unit_update_phone(**params)
        # TODO: I have no idea what self.session.wialon_api.unit_update_phone() returns
        return bool(response)

    def generate_password(self, length: int) -> str:
        """
        Password requirements:
            - At least one lowercase letter
            - At least one number
            - At least one special character
            - At least one uppercase letter
            - Different from username
            - Minumum 8 charcters
        """
        password_list: list = []

        for i in range(length - 3):
            password_list += random.choice(list(string.ascii_lowercase))
        password_list += random.choice(list(string.ascii_uppercase))
        password_list += random.choice(["!", "@", "#", "$"])
        password_list += str(random.choice(range(1, 9, 1)))
        return "".join(password_list)
