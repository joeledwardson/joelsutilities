import json
from typing import Any


def is_jsonable(x: Any) -> bool: 
    """
    determine if data can be serialized safely with `json.dumps`
    
    >>> is_jsonable("some string")
    True
    >>> is_jsonable(12345)
    True
    >>> is_jsonable(object())
    False
    """
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False
