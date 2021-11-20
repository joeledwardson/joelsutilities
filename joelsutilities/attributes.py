from typing import Any, List
import functools
import re


def dgetattr(obj: object, name: str, is_dict=False) -> Any:
    """
    get deep attribute
    operates the same as getattr(obj, name) but can use '.' for nested attributes
    e.g. dgetattr(my_object, 'a.b') would return value of my_object.a.b
    """
    atr = dict.__getitem__ if is_dict else getattr
    names = name.split('.')
    names = [obj] + names
    return functools.reduce(atr, names)


def dattr_name(deep_attr: str) -> str:
    """
    get deep attribute name
    e.g. dattr_name('my_object.a.b') would return 'b'
    """
    return re.match(r'(.*[.])?(.*)', deep_attr).groups()[1]


def object_members(o: object) -> List[str]:
    """
    get object members
    get all members of a class instance etc that are:
    - not private (starting with underscore)
    - not Callable
    """
    return [k for k in o.__dir__() if not re.match('^_', k) and not callable(getattr(o, k))]