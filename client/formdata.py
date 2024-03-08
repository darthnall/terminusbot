from typing import Any

def create_new_form(**kwargs) -> dict[str, Any]:
    return {key: value for key, value in kwargs.items()}

def create_validated_form(**kwargs) -> dict[str, Any]:
    return {key: dict(value) for key, value in kwargs.items()}
