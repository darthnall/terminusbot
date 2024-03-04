from auth import Session

from . import User


class Flags:
    UNIT_DEFAULT = [
        # GENERAL
        "0x0001",  # View item and its basic properties
        "0x0002",  # View detailed item properties
        "0x0004",  # Manage access to this item
        "0x0010",  # Rename item
        "0x0020",  # View custom fields
        "0x0100",  # Change icon
        "0x4000",  # View attached files
    ]

    UNIT_DESTRUCTIVE = [
        # GENERAL
        "0x0008", # Delete item
    ]

    def __init__(self, session: Session):
        self.session = session

    def set(self, item_id: int, user_id: int, flags: list[str | int], defaults: bool = False) -> bool:
        """
            Set user permissions of item based on a list of flags defined in the Wialon API documentation.

            Parameters:
                item_id <int>: Item ID to be assigned to user.
                user_id <int>: Item ID of the user.
                flags <list[str | int]>: List of flags to be assigned to user. Can be <int> or <str>.

            Returns:
                <bool>: True if flags were set successfully. False if something went wrong.
        """
        int_flags = [flag for flag in flags if isinstance(flag, int)]
        str_flags = [flag for flag in flags if isinstance(flag, str)]

        if defaults:
            str_flags += self.UNIT_DEFAULT
        access_mask = self.convert(flags=str_flags)
        access_mask += sum(int_flags)

        params = {"userId": user_id, "itemId": item_id, "accessMask": access_mask}
        response = self.session.wialon_api.user_update_item_access(**params)

        if not response:
            return True
        return False

    def convert(self, flags: list[str]) -> int:
        return sum([int(flag, 16) for flag in flags])
