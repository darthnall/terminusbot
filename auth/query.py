# Search queries for webapp

def generate(_filter: str | None, category: str | None) -> dict | None:
    categories = {
            "Users": "user",
            "Hardware Type": "hw_type"
            }
    if category not in categories:
        return None
    if _filter is None or _filter == '':
        return {
            'spec': {
                'itemsType': categories[category],
                'propName': 'sys_name',
                'propValueMask': '*',
                'sortType': 'sys_name',
            },
            'force': 1,
            'flags': 1,
            'from': 0,
            'to': 0
        }
    else:
        return {
            'spec': {
                'itemsType': categories[category],
                'propName': 'sys_name',
                'propValueMask': _filter,
                'sortType': 'sys_name',
            },
            'force': 1,
            'flags': 1,
            'from': 0,
            'to': 0
        }

def search_hardware(_filter: str | None, category: str | None) -> dict | None:
    pass
