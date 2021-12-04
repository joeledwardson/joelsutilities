import json


def is_jsonable(x):
    """
    determine if data can be serialized
    """
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False
