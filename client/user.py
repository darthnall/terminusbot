import secrets
import string

from auth import Session

from . import EmailUser


class User:
    def __init__(self, data: dict[str, str], session: Session):
        self.session = session
        self.creds = {key: value for key, value in data.items()}
        self.creds.update({"password": self.generate_password(length=12)})

    def __repr__(self) -> str:
        return f"{self.creds = }"

    def create(self, name: str, password: str) -> dict:
        """
        Create a new user.

        Parameters
        ----------
        name: <str>
            The name of the new user.
        password: <str>
            The password of the new user.

        Returns
        -------
        _success: <bool>
            True if the user was created, False otherwise.

        """
        params = {
            "creatorId": 27881459, # Terminus-1000's user id
            "name": name,
            "password": password,
            "dataFlags": 1,
        }

        response = self.session.wialon_api.core_create_user(**params)

        self.creds["userId"] = response["item"]["id"]
        self.set_default_flags()

        _success = response

        return _success

    def set_default_perms(self, unit_id: int) -> None:
        # TODO: Convert hexadecimals to integers
        """
        Set user's default permissions.

        Parameters
        ----------
        unit_id: <int>
            The ID of the unit to set permissions for.

        Returns
        -------
        _success: <bool>
            True if the permission were set, False otherwise.

        """
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
        params = {"userId": self.creds["userId"], "flags": 2, "flagsMask": 0}
        self.session.wialon_api.user_update_user_flags(**params)

    def email_creds(self, creds: dict[str, str] | None = None) -> bool:
        """
        Email credentials to the user.

        Parameters
        ----------
        creds: <dict[str, str]> | <None>
            The credentials to email.

        Returns
        -------
        _success: <bool>
            True if the email was sent, False otherwise.

        """
        if creds is not None:
            self.creds = creds
        to_addr = self.creds["email"]
        email = EmailUser()
        return email.send(to_addr=to_addr, username=self.creds["email"], password=self.creds["password"])

    def assign_phone(self, user_id: int, phone_number: int) -> bool:
        _success = False
        """
        Assign a phone number to a user.

        Parameters
        ----------
        user_id: <int>
            Target user's ID.

        phone_number: <int>
            The phone number to assign to target.

        Returns
        -------
        _success: <bool>
            True if the phone number was assigned, False otherwise.

        """
        # Check if arg user_id is the same as the user's id
        if (item_id := int(self.creds["userId"])) != user_id:
            item_id = user_id

        # Check if arg phone_number is the same as the user's phone number
        if (num := int(self.creds["phoneNumber"])) != phone_number:
            num = phone_number

        # Update the user's phone number using Wialon API
        params = {
            "itemId": item_id,
            "callMode": "create",
            "n": "phoneNumber",
            "v": num,
        }

        # NOTE: The Wialon API returns empty dict on success
        response = self.session.wialon_api.item_update_custom_field(**params)

        try:
            response["id"]
            _success = True
        except KeyError:
            _success = False

        return _success

    def generate_password(self, length: int) -> str:
        """
        Create a random Wialon API compliant password.

        Parameters
        ----------
        length: <int>
            The length of the password.

        Returns
        -------
        password: <str>
            The password.

        Password Requirements
        ---------------------
        - At least one lowercase letter
        - At least one number
        - At least one special character
        - At least one uppercase letter
        - Different from username
        - Minumum 8 charcters

        """
        length += 1
        letters: tuple = tuple(string.ascii_letters)
        numbers: tuple = tuple(string.digits)
        symbols: tuple = ("@", "#", "$", "%")

        while True:
            password = "".join(
                secrets.choice(letters + numbers + symbols) for i in range(length)
            )
            if (
                any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3
            ):
                break

        return password
