from auth import Session, Validator
from dotenv import load_dotenv

class BaseTest:
    def __init__(self, iter: int = 1_000_000) -> None:
        self._iter = iter

    @property
    def iter(self) -> int:
        return self._iter

class ValidationTest(BaseTest):
    def __init__(self, iter: int) -> None:
        super().__init__(iter=iter)

    def run(self) -> None:
        print(self.iter)

if __name__ == "__main__":
    ValidationTest(iter=1_000).run()
