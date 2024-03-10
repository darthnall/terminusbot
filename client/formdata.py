from typing import Any, Iterable
from dataclasses import dataclass

@dataclass(init=True)
class RegistrationForm:
    first_name:   dict[str, dict[str, Any]] | None = None
    last_name:    dict[str, dict[str, Any]] | None = None
    email:        dict[str, dict[str, Any]] | None = None
    asset_name:   dict[str, dict[str, Any]] | None = None
    phone_number: dict[str, dict[str, Any]] | None = None
    vin:          dict[str, dict[str, Any]] | None = None
    imei:         dict[str, dict[str, Any]] | None = None

    data:   list[dict[str, dict[str, Any]]] | None = None

    def create(self):
        self.first_name   = self._create_first_name()
        self.last_name    = self._create_last_name()
        self.email        = self._create_email()
        self.asset_name   = self._create_asset_name()
        self.phone_number = self._create_phone_number()
        self.vin          = self._create_vin()
        self.imei         = self._create_imei()

        data = [
            self.first_name,
            self.last_name,
            self.email,
            self.asset_name,
            self.phone_number,
            self.vin,
            self.imei
        ]

        return data

    def _create_first_name(self) -> dict[str, dict[str, Any]]:
        return {
            "firstName": {
                "valid": None,
                "displayAs": "First Name",
                "endpoint": "/v/first_name",
                "userInput": ""
            }
        }

    def _create_last_name(self) -> dict[str, dict[str, Any]]:
        return {
            "lastName": {
                "valid": None,
                "displayAs": "Last Name",
                "endpoint": "/v/last_name",
                "userInput": ""
            }
        }

    def _create_email(self) -> dict[str, dict[str, Any]]:
        return {
            "email": {
                "valid": None,
                "displayAs": "Email",
                "endpoint": "/v/email",
                "userInput": ""
            }
        }

    def _create_asset_name(self) -> dict[str, dict[str, Any]]:
        return {
            "assetName": {
                "valid": None,
                "displayAs": "Asset Name",
                "endpoint": "/v/asset_name",
                "userInput": ""
            }
        }

    def _create_phone_number(self) -> dict[str, dict[str, Any]]:
        return {
            "phoneNumber": {
                "valid": None,
                "displayAs": "Phone #",
                "endpoint": "/v/phone_number",
                "userInput": ""
            }
        }

    def _create_vin(self) -> dict[str, dict[str, Any]]:
        return {
            "vin": {
                "valid": None,
                "displayAs": "Vin #",
                "endpoint": "/v/vin",
                "userInput": ""
            }
        }

    def _create_imei(self) -> dict[str, dict[str, Any]]:
        return {
            "imei": {
                "valid": None,
                "displayAs": "IMEI #",
                "endpoint": "/v/imei",
                "userInput": ""
            }
        }
