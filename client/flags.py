from auth import Session
from . import User

class Flags():
    def __init__(self, session: Session):
        self.session = session

    def set(self, user_id: str, flags: list[str|int]) -> bool:
        for flag in flags:
            if isinstance(flag, int):
                pass
            else:
                int_flags = self.convert(flags=flags)
                break

    def convert(self, flags: list[str]) -> int:
        return sum([int(flag, 16) for flag in flags])
