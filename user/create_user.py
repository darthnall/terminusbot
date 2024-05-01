from auth.session import Session
from dataclasses import dataclass

from user.errors import WialonUserExistsError, VideoUserExistsError


@dataclass
class TerminusUser:
    first: str
    last: str
    email: str
    phone: str = None

    is_wialon_user: bool = False
    is_video_user: bool = False

    def create_wialon_user(self, params: dict) -> None:
        with Session() as session:
            session.wialon_api.core_create_user(**params)
            self.is_wialon_user = True

    def create_video_user(self, params: dict) -> None:
        print("Creating video user...")
        print("Created video user.")

    @property
    def fullname(self) -> str:
        return f"{self.first} {self.last}"
