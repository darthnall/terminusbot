def calc_mask(flags: list[str]) -> int:
    return sum([int(flag, 16) for flag in flags])

if __name__ == "__main__":
    hex_flags = [
        "0x0001",  # View item and basic properties
        "0x0002",  # View detailed item properties
        "0x0004",  # Manage access to this item
        "0x0010",  # Rename item
        "0x0100",  # Change icon
        "0x0200",  # Query reports or messages
        "0x4000",  # View attached files
    ]
    print(calc_mask(flags=hex_flags))
