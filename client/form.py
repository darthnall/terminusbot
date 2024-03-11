from dataclasses import dataclass

@dataclass(init=True)
class Field:
    id: str
    display_as: str
    validation_endpoint: str = "/v"
    on_input: str | None = None
    validation_result: bool | None = None
    placeholder: str = ""
    required: bool = True
    user_input: str | None = None
    type: str = "text"
    starts_hidden: bool = False
    validation_msg: str | None = None


def create_registration_form() -> dict[str, Field]:
    return {
        "firstName":
        Field(
            "firstName",
            "First Name",
            placeholder="First",
            validation_endpoint="/v/first-name",
            on_input="updateAssetName()",
        ),
        "lastName":
        Field(
            "lastName",
            "Last Name",
            placeholder="Last",
            validation_endpoint="/v/last-name",
        ),
        "assetName":
        Field(
            "assetName",
            "Asset Name",
            placeholder="Asset",
            validation_endpoint="/v/asset-name",
            on_input="disableAutoUpdate()"
        ),
        "email":
        Field(
            "email",
            "Email",
            placeholder="Email",
            validation_endpoint="/v/email",
            type="email"
        ),
        "phoneNumber":
        Field(
            "phoneNumber",
            "Phone #",
            placeholder="Phone",
            validation_endpoint="/v/phone-number",
            required=False,
        ),
        "imeiNumber":
        Field(
            "imeiNumber",
            "IMEI #",
            placeholder="IMEI",
            validation_endpoint="/v/imei-number",
            required=True,
        ),
        "vinNumber":
        Field(
            "vinNumber",
            "VIN #",
            placeholder="VIN",
            validation_endpoint="/v/vin-number",
            required=False,
            starts_hidden=True,
        ),
    }
