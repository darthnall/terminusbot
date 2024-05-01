import requests

import unittest

class PhoneNotificationTest(unittest.TestCase):
    def test_send_notification(self, to_number: str = "+1713049421", msg: str = None) -> None:
