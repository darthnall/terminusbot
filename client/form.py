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
