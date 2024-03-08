from typing import Any

def create_form_data(**kwargs) -> dict[str, Any]:
    return {key: value for key, value in kwargs.items()}
