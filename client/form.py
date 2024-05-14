from dataclasses import dataclass
from typing import Optional


class RegistrationField(dict):
    def __init__(self, *args, **kwargs) -> None:
        super(RegistrationField, self).__init__(*args, **kwargs)

        return None

    id: str
    display_as: str
    required: bool = True
    starts_hidden: bool = False
    type: str = "text"
    user_input: Optional[str]
    validation_endpoint: Optional[str] = "/v"
    on_input: Optional[str] = ""
    placeholder: Optional[str] = ""
    is_valid: Optional[bool]
    validation_msg: Optional[str]


class RegistrationForm:
    def __init__(self) -> None:
        self.first_name = RegistrationField(
            id="firstName",
            display_as="First Name",
            placeholder="First",
            on_input="updateAssetName()",
            validation_endpoint="/v/first-name",
        )
        self.last_name = RegistrationField(
            id="lastName",
            display_as="Last Name",
            placeholder="Last",
            validation_endpoint="/v/last-name",
        )
        self.email = RegistrationField(
            id="email",
            display_as="Email",
            placeholder="Email",
            validation_endpoint="/v/email",
        )
        self.asset_name = RegistrationField(
            id="assetName",
            display_as="Asset Name",
            placeholder="Asset",
            validation_endpoint="/v/asset-name",
        )
        self.imei = RegistrationField(
            id="imeiNumber",
            display_as="IMEI",
            placeholder="IMEI #",
            validation_endpoint="/v/imei-number",
        )
        self.phone = RegistrationField(
            id="phoneNumber",
            display_as="Phone",
            placeholder="Phone #",
            validation_endpoint="/v/phone-number",
            required=False,
            starts_hidden=True,
        )
        self.vin = RegistrationField(
            id="vinNumber",
            display_as="VIN",
            placeholder="VIN #",
            validation_endpoint="/v/vin-number",
            required=False,
            starts_hidden=True,
        )


@dataclass(init=True)
class Field:
    id: str
    display_as: str
    validation_endpoint: str = "/v"
    on_input: str | None = None
    is_valid: bool | None = None
    placeholder: str = ""
    required: bool = True
    user_input: str | None = None
    type: str = "text"
    starts_hidden: bool = False
    validation_msg: str | None = None


def create_registration_form() -> dict[str, Field]:
    return {
        "firstName": Field(
            "firstName",
            "First Name",
            placeholder="First",
            validation_endpoint="/v/first-name",
            on_input="updateAssetName()",
        ),
        "lastName": Field(
            "lastName",
            "Last Name",
            placeholder="Last",
            validation_endpoint="/v/last-name",
        ),
        "assetName": Field(
            "assetName",
            "Asset Name",
            placeholder="Asset",
            validation_endpoint="/v/asset-name",
            on_input="disableAutoUpdate()",
        ),
        "email": Field(
            "email",
            "Email",
            placeholder="Email",
            validation_endpoint="/v/email",
            type="email",
        ),
        "imeiNumber": Field(
            "imeiNumber",
            "IMEI #",
            placeholder="IMEI",
            validation_endpoint="/v/imei-number",
            required=True,
        ),
        "phoneNumber": Field(
            "phoneNumber",
            "Phone #",
            placeholder="Phone",
            validation_endpoint="/v/phone-number",
            required=False,
            starts_hidden=True,
        ),
        "vinNumber": Field(
            "vinNumber",
            "VIN #",
            placeholder="VIN",
            validation_endpoint="/v/vin-number",
            required=False,
            starts_hidden=True,
        ),
    }
