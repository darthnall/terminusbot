from auth import Session

class Flags:
    USER_FLAGS = {
        0x01, # User disabled
        0x02, # Can't change password
        0x04, # Can create items
        0x10, # Can't change settings
        0x20, # Can send SMS
    }
    UNIT_DEFAULT = [
        # GENERAL
        0x0001,  # View item and its basic properties
        0x0002,  # View detailed item properties
        0x0004,  # Manage access to this item
        0x0010,  # Rename item
        0x0020,  # View custom fields
        0x0100,  # Change icon
        0x4000,  # View attached files
    ]

    UNIT_DESTRUCTIVE = [
        # GENERAL
        0x0008, # Delete item
    ]

    def __init__(self, session: Session):
        self.session = session

    def allow_password_change(self, user_id: int) -> None:
        flags = 0x02 + 0x10
        flags_mask = flags - 0x02
        params = { "userId": user_id, "flags": flags, "flagsMask": flags_mask }

        self.session.wialon_api.user_update_user_flags(**params)

    def set(self, user_id: int, flags: int) -> bool:
        """
            Set user permissions of item based on a list of flags defined in the Wialon API documentation.

            Parameters:
                item_id <int>: Item ID to be assigned to user.
                user_id <int>: Item ID of the user.
                flags <list[str | int]>: List of flags to be assigned to user. Can be <int> or <str>.

            Returns:
                <bool>: True if flags were set successfully. False if something went wrong.
        """
        params = {"userId": user_id, "flags": flags, "accessMask": access_mask}
        response = self.session.wialon_api.user_update_item_access(**params)

        return bool(response)
