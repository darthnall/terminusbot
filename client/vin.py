from typing import Any

from vininfo import Vin


class Vehicle:
    def __init__(self, vin_num: str) -> None:
        self._vin_num = self.validate_vin_num(vin_num)
        self._vin = Vin(vin_num)

        if self._vin.details is not None:
            self.set_details(self._vin.details)

    def __str__(self) -> str:
        string = f"VIN: {self._vin_num}\n"
        if self._vin.details is not None:
            string = f"{string}Country: {self.country}\nManufacturer: {self.manufacturer}\nRegion: {self.region}"
        return string

    def __repr__(self) -> str:
        return f"Vehicle({self._vin_num})"

    @property
    def country(self) -> str:
        return self._country

    @property
    def manufacturer(self) -> str:
        return self._manufacturer

    @property
    def region(self) -> str:
        return self._region

    def validate_vin_num(self, vin_num: str) -> bool:
        match vin_num:
            case vin_num if len(vin_num) == 17:
                return vin_num
            case _:
                raise ValueError("VIN must be 17 characters long.")

    def set_details(self, details: dict[str, Any]) -> None:
        for key, value in details.items():
            match key:
                case "Country":
                    self._country = value
                case "Manufacturer":
                    self._manufacturer = value
                case "Region":
                    self._region = value
                case _:
                    continue

if __name__ == "__main__":
    lexus = Vehicle("JTHBA30G065155212")
