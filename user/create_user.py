from auth.session import Session
from auth.flags import WialonApiFlags as flags
from dataclasses import dataclass


@dataclass
class TerminusUser:
    first: str
    last: str
    email: str
    phone: str = None

    is_wialon_user: bool = False
    is_video_user: bool = False

    def create_wialon_user(self, params: dict) -> None:
        if not self.is_wialon_user:
            with Session() as session:
                session.wialon_api.core_create_user(**params)
                self.is_wialon_user = True

    def create_video_user(self, params: dict) -> None:
        print("Creating video user...")
        print("Created video user.")

    @property
    def fullname(self) -> str:
        return f"{self.first} {self.last}"

def main():
    params = {}
    user = TerminusUser(
        first="John",
        last="Doe",
        email="john@doe.com",
        phone="+17133049421",
    ).create_wialon_user(params=params)
    print(user.is_wialon_user)

if __name__ == "__main__":
    flags = flags.UserFlags
    print(flags.BASE.value)
