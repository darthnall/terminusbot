from dataclasses import dataclass

@dataclass(init=True)
class Field:
    id: str
    display_as: str = id
    validation_endpoint: str = "/v"
    on_input: str | None = None
    validation_result: bool | None = None
    placeholder: str = ""
    required: bool = True
    user_input: str | None = None
    type: str = "text"


def create_registration_form() -> list[Field]:
    return [
        Field(
            "firstName",
            "First Name",
            placeholder="First",
            validation_endpoint="/v/first-name",
            on_input="updateAssetName()",
        ),
        Field(
            "lastName",
            "Last Name",
            placeholder="Last",
            validation_endpoint="/v/last-name",
        ),
        Field(
            "assetName",
            "Asset Name",
            placeholder="Asset",
            validation_endpoint="/v/asset-name",
            on_input="disableAutoUpdate()"
        ),
        Field(
            "email",
            "Email",
            placeholder="Email",
            validation_endpoint="/v/email",
            type="email"
        ),
        Field(
            "phoneNumber",
            "Phone #",
            placeholder="Phone",
            validation_endpoint="/v/phone-number",
            required=False,
        ),
        Field(
            "vinNumber",
            "VIN #",
            placeholder="VIN",
            validation_endpoint="/v/vin-number",
            required=False,
        ),
        Field(
            "imeiNumber",
            "IMEI #",
            placeholder="IMEI",
            validation_endpoint="/v/imei-number",
            required=True,
        )
    ]
