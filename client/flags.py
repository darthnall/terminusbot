from auth import Session
from dataclasses import dataclass

@dataclass
class Flags:
    user: dict = {
        "disable_user": 0x01,
        "cant_change_password": 0x02,
        "can_create_items": 0x04,
        "cant_change_settings": 0x10,
        "can_send_sms": 0x20,
    }
    unit: dict = {
        "view_item_and_its_basic_properties": 0x0001,
        "view_detailed_item_properties": 0x0002,
        "manage_access_to_this_item": 0x0004,
        "rename_item": 0x0010,
        "view_custom_fields": 0x0020,
        "change_icon": 0x0100,
        "view_attached_files": 0x4000,
    }

class Flagsu:
    USER_FLAGS: set = {
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
        flags = Flags.user["cant_change_password"] + Flags.user["cant_change_settings"]
        flags_mask = flags - Flags.user["cant_change_password"]
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
