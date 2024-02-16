# Search queries for webapp

def generate(_filter: str | None) -> dict | None:
    if _filter is None or _filter == '':
        return {
            'spec': {
                'itemsType': 'user',
                'propName': 'sys_name,sys_id',
                'propValueMask': '*',
                'sortType': 'sys_name'
            },
            'force': 1,
            'flags': 1,
            'from': 0,
            'to': 0
        }
    else:
        return {
            'spec': {
                'itemsType': 'user',
                'propName': 'sys_name,sys_id',
                'propValueMask': _filter,
                'sortType': 'sys_name'
            },
            'force': 1,
            'flags': 1,
            'from': 0,
            'to': 0
        }
