from integrations.twiliophone.caller import TwilioCaller

class PhoneNotifier:
    def __init__(self) -> None:
        self.caller = TwilioCaller()

        return None

    def notify(self, phone: str, msg: str) -> None:
        self.caller.send(phone, msg)

        return None

    def batch_notify(self, phones: list[str], msg: str) -> None:
        for phone in phones:
            self.notify(phone, msg)

        return None
